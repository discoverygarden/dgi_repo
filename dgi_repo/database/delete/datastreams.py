"""
Database delete functions relating to datastreams.

Each DB helper takes an optional cursor as its final argument as transaction
control.
"""

import logging

from dgi_repo.database.utilities import check_cursor
import dgi_repo.database.read.repo_objects as object_reader
import dgi_repo.database.read.datastreams as datastream_reader
import dgi_repo.database.write.datastreams as datastream_writer

logger = logging.getLogger(__name__)


def delete_old_datastream(old_datastream_id, cursor=None):
    """
    Delete a old datastream version information from the repository.
    """
    cursor = check_cursor(cursor)

    cursor.execute('''
        DELETE FROM old_datastreams
        WHERE id = %s
    ''', (old_datastream_id,))

    logger.debug(
        'Deleted old datastream version information with ID: %s',
        old_datastream_id
    )

    return cursor


def delete_datastream_from_raw(pid, dsid, cursor=None):
    """
    Delete a datastream from the repository given a PID and DSID.
    """
    cursor = check_cursor(cursor)

    object_reader.object_id_from_raw(pid, cursor=cursor)
    datastream_reader.datastream_id(
        {
            'object': cursor.fetchone()['id'],
            'dsid': dsid,
        },
        cursor=cursor
    )
    return delete_datastream(cursor.fetchone()['id'], cursor=cursor)


def delete_datastream(datastream_id, cursor=None):
    """
    Delete a datastream from the repository.
    """
    cursor = check_cursor(cursor)

    cursor.execute('''
        DELETE FROM datastreams
        WHERE id = %s
    ''', (datastream_id,))

    logger.debug('Deleted datastream with ID: %s', datastream_id)

    return cursor


def delete_resource(resource_id, cursor=None):
    """
    Delete a resource from the repository.
    """
    cursor = check_cursor(cursor)

    cursor.execute('''
        DELETE FROM resources
        WHERE id = %s
    ''', (resource_id,))

    logger.debug('Deleted resource with ID: %s', resource_id)

    return cursor


def delete_mime(mime_id, cursor=None):
    """
    Delete a mime from the repository.
    """
    cursor = check_cursor(cursor)

    cursor.execute('''
        DELETE FROM mimes
        WHERE id = %s
    ''', (mime_id,))

    logger.debug('Deleted mime with ID: %s', mime_id)

    return cursor


def delete_checksum(checksum_id, cursor=None):
    """
    Delete a checksum from the repository.
    """
    cursor = check_cursor(cursor)

    cursor.execute('''
        DELETE FROM checksums
        WHERE id = %s
    ''', (checksum_id,))

    logger.debug('Deleted checksum with ID: %s', checksum_id)

    return cursor


def delete_datastream_versions(pid, dsid, start=None, end=None, cursor=None):
    """
    Delete versions of a datastream
    """
    cursor = check_cursor(cursor)

    datastream_reader.datastream_from_raw(pid, dsid, cursor=cursor)
    ds_info = cursor.fetchone()
    if ds_info is None:
        return cursor

    # Handle base datastream.
    if end is None and start is None:
        return delete_datastream(ds_info['id'], cursor=cursor)
    elif end is None or end > ds_info['modified']:
        # Find youngest surviving version and make it current.
        ds_replacement = datastream_reader.datastream_as_of_time(
            ds_info['id'],
            start,
            cursor,
            False
        )
        if ds_replacement is not None:
            datastream_writer.upsert_datastream(dict(ds_replacement),
                                                cursor=cursor)
            cursor.execute('''
                DELETE FROM old_datastreams
                WHERE current_datastream = %s AND committed = %s
            ''', (ds_info['id'], ds_replacement['modified']))

    # Handle old datastreams.
    if start is None:
        # Remove from dawn of time to specified end.
        cursor.execute('''
            DELETE FROM old_datastreams
            WHERE current_datastream = %s AND committed <= %s
        ''', (ds_info['id'], end))
    elif end is None:
        # Remove from specified start to end of time.
        cursor.execute('''
            DELETE FROM old_datastreams
            WHERE current_datastream = %s AND committed >= %s
        ''', (ds_info['id'], start))
    else:
        # Remove items between specified start and end times.
        cursor.execute('''
            DELETE FROM old_datastreams
            WHERE current_datastream = %s AND committed <= %s AND
                committed >= %s
        ''', (ds_info['id'], end, start))

    logger.debug('Deleted datastream versions for %s on %s between %s and %s.',
                 dsid, pid, start, end)

    return cursor
