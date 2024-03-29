"""
Database helpers relating to repository objects.
"""

from dgi_repo.database.utilities import check_cursor
from dgi_repo import utilities


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


def namespace_info(namespace_id, cursor=None):
    """
    Query for namespace info from the repository.
    """
    cursor = check_cursor(cursor)

    cursor.execute('''
        SELECT *
        FROM pid_namespaces
        WHERE id = %s
    ''', (namespace_id,))

    return cursor


def object_id(data, cursor=None):
    """
    Query for an object ID from the repository.
    """
    cursor = check_cursor(cursor)

    cursor.execute('''
        SELECT id
        FROM objects
        WHERE objects.pid_id = %(pid_id)s AND namespace = %(namespace)s
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
        WHERE object = %(object)s AND committed = %(committed)s
    ''', data)

    return cursor


def object_info_from_raw(pid, cursor=None):
    """
    Get object info from a PID.
    """
    cursor = check_cursor(cursor)
    namespace, pid_id = utilities.break_pid(pid)

    cursor.execute('''
        SELECT objects.*
        FROM objects
            JOIN
        pid_namespaces
            ON objects.namespace = pid_namespaces.id
        WHERE objects.pid_id = %s AND pid_namespaces.namespace = %s
    ''', (pid_id, namespace))

    return cursor


def object_id_from_raw(pid, cursor=None):
    """
    Get the object database ID from a PID.
    """
    cursor = check_cursor(cursor)
    namespace, pid_id = utilities.break_pid(pid)

    cursor.execute('''
        SELECT objects.id AS id
        FROM objects
            JOIN
        pid_namespaces
            ON objects.namespace = pid_namespaces.id
        WHERE objects.pid_id = %s AND pid_namespaces.namespace = %s
    ''', (pid_id, namespace))

    return cursor
