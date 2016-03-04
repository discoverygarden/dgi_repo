"""
Database delete functions relating to object relations.

Each DB helper takes an optional cursor as its final argument as transaction
control.
"""

import logging

from dgi_repo.database.utilities import check_cursor

logger = logging.getLogger(__name__)


def delete_relationship(namespace, predicate, db_id, cursor=None):
    """
    Delete an object relation from the repository.
    """
    from dgi_repo.database.utilities import OBJECT_RELATION_MAP
    from dgi_repo.database.delete.relations import delete_from_standard_relation_table

    try:
        relation_db_info = OBJECT_RELATION_MAP[(namespace, predicate)]
        cursor = delete_from_standard_relation_table(
            relation_db_info['table'],
            relation_db_info['delete message'],
            db_id,
            cursor
        )
    except KeyError:
        cursor = delete_from_general_rdf_table(db_id, cursor)

    return cursor


def delete_from_general_rdf_table(db_id, cursor=None):
    """
    Delete from the general object RDF table.
    """
    cursor = check_cursor(cursor)

    cursor.execute('''
        DELETE FROM object_relationships
        WHERE id = %s
    ''', (db_id,))

    logger.debug('Deleted object RDF relation with ID: %s', db_id)

    return cursor


def delete_sequence_number(db_id, cursor=None):
    """
    Delete an is sequence number of object relation from the repository.
    """
    cursor = check_cursor(cursor)

    cursor.execute('''
        DELETE FROM is_sequence_number_of
        WHERE id = %s
    ''', (db_id,))

    logger.debug(
        'Deleted an "is sequence number of" relation with ID: %s.',
        db_id
    )

    return cursor
