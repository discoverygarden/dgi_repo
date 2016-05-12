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
        """
        conn = get_connection(ISOLATION_LEVEL_READ_COMMITTED)
        with conn, conn.cursor() as cursor:
            self._upsert_ds(req, pid, dsid, cursor)

    def _update_datastream(self, req, pid, dsid):
        """
        Commit the modification to the datastream.
        """
        conn = get_connection(ISOLATION_LEVEL_READ_COMMITTED)
        with conn, conn.cursor() as cursor:
            ds_reader.datastream_from_raw(pid, dsid, cursor=cursor)
            ds_info = cursor.fetchone()
            if ds_info is not None:
                ds = dict(ds_info)
                ds['committed'] = ds['modified']
                ds['datastream'] = ds['id']
                del ds['id']
                # Check modified date param, exiting if needed.
                modified_date = req.get_param('lastModifiedDate')
                if modified_date is not None:
                    modified_date = utils.iso8601_to_datetime(modified_date)
                    if ds['committed'] > modified_date:
                        raise DatastreamConflictsError(pid, dsid,
                                                       ds['committed'],
                                                       modified_date)
                ds_writer.upsert_old_datastream(ds, cursor=cursor)
            else:
                raise DatastreamDoesNotExistError(pid, dsid)

            self._upsert_ds(req, pid, dsid, cursor, ds=ds_info)
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
            foxml.internalize_rels(pid, dsid,
                                   req.env['wsgi.identity'].source_id,
                                   cursor=cursor)

    def _upsert_ds(self, req, pid, dsid, cursor, ds=None):
        """
        Upsert a datastream.

        Raises:
            ObjectDoesNotExistError: The object doesn't exist.
        """
        ds = dict(ds) if ds is not None else {}
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
                pass
        checksums = None
        checksum = req.get_param('checksum')
        if checksum is not None:
            checksums.append({
                'checksum': checksum,
                'type': req.get_param('checksumType'),
            }),
        ds.update({
            'dsid': dsid,
            'object': object_info['id'],
            'log': fedora_utils.resolve_log(req, cursor),
            'control_group': control_group,
            'label': req.get_param('dsLabel'),
            'versioned': req.get_param('versionable') != 'false',
            'state': req.get_param('dsState', default='A'),
            'checksums': checksums,
            'mimetype': req.get_param('mimeType'),
            'data_ref': data_ref,
            'data': data,
        })
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
