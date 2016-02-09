"""
Database helpers relating to sources and users.
"""

import logging

from dgi_repo.database.utilities import check_cursor

logger = logging.getLogger(__name__)


def source_id(source, cursor=None):
    """
    Query for a source ID from the repository.
    """
    cursor = check_cursor(cursor)

    cursor.execute('''
        SELECT id
        FROM sources
        WHERE source = %s
    ''', (source,))

    return cursor


def user_id(data, cursor=None):
    """
    Query for a user ID from the repository.
    """
    cursor = check_cursor(cursor)

    cursor.execute('''
        SELECT id
        FROM users
        WHERE username = %(name)s AND source_id = %(source)s
    ''', data)

    return cursor


def role_id(data, cursor=None):
    """
    Query for a role ID from the repository.
    """
    cursor = check_cursor(cursor)

    cursor.execute('''
        SELECT id
        FROM user_roles
        WHERE role = %(role)s AND source_id = %(source)s
    ''', data)

    return cursor
