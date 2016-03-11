"""
Database helpers relating to datastreams.
"""

from dgi_repo.database.utilities import check_cursor


def datastream(data, cursor=None):
    """
    Query for a datastream record from the repository.
    """
    cursor = check_cursor(cursor)

    cursor.execute('''
        SELECT *
        FROM datastreams
        WHERE object_id = %(object)s AND dsid = %(dsid)s
    ''', data)

    return cursor


def datastreams(object_id, cursor=None):
    """
    Query for all datastreams on an object.
    """
    cursor = check_cursor(cursor)

    cursor.execute('''
        SELECT *
        FROM datastreams
        WHERE object_id = %s
    ''', (object_id,))

    return cursor


def datastream_id(data, cursor=None):
    """
    Query for a datastream database ID from the repository.
    """
    cursor = check_cursor(cursor)

    cursor.execute('''
        SELECT id
        FROM datastreams
        WHERE object_id = %(object)s AND dsid = %(dsid)s
    ''', data)

    return cursor


def resource_id(uri, cursor=None):
    """
    Query for a resource ID from the repository.
    """
    cursor = check_cursor(cursor)

    cursor.execute('''
        SELECT id
        FROM resources
        WHERE uri = %s
    ''', (uri,))

    return cursor


def resource(id, cursor=None):
    """
    Query for resource information from the repository.
    """
    cursor = check_cursor(cursor)

    cursor.execute('''
        SELECT *
        FROM resources
        WHERE id = %s
    ''', (id,))

    return cursor


def resource_uri(id, cursor=None):
    """
    Query for a resource URI from the repository.
    """
    cursor = check_cursor(cursor)

    cursor.execute('''
        SELECT uri
        FROM resources
        WHERE id = %s
    ''', (id,))

    return cursor


def mime(mime_id, cursor=None):
    """
    Query for mime information from the repository.
    """
    cursor = check_cursor(cursor)

    cursor.execute('''
        SELECT *
        FROM mimes
        WHERE id = %s
    ''', (mime_id,))

    return cursor


def mime_id(mime, cursor=None):
    """
    Query for a mime ID from the repository.
    """
    cursor = check_cursor(cursor)

    cursor.execute('''
        SELECT id
        FROM mimes
        WHERE mime = %s
    ''', (mime,))

    return cursor


def checksum_id(resource_id, cursor=None):
    """
    Query for a checksum record from the repository.
    """
    cursor = check_cursor(cursor)

    cursor.execute('''
        SELECT id
        FROM checksums
        WHERE uri = %s
    ''', (resource_id,))

    return cursor


def checksums(resource_id, cursor=None):
    """
    Query for all checksums on a resource from the repository.
    """
    cursor = check_cursor(cursor)

    cursor.execute('''
        SELECT *
        FROM checksums
        WHERE uri = %s
    ''', (resource_id,))

    return cursor


def old_datastreams(ds_db_id, cursor=None):
    """
    Query for old versions of a datastream.
    """
    cursor = check_cursor(cursor)

    cursor.execute('''
        SELECT *
        FROM old_datastreams
        WHERE current_datastream = %s
    ''', (ds_db_id,))

    return cursor


def old_datastream_id(data, cursor=None):
    """
    Query for an old datastream ID from the repository.
    """
    cursor = check_cursor(cursor)

    cursor.execute('''
        SELECT id
        FROM old_datastreams
        WHERE current_datastream = %(datastream)s AND committed = %(committed)s
    ''', data)

    return cursor
