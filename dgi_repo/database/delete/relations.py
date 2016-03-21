"""
Database delete functions relating to relations.

Each DB helper takes an optional cursor as its final argument as transaction
control.
"""

import logging

from dgi_repo.database.utilities import check_cursor

logger = logging.getLogger(__name__)


def delete_namespace(namespace_id, cursor=None):
    """
    Delete an RDF namespace from the repository.
    """
    cursor = check_cursor(cursor)

    cursor.execute('''
        DELETE FROM rdf_namespaces
        WHERE id = %s
    ''', (namespace_id,))

    logger.debug('Deleted RDF namespace with ID: %s', namespace_id)

    return cursor


def delete_predicate(predicate_id, cursor=None):
    """
    Delete a predicate from the repository.
    """
    cursor = check_cursor(cursor)

    cursor.execute('''
        DELETE FROM predicates
        WHERE id = %s
    ''', (predicate_id,))

    logger.debug('Deleted predicate with ID: %s', predicate_id)

    return cursor


def delete_from_standard_relation_table(table, log_message, db_id,
                                        cursor=None):
    """
    Delete from a table that uses the standard relation design.
    """
    cursor = check_cursor(cursor)

    cursor.execute('''
        DELETE FROM {}
        WHERE id = %s
    '''.format(table), (db_id,))

    logger.debug(log_message, db_id)

    return cursor
