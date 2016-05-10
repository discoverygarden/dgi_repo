"""
Database delete functions relating to object relations.

Each DB helper takes an optional cursor as its final argument as transaction
control.
"""

import logging

from dgi_repo.fcrepo3 import relations
from dgi_repo.database.utilities import check_cursor
from dgi_repo.database.utilities import OBJECT_RELATION_MAP
from dgi_repo.database.delete.relations import (
    delete_from_standard_relation_table)

logger = logging.getLogger(__name__)


def delete_object_relations(object_id, cursor=None):
    """
    Purge all non-DC relations on an object.
    """
    cursor = check_cursor(cursor)

    for relation_db_info in OBJECT_RELATION_MAP.values():
        # Delete from specific tables.
        cursor.execute('''
            DELETE FROM {}
            WHERE rdf_subject = %s
        '''.format(relation_db_info['table']), (object_id,))

        logger.debug('Deleted any RDF relations in %s about object %s.',
                     relation_db_info['table'], object_id)
    # Delete from general table.
    cursor.execute('''
        DELETE FROM object_relationships
        WHERE rdf_subject = %s
    ''', (object_id,))

    logger.debug(('Deleted any RDF relation about object: %s from the general'
                  ' table.'), object_id)

    return cursor


def delete_dc_relations(object_id, cursor=None):
    """
    Purge all DC relations on an object.
    """
    cursor = check_cursor(cursor)

    for predicate in relations.RELATIONS[relations.DC_NAMESPACE]:
        relation_db_info = OBJECT_RELATION_MAP[(relations.DC_NAMESPACE,
                                                predicate)]
        cursor.execute('''
            DELETE FROM {}
            WHERE rdf_subject = %s
        '''.format(relation_db_info['table']), (object_id,))

        logger.debug('Deleted any DC relations in %s about object %s.',
                     relation_db_info['table'], object_id)

    return cursor


def delete_relationship(namespace, predicate, db_id, cursor=None):
    """
    Delete an object relation from the repository.
    """
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

    logger.debug('Deleted object RDF relation with ID: %s.', db_id)

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
