"""
Utility functions to assist with the Fedora 3 spoofing.
"""
import logging

import falcon
import requests
from psycopg2.extensions import ISOLATION_LEVEL_READ_COMMITTED

import dgi_repo.database.write.log as log_writer
from dgi_repo.database.utilities import check_cursor
import dgi_repo.database.write.datastreams as datastream_writer
from dgi_repo.configuration import configuration as _config
import dgi_repo.database.filestore as filestore
from dgi_repo import utilities as utils

logger = logging.getLogger(__name__)


def resolve_log(req, cursor):
    """
    Get the DB log from the req.
    """
    raw_log = req.get_param('logMessage')
    if raw_log:
        log_writer.upsert_log(raw_log, cursor=cursor)
        log = cursor.fetchone()['id']
    else:
        log = None
    return log


def write_ds(ds, old=False, cursor=None):
    """
    Create a datastream on the current object.
    """
    cursor = check_cursor(cursor, ISOLATION_LEVEL_READ_COMMITTED)

    if ds['data'] is not None:
        # We already have data.
        filestore.create_datastream_from_data(
            ds,
            ds['data'],
            mime=ds['mimetype'],
            checksums=ds['checksums'],
            old=old,
            cursor=cursor
        )
    elif ds['data_ref'] is not None:
        if ds['data_ref']['TYPE'] == 'URL':
            # Data will remain external.
            if ds['control_group'] == 'R':
                datastream_writer.upsert_mime(ds['mimetype'],
                                              cursor=cursor)
                datastream_writer.upsert_resource(
                    {
                        'uri': ds['data_ref']['REF'],
                        'mime': cursor.fetchone()['id'],
                    },
                    cursor=cursor)
                ds['resource'] = cursor.fetchone()['id']
                datastream_writer.upsert_datastream(ds,
                                                    cursor=cursor)
            else:
                # Data has been uploaded.
                filestore.create_datastream_from_upload(
                    ds,
                    ds['data_ref']['REF'],
                    mime=ds['mimetype'],
                    checksums=ds['checksums'],
                    old=old,
                    cursor=cursor
                )
        elif ds['data_ref']['TYPE'] == 'INTERNAL_ID':
            # We need to fetch data.
            ds_resp = requests.get(
                ds['data_ref']['REF'], stream=True
            )
            # @XXX: we should be able to avoid creating this file by
            # wrapping the raw attribute on the response to decode on read.
            ds_file = utils.SpooledTemporaryFile()
            for chunk in ds_resp.iter_content(
                    _config['download_chunk_size']):
                ds_file.write(chunk)
            ds_file.seek(0)

            filestore.create_datastream_from_data(
                ds,
                ds_file,
                mime=ds['mimetype'],
                checksums=ds['checksums'],
                old=old,
                cursor=cursor
            )

    return cursor


def send_object_404(pid, resp):
    """
    Send a Fedora like 404 when objects don't exist.
    """
    resp.content_type = 'text/plain'
    logger.info('Object not found in low-level storage: %s', pid)
    resp.body = 'Object not found in low-level storage: {}'.format(pid)
    raise falcon.HTTPNotFound()
