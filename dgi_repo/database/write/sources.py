"""
Database helpers relating to sources and users.

Each DB helper takes an optional cursor as its final argument as transaction
control.
"""

import logging

from dgi_repo.database.utilities import check_cursor

logger = logging.getLogger(__name__)


def upsert_source(source, cursor=None):
    """
    Upsert a source in the repository.
    """
    from dgi_repo.database.read.sources import source_id

    cursor = check_cursor(cursor)

    cursor.execute('''
        INSERT INTO sources (source)
        VALUES (%s)
        ON CONFLICT (source) DO NOTHING
        RETURNING id
    ''', (source,))

    if not cursor.rowcount:
        cursor = source_id(source, cursor)

    logger.debug('Upserted source: %s', source)

    return cursor


def upsert_user(data, cursor=None):
    """
    Upsert a user in the repository.
    """
    from dgi_repo.database.read.sources import user_id

    cursor = check_cursor(cursor)

    cursor.execute('''
        INSERT INTO users (username, source_id)
        VALUES (%(name)s, %(source)s)
        ON CONFLICT (username, source_id) DO NOTHING
        RETURNING id
    ''', data)

    if not cursor.rowcount:
        cursor = user_id(data, cursor)

    logger.debug('Upserted user:%(name)s for source: %(source)s.', data)

    return cursor


def upsert_role(data, cursor=None):
    """
    Upsert a role in the repository.
    """
    from dgi_repo.database.read.sources import role_id

    cursor = check_cursor(cursor)

    cursor.execute('''
        INSERT INTO user_roles (role, source_id)
        VALUES (%(role)s, %(source)s)
        ON CONFLICT (role, source_id) DO NOTHING
        RETURNING id
    ''', data)

    if not cursor.rowcount:
        cursor = role_id(data, cursor)

    logger.debug('Upserted user:%(role)s for source: %(source)s.', data)

    return cursor
