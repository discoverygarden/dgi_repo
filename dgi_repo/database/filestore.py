import logging
import os
from io import BytesIO
from shutil import copyfileobj
from tempfile import NamedTemporaryFile

from psycopg2.extensions import TransactionRollbackError

from dgi_repo.configuration import configuration as _configuration
from dgi_repo.database.utilities import get_connection
from dgi_repo.database.write.datastreams import upsert_resource, upsert_mime
from dgi_repo.database.read.datastreams import resource_uri

logger = logging.getLogger(__name__)


UPLOAD_SCHEME = 'uploaded'
'''
A mapping of URI schemes to dictionaries of parameters to pass to
NamedTemporaryFile.
'''
_URI_MAP = {
    UPLOAD_SCHEME: {
        'dir': os.path.join(_configuration['data_directory'],'uploads'),
    },
    'datastream': {
        'dir': os.path.join(_configuration['data_directory'], 'datastreams'),
        'prefix': 'ds'
    }
}


for scheme, info in _URI_MAP.items():
    try:
        logger.debug('Ensuring %s exists and is both readable and writable.', info['dir'])
        os.makedirs(info['dir'], exist_ok=True)
        logger.debug('%s exists.', info['dir'])
    except OSError as e:
        raise RuntimeError('The path "%s" does not exist for the scheme "%s", and could not be created.', info['dir'], scheme) from e
    else:
        if not os.access(info['dir'], os.W_OK):
            raise RuntimeError('The path "%s" is not writable.', info['dir'])
        elif not os.access(info['dir'], os.R_OK):
            raise RuntimeError('The path "%s" is not readable.', info['dir'])


def stash(data, destination_scheme=UPLOAD_SCHEME, mimetype='application/octet-stream'):
    """
    Persist data, likely in our data directory.

    Args:
        data: Either a file-like object or a (byte)string to dump into a file.
        destination_scheme: One of the keys of URI_MAP. Defaults to UPLOADED_URI.
        mimetype: The MIME-type of the file.
        cursor: An optional cursor, if we are acting as part of another
            transaction.

    Returns:
        The resource_id of the stashed resource.
    """
    def stash_stream(stream):
        """
        Write the given stream to the destination.

        Args:
            stream: A file-like object to copy to the destination.

        Returns:
            The relative path to the file, inside of the destination.
        """
        destination = _URI_MAP[destination_scheme]
        with stream as src, NamedTemporaryFile(delete=False, **destination) as dest:
            logger.debug('Stashing data as %s.', dest.name)
            copyfileobj(src, dest)
            return os.path.relpath(dest.name, destination['dir'])

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

    name = stash_stream(streamify())
    uri = '{}://{}'.format(destination_scheme, name)
    logger.info('Stashed data as %s.', uri)
    connection = get_connection()
    try:
        with connection:
            # XXX: This _must_ happen as a separate transaction, so we know
            # that the resource is tracked when it is present in the relevant
            # directory (and so might be garbage collected).
            cursor = connection.cursor()
            cursor = upsert_mime(mimetype, cursor)
            mime_id = cursor.fetchone()[0]

            upsert_resource({
              'uri': uri,
              'mime': mime_id,
            }, cursor=cursor)
    except:
        logger.info('Cleanup up %s due to DB rollback.', name)
        os.remove(resolve_uri(uri))
        raise
    else:
        resource_id = cursor.fetchone()[0]
        logger.debug('%s got resource id %s', uri, resource_id)
        return resource_id
    finally:
        connection.close()


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
