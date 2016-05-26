"""
Utility functions to assist with the Fedora 3 spoofing.
"""
import logging

import requests
from psycopg2.extensions import ISOLATION_LEVEL_READ_COMMITTED
import pytz

import dgi_repo.database.write.log as log_writer
import dgi_repo.database.write.datastreams as ds_writer
import dgi_repo.database.read.datastreams as ds_reader
import dgi_repo.database.filestore as filestore
from dgi_repo.database.utilities import check_cursor
from dgi_repo.configuration import configuration as _config
from dgi_repo import utilities as utils

logger = logging.getLogger(__name__)

RDF_NAMESPACE = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'

FEDORA_URI_PREFIX = 'info:fedora/'


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
        if ds['control_group'] == 'R':
            # Data will remain external.
            ds_writer.upsert_mime(ds['mimetype'], cursor=cursor)
            ds_writer.upsert_resource(
                {
                    'uri': ds['data_ref']['REF'],
                    'mime': cursor.fetchone()['id'],
                },
                cursor=cursor)
            ds['resource'] = cursor.fetchone()['id']
            ds_writer.upsert_datastream(ds, cursor=cursor)
        elif ds['data_ref']['REF'].startswith(filestore.UPLOAD_SCHEME):
            # Data has been uploaded.
            filestore.create_datastream_from_upload(
                ds,
                ds['data_ref']['REF'],
                mime=ds['mimetype'],
                checksums=ds['checksums'],
                old=old,
                cursor=cursor
            )
        else:
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
    else:
        ds_writer.upsert_datastream(ds, cursor=cursor)

    return cursor


def datastream_to_profile(ds_info, cursor, version=0):
    """
    Get a datastream profile dict from a DB DS dict.
    """
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
        'dsCreateDate': format_date(ds_info['modified']),
        'dsState': ds_info['state'],
        'dsMime': mime,
        'dsControlGroup': ds_info['control_group'],
        'dsVersionable': versionable,
        'dsVersionID': '{}.{}'.format(ds_info['dsid'], version),
        'dsChecksumType': checksum_type,
        'dsChecksum': checksum,
        'dsSize': size,
        'dsLocation': location,
        'dsLocationType': location_type,
    }

def format_date(dt):
    """
    Format a datetime into Zulu time, with terminal "Z".
    """
    return dt.astimezone(pytz.utc).strftime('%Y-%m-%dT%H:%M:%S.%fZ')


def is_fedora_uri(candidate):
    """
    Check if a string is a Fedora URI.

    @XXX the check is incomplete; it may have false positives.
    """
    return candidate.startswith(FEDORA_URI_PREFIX)


def cut_fedora_prefix(uri):
    """
    Cut the Fedora URI prefix from a URI.
    """
    return uri[len(FEDORA_URI_PREFIX):]


def pid_from_fedora_uri(uri):
    """
    Retrieve a PID from a Fedora URI.
    """
    if not is_fedora_uri(uri):
        return None
    stripped_uri = cut_fedora_prefix(uri)
    try:
        return stripped_uri[:stripped_uri.index('/')]
    except ValueError:
        return stripped_uri


def dsid_from_fedora_uri(uri):
    """
    Retrieve a PID from a Fedora URI.
    """
    if not is_fedora_uri(uri):
        return None
    stripped_uri = cut_fedora_prefix(uri)
    if '/' in stripped_uri:
        return stripped_uri[stripped_uri.find('/') + 1:]
    else:
        return False
