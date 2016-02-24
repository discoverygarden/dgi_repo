import os
from io import BytesIO
from shutil import copyfileobj
from tempfile import NamedTemporaryFile

from dgi_repo.configuration import configuration as _configuration
from dgi_repo.database.utilities import check_cursor
from dgi_repo.database.write.datastreams import upsert_resource, upsert_mime

UPLOADED_URI = 'uploaded'
URI_MAP = {
  UPLOADED_URI: os.path.join(_configuration['data_directory'], 'uploads'),
  'datastreams': os.path.join(_configuration['data_directory'], 'datastreams')
}

for scheme, path in URI_MAP.items():
    try:
        os.makedirs(path, exist_ok=True)
    except OSError as e:
        raise RuntimeError('The path "{}" does not exist for the scheme "{}", and could not be created.'.format(path, scheme)) from e

def stash(data, destination_scheme=UPLOADED_URI, mimetype='application/octet-stream', cursor=None):
    """
    Persist data, likely in our data directory.

    Args:
        data: Either a file-like object or a (byte)string to dump into a file.
        destination_scheme: One of the keys of URI_MAP. Defaults to UPLOADED_URI.
        mimetype: The MIME-type of the file.
        cursor: An optional cursor, if we are acting as part of another
            transaction.

    Returns:
        The cursor with the resource_id of the stashed resource selected on
        success.
    """
    def stash_stream(stream):
        """
        Write the given stream to the destination.

        Args:
            stream: A file-like object to copy to the destination.

        Returns:
            The relative path to the file, inside of the destination.
        """
        destination = URI_MAP[destination_scheme]
        with stream as src, NamedTemporaryFile(dir=destination, delete=False) as dest:
            copyfileobj(src, dest)
            return os.path.relpath(dest.name, destination)

    cursor = check_cursor(cursor)
    with cursor.connection:
        try:
            name = stash_stream(data if hasattr(data, 'read') else BytesIO(data))
            uri = '{}://{}'.format(destination_scheme, name)
            upsert_resource({
              'uri': uri,
              'mime': upsert_mime(mimetype, cursor).fetchone()[0],
            }, cursor=cursor)
        except:
            if os.path.exists(name):
                os.remove(name)
            raise
        else:
            return cursor

def resolve_uri(uri):
    """
    Turn a URI back to a file path.

    Args:
        uri: The URI to transform.

    Return:
        The file path.
    """
    scheme, _, path = uri.partition('://')
    return os.path.join(URI_MAP[scheme], path)
