"""
Database helpers relating to object relations.

Each DB helper takes an optional cursor as its final argument as transaction
control.
"""

import logging

from dgi_repo.database import cache
from dgi_repo.database.utilities import (check_cursor, OBJECT_RELATION_MAP,
                                         LINKED_RDF_OBJECT_TYPES)
from dgi_repo.fcrepo3.relations import ISLANDORA_RELS_EXT_NAMESPACE
from dgi_repo.database.read.repo_objects import object_id_from_raw
from dgi_repo.database.write.relations import write_to_standard_relation_table
from dgi_repo.utilities import rreplace

logger = logging.getLogger(__name__)


def write_relationship(namespace, predicate, subject, rdf_object, rdf_type,
                       cursor=None):
    """
    Write an object relation to the repository.
    """
    cursor = check_cursor(cursor)
    try:
        relation_db_info = OBJECT_RELATION_MAP[(namespace, predicate)]
        write_to_standard_relation_table(
            relation_db_info['table'],
            relation_db_info['upsert message'],
            subject,
            rdf_object,
            cursor
        )
    except KeyError:
        if (namespace == ISLANDORA_RELS_EXT_NAMESPACE and
                predicate.startswith('isSequenceNumberOf')):
            almost_pid = predicate.split('isSequenceNumberOf', 1)[1]
            paged_pid = rreplace(almost_pid, '_', ':', 1)
            paged_object = object_id_from_raw(paged_pid, cursor=cursor
                                              ).fetchone()['id']
            write_sequence_number(subject, paged_object, rdf_object,
                                  cursor=cursor)
        else:
            predicate_id = cache.predicate_id_from_raw(namespace, predicate,
                                                       cursor=cursor)
            write_to_general_rdf_table(predicate_id, subject, rdf_object,
                                       rdf_type, cursor=cursor)

    return cursor


def write_to_general_rdf_table(predicate_id, subject, rdf_object, rdf_type,
                               cursor=None):
    """
    Write to the main object RDF table.
    """
    if rdf_type in LINKED_RDF_OBJECT_TYPES:
        raise TypeError(('Trying to place {} of type {} into the object '
                         'general table.').format(rdf_object, rdf_type))
    cursor = check_cursor(cursor)

    cursor.execute('''
        INSERT INTO object_relationships (predicate, rdf_subject, rdf_object)
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
        INSERT INTO is_sequence_number_of (rdf_subject, rdf_object,
                                           sequence_number)
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
