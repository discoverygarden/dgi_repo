"""
Database helpers relating to relations.

Each DB helper takes an optional cursor as its final argument as transaction
control.
"""

import logging

from dgi_repo.database.utilities import check_cursor

logger = logging.getLogger(__name__)


def upsert_namespace(namespace, cursor=None):
    """
    Upsert an RDF namespace in the repository.
    """
    from dgi_repo.database.read.relations import namespace_id

    cursor = check_cursor(cursor)

    cursor.execute('''
        INSERT INTO rdf_namespaces (rdf_namespace)
        VALUES (%s)
        ON CONFLICT (rdf_namespace) DO NOTHING
        RETURNING id
    ''', (namespace,))

    if not cursor.rowcount:
        cursor = namespace_id(namespace, cursor)

    logger.debug('Upserted the namespace: %s.', namespace)

    return cursor


def upsert_predicate(data, cursor=None):
    """
    Upsert a predicate in the repository.
    """
    from dgi_repo.database.read.relations import predicate_id

    cursor = check_cursor(cursor)

    cursor.execute('''
        INSERT INTO predicates (predicate, rdf_namespace_id)
        VALUES (%(predicate)s, %(namespace)s)
        ON CONFLICT (predicate, rdf_namespace_id) DO NOTHING
        RETURNING id
    ''', data)

    if not cursor.rowcount:
        cursor = predicate_id(data, cursor)

    logger.debug('Upserted predicate %(predicate)s in namespace %(namespace)s.', data)

    return cursor


def write_to_standard_relation_table(table, log_message, subject, rdf_object, cursor=None):
    """
    Write to a table that uses the standard relation design.
    """
    cursor = check_cursor(cursor)

    cursor.execute('''
        INSERT INTO {} (rdf_subject, rdf_object)
        VALUES (%s, %s)
        RETURNING id
    '''.format(table), (subject, rdf_object))

    logger.debug(log_message, subject, rdf_object)

    return cursor
