"""
Database helpers relating to the object relations.
"""

import dgi_repo.database.read.relations as relations_reader

from dgi_repo.database.utilities import check_cursor
from dgi_repo.database.utilities import OBJECT_RELATION_MAP


def read_relationship(namespace, predicate, subject=None, rdf_object=None,
                      cursor=None):
    """
    Read an object relation from the repository.
    """
    try:
        cursor = relations_reader.read_from_standard_relation_table(
            OBJECT_RELATION_MAP[(namespace, predicate)]['table'],
            subject,
            rdf_object,
            cursor
        )
    except KeyError:
        cursor = relations_reader.predicate_id_from_raw(
            namespace,
            predicate,
            cursor
        )
        predicate_id = cursor.fetchone()[0]
        cursor = read_from_general_rdf_table(
            predicate_id,
            subject,
            rdf_object,
            cursor
        )

    return cursor


def read_from_general_rdf_table(predicate, subject=None, rdf_object=None,
                                cursor=None):
    """
    Read from the general object RDF table.
    """
    return relations_reader.read_from_general_rdf_table(
        'object_relationships',
        predicate,
        subject,
        rdf_object,
        cursor
    )


def read_sequence_number(subject=None, paged_object=None, cursor=None):
    """
    Read an is sequence number of object relation from the repository.
    """
    cursor = check_cursor(cursor)

    if (subject and paged_object):
        cursor.execute('''
            SELECT * FROM is_sequence_number_of
            WHERE rdf_subject = %s and rdf_object = %s
        ''', (subject, paged_object))
    elif (subject):
        cursor.execute('''
            SELECT * FROM is_sequence_number_of
            WHERE rdf_subject = %s
        ''', (subject,))
    elif (paged_object):
        cursor.execute('''
            SELECT * FROM is_sequence_number_of
            WHERE rdf_object = %s
        ''', (paged_object,))
    else:
        raise ValueError('Specify either subject, object or both.')

    return cursor
