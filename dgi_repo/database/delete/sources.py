"""
Database delete functions relating to sources.

Each DB helper takes an optional cursor as its final argument as transaction
control.
"""

import logging

from dgi_repo.database.utilities import check_cursor

logger = logging.getLogger(__name__)


def delete_source(source_id, cursor=None):
    """
    Delete a source in the repository.
    """
    cursor = check_cursor(cursor)

    cursor.execute('''
        DELETE FROM sources
        WHERE id = %s
    ''', (source_id,))

    logger.debug('Deleted source with ID: %s', source_id)

    return cursor


def delete_user(user_id, cursor=None):
    """
    Delete a user in the repository.
    """
    cursor = check_cursor(cursor)

    cursor.execute('''
        DELETE FROM users
        WHERE id = %s
    ''', (user_id,))

    logger.debug('Deleted user with ID: %s', user_id)

    return cursor


def delete_role(role_id, cursor=None):
    """
    Delete a role in the repository.
    """
    cursor = check_cursor(cursor)

    cursor.execute('''
        DELETE FROM user_roles
        WHERE id = %s
    ''', (role_id,))

    logger.debug('Deleted user role with ID: %s', role_id)

    return cursor
