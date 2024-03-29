"""
Database helpers relating to datastream relations.

Each DB helper takes an optional cursor as its final argument as transaction
control.
"""

import logging

from dgi_repo.database import cache
from dgi_repo.database.utilities import (check_cursor, DATASTREAM_RELATION_MAP,
                                         LINKED_RDF_OBJECT_TYPES)
from dgi_repo.database.write.relations import write_to_standard_relation_table

logger = logging.getLogger(__name__)


def write_relationship(namespace, predicate, subject, rdf_object, rdf_type,
                       cursor=None):
    """
    Write a datastream relation to the repository.
    """
    cursor = check_cursor(cursor)
    try:
        relation_db_info = DATASTREAM_RELATION_MAP[(namespace, predicate)]
        write_to_standard_relation_table(
            relation_db_info['table'],
            relation_db_info['upsert message'],
            subject,
            rdf_object,
            cursor
        )
    except KeyError:
        predicate_id = cache.predicate_id_from_raw(namespace, predicate,
                                                   cursor=cursor)
        write_to_general_rdf_table(predicate_id, subject, rdf_object,
                                   rdf_type, cursor=cursor)

    return cursor


def write_to_general_rdf_table(predicate_id, subject, rdf_object, rdf_type,
                               cursor=None):
    """
    Write to the main datastream RDF table.
    """
    if rdf_type in LINKED_RDF_OBJECT_TYPES:
        raise TypeError(('Trying to place {} of type {} into the datastream '
                         'general table.').format(rdf_object, rdf_type))
    cursor = check_cursor(cursor)

    cursor.execute('''
        INSERT INTO datastream_relationships (
            predicate,
            rdf_subject,
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
