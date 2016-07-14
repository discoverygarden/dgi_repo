"""
Handle file storage.
"""
import logging
import os
from io import BytesIO
from shutil import copyfileobj
from tempfile import NamedTemporaryFile

from psycopg2.extensions import ISOLATION_LEVEL_READ_COMMITTED

import dgi_repo.database.write.datastreams as datastream_writer
import dgi_repo.database.read.datastreams as datastream_reader
import dgi_repo.database.delete.datastreams as datastream_purger
from dgi_repo.utilities import checksum_file
from dgi_repo.database.utilities import get_connection, check_cursor
from dgi_repo.configuration import configuration as _config
from dgi_repo.database.delete.datastreams import delete_resource

logger = logging.getLogger(__name__)

UPLOAD_SCHEME = 'uploaded'
DATASTREAM_SCHEME = 'datastream'
'''
A mapping of URI schemes to dictionaries of parameters to pass to
NamedTemporaryFile.
'''
_URI_MAP = {
    UPLOAD_SCHEME: {
        'dir': os.path.join(_config['data_directory'], 'uploads'),
    },
    DATASTREAM_SCHEME: {
        'dir': os.path.join(_config['data_directory'], 'datastreams'),
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
            Please make all use of it before passing to stash as the stashed
            copy will not be updated. If data is a file-like object it will be
            closed.
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
            # A readable item may not have an exit, so lets read and wrap it.
            if not hasattr(data, '__exit__'):
                return BytesIO(data.read())
            return data
        elif hasattr(data, 'encode'):
            logger.debug('Data appears to be an (encodable) string.')
            return BytesIO(data.encode())
        else:
            logger.debug('Unknown data type: attempting to wrap in a BytesIO.')
            return BytesIO(data)

    destination = _URI_MAP[destination_scheme]
    connection = get_connection()
    with NamedTemporaryFile(delete=False, **destination) as dest:
        try:
            name = os.path.relpath(dest.name, destination['dir'])
            uri = '{}://{}'.format(destination_scheme, name)
            with streamify() as src:
                with connection:
                    # XXX: This _must_ happen as a separate transaction, so we
                    # know that the resource is tracked when it is present in
                    # the relevant directory (and so might be garbage
                    # collected).
                    cursor = connection.cursor()
                    cursor = datastream_writer.upsert_mime(mimetype, cursor)
                    mime_id = cursor.fetchone()[0]

                    datastream_writer.upsert_resource({
                        'uri': uri,
                        'mime': mime_id,
                    }, cursor=cursor)

                logger.debug('Stashing data as %s.', dest.name)
                copyfileobj(src, dest)
                # This is our Raison d'etre, make sure the file is out.
                dest.flush()
                os.fsync(dest.fileno())
        except:
            logger.exception('Attempting to delete %s (%s) due to exception.',
                             uri, dest.name)
            os.remove(dest.name)
            raise
        else:
            resource_id = cursor.fetchone()[0]
            logger.debug('%s got resource id %s', uri, resource_id)
            return resource_id, uri
    return


def purge(*resource_ids):
    """
    Helper to handle single IDs.
    """
    purge_all(resource_ids)


def purge_all(resource_ids):
    """
    Delete the specified resources.
    """
    connection = get_connection()
    for resource_id in resource_ids:
        cursor = connection.cursor()
        with connection:
            uri = datastream_reader.resource_uri(resource_id,
                                                 cursor).fetchone()[0]
            try:
                path = resolve_uri(uri)
            except KeyError:
                path = '(non-local/unresolvable URI)'
                logger.debug('Unknown schema for %s.', uri)
            else:
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
        uri: The URI to size.

    Return:
        The file size.
    """
    return os.path.getsize(resolve_uri(uri))


def create_datastream_from_data(datastream_data, data, mime=None,
                                checksums=None, old=False, cursor=None):
    """
    Create a datastream from bytes, file or string.
    """
    cursor = check_cursor(cursor, ISOLATION_LEVEL_READ_COMMITTED)

    datastream_data['resource'] = stash(data, DATASTREAM_SCHEME, mime)[0]
    update_checksums(datastream_data['resource'], checksums, cursor=cursor)

    _create_datastream_from_filestore(datastream_data, old, cursor=cursor)

    return cursor


def create_datastream_from_upload(datastream_data, upload_uri, mime=None,
                                  checksums=None, old=False, cursor=None):
    """
    Create a datastream from a resource.
    """
    cursor = check_cursor(cursor, ISOLATION_LEVEL_READ_COMMITTED)

    datastream_reader.resource_from_uri(upload_uri, cursor=cursor)

    with open(resolve_uri(upload_uri), 'rb') as data:
        create_datastream_from_data(datastream_data, data, mime, checksums,
                                    old, cursor=cursor)

    return cursor


def _create_datastream_from_filestore(datastream_data, old=False, cursor=None):
    """
    Create datastream removing the file if something goes wrong.
    """
    cursor = check_cursor(cursor, ISOLATION_LEVEL_READ_COMMITTED)

    try:
        if old:
            datastream_writer.upsert_old_datastream(datastream_data,
                                                    cursor=cursor)
        else:
            datastream_writer.upsert_datastream(datastream_data,
                                                cursor=cursor)
    except Exception as e:
        purge(datastream_data['resource'])
        raise e

    return cursor


def update_checksums(resource, checksums, cursor=None):
    """
    Bring a resource's checksums up to date.

    Raises:
        ValueError: On checksum mismatch.
    """
    # Fedora hash types mapped to the names that hashlib uses.
    hash_type_map = {
        'MD5': 'md5',
        'SHA-1': 'sha1',
        'SHA-256': 'sha256',
        'SHA-384': 'sha384',
        'SHA-512': 'sha512'
    }

    if checksums is not None:
        old_checksums = datastream_reader.checksums(resource, cursor=cursor
                                                    ).fetchall()
        for checksum in checksums:
            # Resolve default checksum.
            if checksum['type'] == 'DEFAULT':
                checksum['type'] = _config['default_hash_algorithm']

            # Checksums can be disabled.
            if checksum['type'] == 'DISABLED':
                for old_checksum in old_checksums:
                    datastream_purger.delete_checksum(old_checksum['id'],
                                                      cursor=cursor)
                continue

            # Only set or validate checksums if they have changed.
            update_checksum = True
            for old_checksum in old_checksums:
                # If we get checksums with no type it is the old.
                if not checksum['type']:
                    checksum['type'] = old_checksum['type']
                if (old_checksum['type'] == checksum['type'] and
                        old_checksum['checksum'] == checksum['checksum']):
                    update_checksum = False

            if update_checksum:
                checksum['resource'] = resource
                file_path = resolve_uri(datastream_reader.resource(
                    resource,
                    cursor=cursor).fetchone()['uri'])
                checksum_value = checksum_file(
                    file_path,
                    hash_type_map[checksum['type']]
                )

                if not checksum['checksum']:
                    # Set checksum.
                    checksum['checksum'] = checksum_value
                elif checksum_value != checksum['checksum']:
                    raise ValueError('Checksum mismatch.')

                datastream_writer.upsert_checksum(checksum, cursor=cursor)
                cursor.fetchone()
