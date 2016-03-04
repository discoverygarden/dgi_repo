"""
Database delete functions relating to datastreams.

Each DB helper takes an optional cursor as its final argument as transaction
control.
"""

import logging

from dgi_repo.database.utilities import check_cursor

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
