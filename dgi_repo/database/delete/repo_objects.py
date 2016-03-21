"""
Database delete functions relating to objects.

Each DB helper takes an optional cursor as its final argument as transaction
control.
"""

import logging

from dgi_repo.database.utilities import check_cursor

logger = logging.getLogger(__name__)


def delete_object(object_id, cursor=None):
    """
    Delete a object from the repository.
    """
    cursor = check_cursor(cursor)

    cursor.execute('''
        DELETE FROM objects
        WHERE id = %s
    ''', (object_id,))

    logger.debug('Deleted object with ID: %s', object_id)

    return cursor


def delete_old_object(old_object_id, cursor=None):
    """
    Delete old object version information from the repository.
    """
    cursor = check_cursor(cursor)

    cursor.execute('''
        DELETE FROM old_objects
        WHERE id = %s
    ''', (old_object_id,))

    logger.debug('Deleted old object version information with ID: %s',
                 old_object_id)

    return cursor


def delete_namespace(namespace_id, cursor=None):
    """
    Delete a namespace from the repository.
    """
    cursor = check_cursor(cursor)

    cursor.execute('''
        DELETE FROM pid_namespaces
        WHERE id = %s
    ''', (namespace_id,))

    logger.debug('Deleted namespace with ID: %s', namespace_id)

    return cursor
