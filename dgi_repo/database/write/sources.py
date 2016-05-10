"""
Database helpers relating to sources and users.

Each DB helper takes an optional cursor as its final argument as transaction
control.
"""

import logging

from dgi_repo.database.utilities import check_cursor
from dgi_repo.database.read.sources import source_id
from dgi_repo.database.read.sources import user_id
from dgi_repo.database.read.sources import role_id

logger = logging.getLogger(__name__)


def upsert_source(source, cursor=None):
    """
    Upsert a source in the repository.
    """
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
    cursor = check_cursor(cursor)

    cursor.execute('''
        INSERT INTO users (username, source)
        VALUES (%(name)s, %(source)s)
        ON CONFLICT (username, source) DO NOTHING
        RETURNING id
    ''', data)

    if not cursor.rowcount:
        cursor = user_id(data, cursor)

    logger.debug('Upserted user: %(name)s for source: %(source)s.', data)

    return cursor


def upsert_role(data, cursor=None):
    """
    Upsert a role in the repository.
    """
    cursor = check_cursor(cursor)

    cursor.execute('''
        INSERT INTO user_roles (role, source)
        VALUES (%(role)s, %(source)s)
        ON CONFLICT (role, source) DO NOTHING
        RETURNING id
    ''', data)

    if not cursor.rowcount:
        cursor = role_id(data, cursor)

    logger.debug('Upserted user role: %(role)s for source: %(source)s.', data)

    return cursor
