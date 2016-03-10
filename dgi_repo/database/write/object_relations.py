"""
Database helpers relating to object relations.

Each DB helper takes an optional cursor as its final argument as transaction
control.
"""

import logging

from dgi_repo.database.utilities import check_cursor

logger = logging.getLogger(__name__)


def write_relationship(namespace, predicate, subject, rdf_object, cursor=None):
    """
    Write an object relation to the repository.
    """
    from dgi_repo.database.read.relations import predicate_id_from_raw
    from dgi_repo.database.utilities import OBJECT_RELATION_MAP
    from dgi_repo.database.write.relations import write_to_standard_relation_table

    try:
        relation_db_info = OBJECT_RELATION_MAP[(namespace, predicate)]
        cursor = write_to_standard_relation_table(
            relation_db_info['table'],
            relation_db_info['upsert message'],
            subject,
            rdf_object,
            cursor
        )
    except KeyError:
        cursor = predicate_id_from_raw(namespace, predicate, cursor)
        predicate_id = cursor.fetchone()[0]
        cursor = write_to_general_rdf_table(predicate_id, subject, rdf_object, cursor)

    return cursor


def write_to_general_rdf_table(predicate_id, subject, rdf_object, cursor=None):
    """
    Write to the main object RDF table.
    """
    cursor = check_cursor(cursor)

    cursor.execute('''
        INSERT INTO object_relationships (predicate_id, subject, rdf_object)
        VALUES (%s, %s, %s)
        RETURNING id
    ''', (predicate_id, subject, rdf_object))

    logger.debug(
        'Upserted an object relation "%s" on %s as %s.',
        predicate_id,
        subject,
        rdf_object
    )

    return cursor


def write_sequence_number(subject, paged_object, sequence_number, cursor=None):
    """
    Write an is sequence number of object relation to the repository.
    """
    cursor = check_cursor(cursor)

    cursor.execute('''
        INSERT INTO is_sequence_number_of (rdf_subject, rdf_object, sequence_number)
        VALUES (%s, %s, %s)
        RETURNING id
    ''', (subject, paged_object, sequence_number))

    logger.debug(
        'Upserted an "is sequence number of" relation on %s to %s as %s.',
        subject,
        paged_object,
        sequence_number
    )

    return cursor
