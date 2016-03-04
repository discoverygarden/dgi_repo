"""
Database delete functions relating to logs.

Each DB helper takes an optional cursor as its final argument as transaction
control.
"""

import logging

from dgi_repo.database.utilities import check_cursor

logger = logging.getLogger(__name__)


def delete_log(log_id, cursor=None):
    """
    Delete a log from the repository.
    """
    cursor = check_cursor(cursor)

    cursor.execute('''
        DELETE FROM log
        WHERE id = %s
    ''', (log_id,))

    logger.debug('Deleted log with ID: %s', log_id)

    return cursor
