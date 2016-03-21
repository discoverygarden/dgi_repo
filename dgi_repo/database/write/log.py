"""
Database helpers relating to logs.

Each DB helper takes an optional cursor as its final argument as transaction
control.
"""

import logging

from dgi_repo.database.utilities import check_cursor
from dgi_repo.database.read.log import log_id

logger = logging.getLogger(__name__)


def upsert_log(log, cursor=None):
    """
    Upsert a log in the repository.
    """
    cursor = check_cursor(cursor)

    cursor.execute('''
        INSERT INTO log (log_entry)
        VALUES (%s)
        ON CONFLICT (log_entry) DO NOTHING
        RETURNING id
    ''', (log,))

    if not cursor.rowcount:
        cursor = log_id(log, cursor)

    logger.debug('Upserted log: %s.', log)

    return cursor
