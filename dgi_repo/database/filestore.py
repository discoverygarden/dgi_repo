"""
Handle file storage.
"""
import logging
import os
from io import BytesIO
from shutil import copyfileobj
from tempfile import NamedTemporaryFile

from psycopg2.extensions import ISOLATION_LEVEL_READ_COMMITTED

from dgi_repo.configuration import configuration as _configuration
from dgi_repo.database.utilities import get_connection, check_cursor
from dgi_repo.database.write.datastreams import (upsert_resource, upsert_mime,
                                                 upsert_datastream)
from dgi_repo.database.read.datastreams import resource_uri
from dgi_repo.database.delete.datastreams import delete_resource
import dgi_repo.database.read.datastreams as datastream_reader

logger = logging.getLogger(__name__)

UPLOAD_SCHEME = 'uploaded'
DATASTREAM_SCHEME = 'datastream'
'''
A mapping of URI schemes to dictionaries of parameters to pass to
NamedTemporaryFile.
'''
_URI_MAP = {
    UPLOAD_SCHEME: {
        'dir': os.path.join(_configuration['data_directory'], 'uploads'),
    },
    'datastream': {
        'dir': os.path.join(_configuration['data_directory'], 'datastreams'),
        'prefix': 'ds'
    }
}


for scheme, info in _URI_MAP.items():
    try:
        logger.debug('Ensuring %s exists and is both readable and writable.',
                     info['dir'])
        os.makedirs(info['dir'], exist_ok=True)
        logger.debug('%s exists.', info['dir'])
    except OSError as e:
        message = ('The path "%s" does not exist for the scheme "%s", and'
                   ' could not be created.')
        raise RuntimeError(message, info['dir'], scheme) from e
    else:
        if not os.access(info['dir'], os.W_OK):
            raise RuntimeError('The path "%s" is not writable.', info['dir'])
        elif not os.access(info['dir'], os.R_OK):
            raise RuntimeError('The path "%s" is not readable.', info['dir'])


def stash(data, destination_scheme=UPLOAD_SCHEME,
          mimetype='application/octet-stream'):
    """
    Persist data, likely in our data directory.

    Args:
        data: Either a file-like object or a (byte)string to dump into a file.
        destination_scheme: One of URI_MAP's keys. Defaults to UPLOADED_URI.
        mimetype: The MIME-type of the file.

    Returns:
        The resource_id and URI of the stashed resource.
    """
    def streamify():
        """
        Get the "data" as a file-like object.
        """
        if hasattr(data, 'read'):
            logger.debug('Data appears file-like.')
            return data
        elif hasattr(data, 'encode'):
            logger.debug('Data appears to be an (encodable) string.')
            return BytesIO(data.encode())
        else:
            logger.debug('Unknown data type: attempting to wrap in a BytesIO.')
            return BytesIO(data)

    try:
        destination = _URI_MAP[destination_scheme]
        connection = get_connection()
        with streamify() as src, NamedTemporaryFile(delete=False,
                                                    **destination) as dest:
            name = os.path.relpath(dest.name, destination['dir'])
            uri = '{}://{}'.format(destination_scheme, name)

            with connection:
                # XXX: This _must_ happen as a separate transaction, so we know
                # that the resource is tracked when it is present in the
                # relevant directory (and so might be garbage collected).
                cursor = connection.cursor()
                cursor = upsert_mime(mimetype, cursor)
                mime_id = cursor.fetchone()[0]

                upsert_resource({
                  'uri': uri,
                  'mime': mime_id,
                }, cursor=cursor)

            logger.debug('Stashing data as %s.', dest.name)
            copyfileobj(src, dest)
    except:
        logger.exception('Attempting to delete %s (%s) due to exception.',
                         uri, dest.name)
        os.remove(dest.name)
        raise
    else:
        resource_id = cursor.fetchone()[0]
        logger.debug('%s got resource id %s', uri, resource_id)
        return resource_id, uri


def purge(*resource_ids):
    """
    Delete the specified resources.
    """
    connection = get_connection()
    for resource_id in resource_ids:
        cursor = connection.cursor()
        with connection:
            uri = datastream_reader.resource_uri(resource_id,
                                                 cursor).fetchone()[0]
            path = resolve_uri(uri)
            if not os.path.exists(path):
                logger.warning(
                    'Skipping deletion: %s (%s) does not appear to exist.',
                    uri,
                    path
                )
                continue

            logger.debug('Deleting %s (%s).', uri, path)
            os.remove(path)
            logger.debug('Deleted %s (%s).', uri, path)

            delete_resource(resource_id, cursor)
            logger.info('Resource ID %s (%s, %s) has been deleted.',
                        resource_id, uri, path)


def resolve_uri(uri):
    """
    Turn a URI back to a file path.

    Args:
        uri: The URI to transform.

    Return:
        The file path.
    """
    scheme, _, path = uri.partition('://')
    return os.path.join(_URI_MAP[scheme]['dir'], path)


def uri_size(uri):
    """
    Get the size of a resource.

    Args:
        uri: The URI to szie.

    Return:
        The file size.
    """
    return os.path.getsize(resolve_uri(uri))


def create_datastream_from_data(datastream_data, data, mime=None, cursor=None):
    """
    Create a datastream from bytes, file or string.
    """
    cursor = check_cursor(cursor, ISOLATION_LEVEL_READ_COMMITTED)

    datastream_data['resource'] = stash(
        data, DATASTREAM_SCHEME, mime)[0]

    _create_datastream_from_filestore(datastream_data, cursor)

    return cursor


def create_datastream_from_upload(datastream_data, upload_uri, cursor=None):
    """
    Create a datastream from a resource.
    """
    cursor = check_cursor(cursor, ISOLATION_LEVEL_READ_COMMITTED)

    datastream_reader.resource_from_uri(upload_uri, cursor)
    mime_id = cursor.fetchone()['mime_id']
    datastream_reader.mime(mime_id, cursor)
    mime = cursor.fetchone()['mime']

    with open(resolve_uri(upload_uri), 'rb') as data:
        create_datastream_from_data(datastream_data, data, mime, cursor)

    return cursor


def _create_datastream_from_filestore(datastream_data, cursor=None):
    """
    Create datastream removing the file if something goes wrong.
    """
    cursor = check_cursor(cursor, ISOLATION_LEVEL_READ_COMMITTED)

    try:
        upsert_datastream(datastream_data, cursor)
    except Exception as e:
        purge(datastream_data['resource'])
        raise e
