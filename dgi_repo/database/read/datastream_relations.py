"""
Database helpers relating to datastream relations.
"""

import dgi_repo.database.read.relations as relations_reader
from dgi_repo.database.utilities import DATASTREAM_RELATION_MAP
from dgi_repo.database.utilities import check_cursor
from dgi_repo.database import cache


def read_relationship(namespace, predicate, subject=None, rdf_object=None,
                      cursor=None):
    """
    Read a datastream relation from the repository.
    """
    cursor = check_cursor(cursor)
    try:
        relations_reader.read_from_standard_relation_table(
            DATASTREAM_RELATION_MAP[(namespace, predicate)]['table'],
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
    Read from the general datastream RDF table.
    """
    return relations_reader.read_from_general_rdf_table(
        'datastream_relationships',
        predicate,
        subject,
        rdf_object,
        cursor
    )
