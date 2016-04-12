"""
Database delete functions relating to datastream relations.

Each DB helper takes an optional cursor as its final argument as transaction
control.
"""

import logging

from dgi_repo.database.utilities import check_cursor
from dgi_repo.database.utilities import DATASTREAM_RELATION_MAP
from dgi_repo.database.delete.relations import (
    delete_from_standard_relation_table)

logger = logging.getLogger(__name__)


def delete_datastream_relations(datastream_id, cursor=None):
    """
    Purge all relations on a datastream.
    todo: implement
    """
    cursor = check_cursor(cursor)

    return cursor


def delete_relationship(namespace, predicate, db_id, cursor=None):
    """
    Delete a datastream relation from the repository.
    """
    try:
        relation_db_info = DATASTREAM_RELATION_MAP[(namespace, predicate)]
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
    Delete from the general datastream RDF table.
    """
    cursor = check_cursor(cursor)

    cursor.execute('''
        DELETE FROM datastream_relationships
        WHERE id = %s
    ''', (db_id,))

    logger.debug('Deleted datastream RDF relation with ID: %s', db_id)

    return cursor
