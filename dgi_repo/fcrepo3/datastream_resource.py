"""
Class file for the implementation of the datastream resource.
"""
import logging

from psycopg2.extensions import ISOLATION_LEVEL_READ_COMMITTED

import dgi_repo.database.read.repo_objects as object_reader
import dgi_repo.database.delete.datastreams as ds_purger
import dgi_repo.database.read.datastreams as ds_reader
from dgi_repo.fcrepo3.utilities import resolve_log, create_ds
from dgi_repo.fcrepo3 import api
from dgi_repo.database.utilities import get_connection
from dgi_repo.database import filestore

logger = logging.getLogger(__name__)


class DatastreamResource(api.DatastreamResource):
    """
    Provide the datastream CRUD endpoints.
    """

    def on_post(self, req, resp, pid, dsid):
        """
        Persist the new datastream.
        """
        super().on_post(req, resp, pid, dsid)
        with get_connection(ISOLATION_LEVEL_READ_COMMITTED) as conn:
            with conn.cursor() as cursor:
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
                object_reader.object_id_from_raw(pid, cursor=cursor)
                create_ds(
                    {
                        'dsid': dsid,
                        'object': cursor.fetchone()['id'],
                        'log': resolve_log(req, cursor),
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
                logger.info('Created DS %s on %s.', dsid, pid)

    def on_put(self, req, resp, pid, dsid):
        """
        Commit the modification to the datastream.

        @TODO: commit DS.
        @TODO: create old versions.
        """
        super().on_put(req, resp, pid, dsid)
        with get_connection() as conn:
            with conn.cursor() as cursor:
                log = resolve_log(req, cursor)
                logger.info('Updated DS %s on %s.', dsid, pid)

    def on_delete(self, req, resp, pid, dsid):
        """
        Purge the datastream (or range of versions).

        @TODO: handle startDT/endDT
        @TODO: handle logMessage when audit is dealt with.
        """
        super().on_delete(req, resp, pid, dsid)
        with get_connection() as conn:
            with conn.cursor() as cursor:
                ds_purger.delete_datastream_from_raw(pid, dsid, cursor=cursor)
                logger.info('Purged DS %s on %s.', dsid, pid)

    def _get_datastream_info(self, pid, dsid, asOfDateTime=None, **kwargs):
        """
        Get the ds* values in a dict, to build the datastream profile.

        @TODO: handle as of date time.
        """
        with get_connection() as conn:
            with conn.cursor() as cursor:
                ds_reader.datastream_from_raw(pid, dsid, cursor=cursor)
                ds_info = cursor.fetchone()
                if ds_info is None:
                    return None
                versionable = 'true' if ds_info['versioned'] else 'false'
                location = None
                location_type = 'INTERNAL_ID'
                mime = None
                checksum = 'none'
                checksum_type = 'DISABLED'
                size = None
                if ds_info['resource'] is not None:
                    ds_reader.resource(ds_info['resource'], cursor=cursor)
                    resource_info = cursor.fetchone()
                    if resource_info is not None:
                        location = resource_info['uri']
                        if ds_info['control_group'] != 'R':
                            size = filestore.uri_size(resource_info['uri'])
                        else:
                            location_type = 'URL'

                        ds_reader.mime(resource_info['mime'], cursor=cursor)
                        mime = cursor.fetchone()['mime']

                        ds_reader.checksums(ds_info['resource'], cursor=cursor)
                        checksum_info = cursor.fetchone()
                        if checksum_info is not None:
                            checksum = checksum_info['checksum']
                            checksum_type = checksum_info['type']
                            cursor.fetchall()
                return {
                    'dsLabel': ds_info['label'],
                    'dsCreateDate': ds_info['modified'].isoformat(),
                    'dsState': ds_info['state'],
                    'dsMime': mime,
                    'dsConrolGroup': ds_info['control_group'],
                    'dsVersionable': versionable,
                    'dsChecksumType': checksum_type,
                    'dsChecksum': checksum,
                    'dsSize': size,
                    'dsLocation': location,
                    'dsLocationType': location_type,
                }
