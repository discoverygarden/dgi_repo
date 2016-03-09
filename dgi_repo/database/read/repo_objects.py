"""
Database helpers relating to repository objects.
"""

import logging

from dgi_repo.database.utilities import check_cursor

logger = logging.getLogger(__name__)


def object_info(db_id, cursor=None):
    """
    Query for an object's information from the repository.
    """
    cursor = check_cursor(cursor)

    cursor.execute('''
        SELECT *
        FROM objects
        WHERE id = %s
    ''', (db_id,))

    return cursor


def object_id(data, cursor=None):
    """
    Query for an object ID from the repository.
    """
    cursor = check_cursor(cursor)

    cursor.execute('''
        SELECT id
        FROM objects
        WHERE objects.pid_id = '%(pid_id)s' AND namespace = %(namespace)s
    ''', data)

    return cursor


def namespace_id(namespace, cursor=None):
    """
    Query for a namespace ID from the repository.
    """
    cursor = check_cursor(cursor)

    cursor.execute('''
        SELECT id
        FROM pid_namespaces
        WHERE namespace = %s
    ''', (namespace,))

    return cursor


def old_object_id(data, cursor=None):
    """
    Query for an old object ID from the repository.
    """
    cursor = check_cursor(cursor)

    cursor.execute('''
        SELECT id
        FROM old_objects
        WHERE current_object = %(object)s AND committed = %(committed)s
    ''', data)

    return cursor
