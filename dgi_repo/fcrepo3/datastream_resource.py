"""
Class file for the implementation of the datastream resource.
"""

from psycopg2.extensions import ISOLATION_LEVEL_READ_COMMITTED

import dgi_repo.database.read.repo_objects as object_reader
import dgi_repo.database.read.datastreams as ds_reader
import dgi_repo.database.write.datastreams as ds_writer
import dgi_repo.database.delete.datastreams as ds_purger
import dgi_repo.utilities as utils
import dgi_repo.fcrepo3.utilities as fedora_utils
from dgi_repo.exceptions import (ObjectDoesNotExistError,
                                 DatastreamDoesNotExistError,
                                 DatastreamExistsError,
                                 DatastreamConflictsError,
                                 ExternalDatastreamsNotSupported)
from dgi_repo.fcrepo3 import api, foxml
from dgi_repo.database.utilities import get_connection


class DatastreamResource(api.DatastreamResource):
    """
    Provide the datastream CRUD endpoints.
    """

    def _create_datastream(self, req, pid, dsid):
        """
        Persist the new datastream.

        Raises:
            DatastreamExistsError: The object doesn't exist.
        """
        conn = get_connection(ISOLATION_LEVEL_READ_COMMITTED)
        with conn, conn.cursor() as cursor:
            ds_info = ds_reader.datastream_from_raw(pid, dsid,
                                                    cursor=cursor).fetchone()
            if ds_info:
                raise DatastreamExistsError(pid, dsid)
            self._upsert_ds(req, pid, dsid, cursor)

    def _update_datastream(self, req, pid, dsid):
        """
        Commit the modification to the datastream.
        """
        conn = get_connection(ISOLATION_LEVEL_READ_COMMITTED)
        with conn, conn.cursor() as cursor:
            ds_reader.datastream_from_raw(pid, dsid, cursor=cursor)
            ds_info = cursor.fetchone()
            if ds_info is None:
                raise DatastreamDoesNotExistError(pid, dsid)
            ds = dict(ds_info)
            ds['committed'] = ds['modified']
            ds['datastream'] = ds['id']
            del ds['id']
            # Check modified date param, exiting if needed.
            modified_date = req.get_param('lastModifiedDate')
            if modified_date is not None:
                modified_date = utils.iso8601_to_datetime(modified_date)
                if ds['committed'] > modified_date:
                    raise DatastreamConflictsError(pid, dsid, ds['committed'],
                                                   modified_date)
            if ds_info['versioned']:
                ds_writer.upsert_old_datastream(ds, cursor=cursor)

            if ds['resource'] is not None:
                ds['mimetype'] = ds_reader.mime_from_resource(
                    ds['resource'],
                    cursor=cursor
                ).fetchone()['mime']
            self._upsert_ds(req, pid, dsid, cursor, ds=ds)
        return

    def _delete_datastream(self, req, pid, dsid):
        """
        Purge the datastream (or range of versions).

        @TODO: handle logMessage when audit is dealt with.
        """
        start = utils.iso8601_to_datetime(req.get_param('startDT'))
        end = utils.iso8601_to_datetime(req.get_param('endDT'))
        with get_connection() as conn, conn.cursor() as cursor:
            ds_purger.delete_datastream_versions(
                pid,
                dsid,
                start=start,
                end=end,
                cursor=cursor
            )
            if not cursor.rowcount:
                object_info = object_reader.object_id_from_raw(
                    pid,
                    cursor=cursor
                ).fetchone()
                if object_info is None:
                    # Only raise if the object is missing because Fedora.
                    raise ObjectDoesNotExistError(pid)

            foxml.internalize_rels(pid, dsid,
                                   req.env['wsgi.identity'].source_id,
                                   cursor=cursor)
        return (start, end)

    def _upsert_ds(self, req, pid, dsid, cursor, ds=None):
        """
        Upsert a datastream.

        Raises:
            ObjectDoesNotExistError: The object doesn't exist.
        """
        if ds is not None:
            ds = dict(ds)
            del ds['modified']
        else:
            ds = {}

        object_info = object_reader.object_id_from_raw(
            pid, cursor=cursor).fetchone()
        if object_info is None:
            raise ObjectDoesNotExistError(pid)

        control_group = req.get_param('controlGroup', default='M')
        if control_group == 'E':
            raise ExternalDatastreamsNotSupported

        ds_location = req.get_param('dsLocation')
        data_ref = None
        data = None
        if ds_location is not None:
            if control_group == 'R':
                data_ref = {
                    'TYPE': 'URL',
                    'REF': ds_location,
                }
            else:
                data_ref = {
                    'TYPE': 'INTERNAL_ID',
                    'REF': ds_location,
                }
        else:
            try:
                data = req.get_param('file').file
            except AttributeError:
                # Data can come as the request body.
                if req.content_length:
                    data = req.stream

        checksums = []
        checksum = req.get_param('checksum')
        checksum_type = req.get_param('checksumType')
        if checksum is not None or checksum_type is not None:
            checksums.append({
                'checksum': checksum,
                'type': checksum_type,
            }),

        ds.update({
            'dsid': dsid,
            'object': object_info['id'],
            'log': fedora_utils.resolve_log(req, cursor),
            'checksums': checksums,
            'data_ref': data_ref,
            'data': data,
        })

        label_in = req.get_param('dsLabel')
        if label_in is not None:
            ds['label'] = label_in
        ds.setdefault('label', '')

        ds.setdefault('control_group', control_group)

        version_in = req.get_param('versionable')
        if version_in:
            ds['versioned'] = version_in != 'false'
        ds.setdefault('versioned', True)

        mime_in = req.get_param('mimeType')
        if mime_in:
            ds['mimetype'] = mime_in
        ds.setdefault('mimetype', 'application/octet-stream')

        state_in = req.get_param('dsState')
        if state_in:
            ds['state'] = state_in
        ds.setdefault('state', 'A')

        fedora_utils.write_ds(ds, cursor=cursor)
        foxml.internalize_rels(pid, dsid,
                               req.env['wsgi.identity'].source_id,
                               cursor=cursor)

    def _get_datastream_info(self, pid, dsid, asOfDateTime=None, **kwargs):
        """
        Get the ds* values in a dict, to build the datastream profile.
        """
        with get_connection() as conn, conn.cursor() as cursor:
            ds_reader.datastream_from_raw(pid, dsid, cursor=cursor)
            ds_info = cursor.fetchone()
            if ds_info is None:
                raise DatastreamDoesNotExistError(pid, dsid)
            if asOfDateTime is not None:
                time = utils.iso8601_to_datetime(asOfDateTime)
                ds_info = ds_reader.datastream_as_of_time(
                    ds_info['id'],
                    time,
                    cursor=cursor
                )
                if ds_info is None:
                    raise DatastreamDoesNotExistError(pid, dsid, time)
            return fedora_utils.datastream_to_profile(ds_info, cursor)
