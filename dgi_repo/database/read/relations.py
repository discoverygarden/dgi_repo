"""
Database helpers relating to relations.
"""

import logging

from dgi_repo.database.utilities import check_cursor

logger = logging.getLogger(__name__)

def namespace_id(namespace, cursor=None):
    """
    Query for an RDF namespace  ID from the repository.
    """
    cursor = check_cursor(cursor)

    cursor.execute('''
        SELECT id
        FROM rdf_namespaces
        WHERE  rdf_namespace = %s
    ''', (namespace,))

    return cursor


def predicate_id(data, cursor=None):
    """
    Query for a predicate ID from the repository.
    """
    cursor = check_cursor(cursor)

    cursor.execute('''
        SELECT id
        FROM predicates
        WHERE rdf_namespace_id = %(namespace)s AND predicate = %(predicate)s
    ''', data)

    return cursor
