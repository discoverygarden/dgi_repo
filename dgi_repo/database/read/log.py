"""
Database helpers relating to the log.
"""

from dgi_repo.database.utilities import check_cursor


def log_id(log, cursor=None):
    """
    Query for a log ID from the repository.
    """
    cursor = check_cursor(cursor)

    cursor.execute('''
        SELECT id
        FROM log
        WHERE log_entry = %s
    ''', (log,))

    return cursor
