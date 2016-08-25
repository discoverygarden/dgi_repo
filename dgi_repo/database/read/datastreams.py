"""
Database helpers relating to datastreams.
"""

from dgi_repo.database.utilities import check_cursor
from dgi_repo import utilities


def datastream(data, cursor=None):
    """
    Query for a datastream record from the repository.
    """
    cursor = check_cursor(cursor)

    cursor.execute('''
        SELECT *
        FROM datastreams
        WHERE object = %(object)s AND dsid = %(dsid)s
    ''', data)

    return cursor


def datastream_info(ds_db_id, cursor=None):
    """
    Query for a datastream record from the repository.
    """
    cursor = check_cursor(cursor)

    cursor.execute('''
        SELECT *
        FROM datastreams
        WHERE id = %s
    ''', (ds_db_id,))

    return cursor


def datastream_from_raw(pid, dsid, cursor=None):
    """
    Query for a datastream record from the repository given a PID and DSID.
    """
    cursor = check_cursor(cursor)
    namespace, pid_id = utilities.break_pid(pid)

    cursor.execute('''
        SELECT datastreams.*
        FROM datastreams
            JOIN
        objects
            ON datastreams.object = objects.id
            JOIN
        pid_namespaces
            ON objects.namespace = pid_namespaces.id
        WHERE objects.pid_id = %s AND pid_namespaces.namespace = %s
            AND datastreams.dsid = %s
    ''', (pid_id, namespace, dsid))

    return cursor


def datastreams(object_id, cursor=None):
    """
    Query for all datastreams on an object.
    """
    cursor = check_cursor(cursor)

    cursor.execute('''
        SELECT *
        FROM datastreams
        WHERE object = %s
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
        WHERE object = %(object)s AND dsid = %(dsid)s
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


def resource_from_uri(uri, cursor=None):
    """
    Query for a resource from the repository using the URI.
    """
    cursor = check_cursor(cursor)

    cursor.execute('''
        SELECT *
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


def checksum_ids(resource_id, cursor=None):
    """
    Query for checksum IDs from the repository.
    """
    cursor = check_cursor(cursor)

    cursor.execute('''
        SELECT id
        FROM checksums
        WHERE resource = %s
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
        WHERE resource = %s
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
        WHERE datastream = %s
        ORDER BY committed
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
        WHERE datastream = %(datastream)s AND committed = %(committed)s
    ''', data)

    return cursor


def old_datastream_as_of_time(ds_db_id, time, cursor=None):
    """
    Query for an old datastream from the repository at a given time.
    """
    cursor = check_cursor(cursor)

    cursor.execute('''
        SELECT *
        FROM old_datastreams
        WHERE datastream = %s AND committed <= %s
        ORDER BY committed DESC
        LIMIT 1
    ''', (ds_db_id, time))

    return cursor


def datastream_as_of_time(ds_db_id, time, cursor, inclusive=True):
    """
    Get a datastream as it would have been at a time.
    """

    datastream_info(ds_db_id, cursor=cursor)
    ds_info = cursor.fetchone()
    # Fall out if current version is asked for.
    if ds_info['modified'] <= time and inclusive:
        return ds_info
    old_datastream_as_of_time(ds_db_id, time, cursor=cursor)
    old_ds_info = cursor.fetchone()
    if old_ds_info is not None:
        ds_replacement = ds_info.copy()
        ds_replacement.update(old_ds_info)
        ds_replacement['modified'] = old_ds_info['committed']
        ds_replacement['id'] = ds_db_id
        ds_replacement['object'] = ds_info['object']
        return ds_replacement

    return None


def mime_from_resource(resource_id, cursor=None):
    """
    Get the mime info given a resource
    """
    cursor = check_cursor(cursor)

    cursor.execute('''
        SELECT m.*
        FROM mimes m
            JOIN
        resources r
            on m.id = r.mime
        WHERE r.id = %s
    ''', (resource_id,))

    return cursor
