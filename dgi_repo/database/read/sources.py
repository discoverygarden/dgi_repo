"""
Database helpers relating to sources and users.
"""

from dgi_repo.database.utilities import check_cursor


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
        WHERE name = %(name)s AND source = %(source)s
    ''', data)

    return cursor


def user(user_id, cursor=None):
    """
    Query for user information from the repository.
    """
    cursor = check_cursor(cursor)

    cursor.execute('''
        SELECT *
        FROM users
        WHERE id = %s
    ''', (user_id,))

    return cursor


def role_id(data, cursor=None):
    """
    Query for a role ID from the repository.
    """
    cursor = check_cursor(cursor)

    cursor.execute('''
        SELECT id
        FROM user_roles
        WHERE role = %(role)s AND source = %(source)s
    ''', data)

    return cursor


def user_id_from_raw(source, user, cursor=None):
    """
    Query for a user ID from the repository given a source and user.
    """
    cursor = check_cursor(cursor)

    cursor.execute('''
        SELECT u.id
        FROM
            users u
                JOIN
            sources s
                ON u.source = s.id
        WHERE u.name = %s AND s.source = %s
    ''', (user, source))

    return cursor


def source_and_user_from_raw(source, user, cursor=None):
    """
    Query for a source and user ID from the repository given a source and user.
    """
    cursor = check_cursor(cursor)

    cursor.execute('''
        SELECT u.id AS user_id, s.id AS source_id
        FROM
            users u
                JOIN
            sources s
                ON u.source = s.id
        WHERE u.name = %s AND s.source = %s
    ''', (user, source))

    return cursor
