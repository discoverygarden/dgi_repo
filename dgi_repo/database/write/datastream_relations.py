"""
Database helpers relating to datastream relations.

Each DB helper takes an optional cursor as its final argument as transaction
control.
"""

import logging

from dgi_repo.database.utilities import check_cursor

logger = logging.getLogger(__name__)


def write_relationship(namespace, predicate, subject, rdf_object, cursor=None):
    """
    Read a datastream relation to the repository.
    """
    from dgi_repo.database.read.relations import predicate_id_from_raw
    from dgi_repo.database.utilities import DATASTREAM_RELATION_MAP
    from dgi_repo.database.write.relations import write_to_standard_relation_table

    try:
        (table, log_message) = DATASTREAM_RELATION_MAP[(namespace, predicate)]
        cursor = write_to_standard_relation_table(
            table,
            log_message,
            subject,
            rdf_object,
            cursor
        )
    except KeyError:
        predicate_id = predicate_id_from_raw(namespace, predicate, cursor)
        cursor = write_to_general_rdf_table(predicate_id, subject, rdf_object, cursor)

    return cursor


def write_to_general_rdf_table(predicate_id, subject, rdf_object, cursor=None):
    """
    Write to the main datastream RDF table.
    """
    cursor = check_cursor(cursor)

    cursor.execute('''
        INSERT INTO datastream_relationships (predicate_id, subject, rdf_object)
        VALUES (%s, %s, %s)
        RETURNING id
    ''', (predicate_id, subject, rdf_object))

    return cursor
