"""
Database helpers relating to datastream relations.

Each DB helper takes an optional cursor as its final argument as transaction
control.
"""

import logging

from dgi_repo.database.utilities import check_cursor
from dgi_repo.database.utilities import DATASTREAM_RELATION_MAP
from dgi_repo.database.write.relations import (
    write_to_standard_relation_table,
    upsert_namespace,
    upsert_predicate
)

logger = logging.getLogger(__name__)


def write_relationship(namespace, predicate, subject, rdf_object, cursor=None):
    """
    Write a datastream relation to the repository.
    """
    try:
        relation_db_info = DATASTREAM_RELATION_MAP[(namespace, predicate)]
        cursor = write_to_standard_relation_table(
            relation_db_info['table'],
            relation_db_info['upsert message'],
            subject,
            rdf_object,
            cursor
        )
    except KeyError:
        cursor = upsert_namespace(namespace, cursor=cursor)
        namespace_id = cursor.fetchone()['id']
        cursor = upsert_predicate(
            {'namespace': namespace_id, 'predicate': predicate},
            cursor=cursor
        )
        predicate_id = cursor.fetchone()['id']
        cursor = write_to_general_rdf_table(predicate_id, subject, rdf_object,
                                            cursor=cursor)

    return cursor


def write_to_general_rdf_table(predicate_id, subject, rdf_object, cursor=None):
    """
    Write to the main datastream RDF table.
    """
    cursor = check_cursor(cursor)

    cursor.execute('''
        INSERT INTO datastream_relationships (
            predicate_id,
            subject,
            rdf_object
        )
        VALUES (%s, %s, %s)
        RETURNING id
    ''', (predicate_id, subject, rdf_object))

    logger.debug(
        'Upserted a datastream relation "%s" on %s as %s.',
        predicate_id,
        subject,
        rdf_object
    )

    return cursor
