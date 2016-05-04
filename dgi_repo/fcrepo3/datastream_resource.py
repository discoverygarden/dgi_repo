"""
Class file for the implementation of the datastream resource.
"""
import logging

from psycopg2.extensions import ISOLATION_LEVEL_READ_COMMITTED

import dgi_repo.database.read.repo_objects as object_reader
import dgi_repo.database.read.datastreams as ds_reader
import dgi_repo.database.write.datastreams as ds_writer
import dgi_repo.database.delete.datastreams as ds_purger
import dgi_repo.utilities as utils
import dgi_repo.fcrepo3.utilities as fedora_utils
from dgi_repo.fcrepo3.exceptions import ObjectDoesNotExistError
from dgi_repo.fcrepo3.exceptions import DatastreamDoesNotExistError
from dgi_repo.fcrepo3 import api, foxml
from dgi_repo.database.utilities import get_connection

logger = logging.getLogger(__name__)


class DatastreamResource(api.DatastreamResource):
    """
    Provide the datastream CRUD endpoints.
    """

    def _create_ds(self, req, pid, dsid):
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
            try:
                ds_reader.datastream_from_raw(pid, dsid, cursor=cursor)
            except TypeError as e:
                raise ObjectDoesNotExistError(pid) from e
            ds_info = cursor.fetchone()
            if ds_info is not None:
                ds = dict(ds_info)
                ds['committed'] = ds['modified']
                ds['datastream'] = ds['id']
                del ds['id']
                ds_writer.upsert_old_datastream(ds, cursor=cursor)
            else:
                raise DatastreamDoesNotExistError(pid, dsid)

            self._upsert_ds(req, pid, dsid, cursor)
            logger.info('Updated DS %s on %s.', dsid, pid)
        return

    def on_delete(self, req, resp, pid, dsid):
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
            logger.info(('Deleted datastream versions for %s on %s between'
                         ' %s and %s.'), dsid, pid, start, end)
            foxml.internalize_rels(pid, dsid,
                                   req.env['wsgi.identity'].source_id,
                                   cursor=cursor)

    def _upsert_ds(self, req, pid, dsid, cursor):
        """
        Upsert a datastream.
        """
        object_info = object_reader.object_id_from_raw(
            pid, cursor=cursor).fetchone()
        if object_info is None:
            raise ObjectDoesNotExistError(pid)

        control_group = req.get_param('controlGroup', default='M')
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
            data = req.get_param('file').file
        checksums = None
        checksum = req.get_param('checksum')
        if checksum is not None:
            checksums.append({
                'checksum': checksum,
                'type': req.get_param('checksumType'),
            }),
        fedora_utils.write_ds(
            {
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
            },
            cursor=cursor
        )
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
                return None
            if asOfDateTime is not None:
                ds_info = ds_reader.datastream_as_of_time(
                    ds_info['id'],
                    utils.iso8601_to_datetime(asOfDateTime),
                    cursor=cursor
                )
                if ds_info is None:
                    return None
            return fedora_utils.datastream_to_profile(ds_info, cursor)
