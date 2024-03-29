"""
Database helpers relating to the object relations.
"""

import dgi_repo.database.read.relations as relations_reader

from dgi_repo.database.utilities import check_cursor
from dgi_repo.database.utilities import OBJECT_RELATION_MAP
from dgi_repo.database import cache

REPO_OBJECT_RDF_OBJECT_TABLES = [
    'is_member_of_collection',
    'is_member_of',
    'is_constituent_of',
    'has_model',
    'is_page_of',
    'is_sequence_number_of',
]


def read_relationship(namespace, predicate, subject=None, rdf_object=None,
                      cursor=None):
    """
    Read an object relation from the repository.
    """
    cursor = check_cursor(cursor)
    try:
        relations_reader.read_from_standard_relation_table(
            OBJECT_RELATION_MAP[(namespace, predicate)]['table'],
            subject,
            rdf_object,
            cursor
        )
    except KeyError:
        predicate_id = cache.predicate_id_from_raw(
            namespace,
            predicate,
            cursor
        )
        read_from_general_rdf_table(
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


def is_object_referenced(object_id, cursor):
    """
    Check if an object is referenced by relations.
    """
    for table in REPO_OBJECT_RDF_OBJECT_TABLES:
        cursor.execute('''
            SELECT EXISTS(SELECT 1 from {} WHERE rdf_object=%s)
        '''.format(table), (object_id,))
        if cursor.fetchone()[0]:
            return True
    return False
