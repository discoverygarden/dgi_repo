"""
Database helpers relating to relations.
"""

from dgi_repo.database.utilities import check_cursor


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
        WHERE rdf_namespace = %(namespace)s AND predicate = %(predicate)s
    ''', data)

    return cursor


def read_from_standard_relation_table(table, subject=None, rdf_object=None,
                                      cursor=None):
    """
    Read from a table that uses the standard relation design.
    """
    cursor = check_cursor(cursor)

    if (subject and rdf_object):
        cursor.execute('''
            SELECT * FROM {}
            WHERE rdf_subject = %s and rdf_object = %s
        '''.format(table), (subject, rdf_object))
    elif (subject):
        cursor.execute('''
            SELECT * FROM {}
            WHERE rdf_subject = %s
        '''.format(table), (subject,))
    elif (rdf_object):
        cursor.execute('''
            SELECT * FROM {}
            WHERE rdf_object = %s
        '''.format(table), (rdf_object,))
    else:
        raise ValueError('Specify either subject, object or both.')

    return cursor


def read_from_general_rdf_table(table, predicate, subject=None,
                                rdf_object=None, cursor=None):
    """
    Read from the general object RDF table.
    """
    cursor = check_cursor(cursor)

    if (subject and rdf_object):
        cursor.execute('''
            SELECT * FROM {}
            WHERE predicate = %s and rdf_subject = %s and rdf_object = %s
        '''.format(table), (predicate, subject, rdf_object))
    elif (subject):
        cursor.execute('''
            SELECT * FROM {}
            WHERE predicate = %s and rdf_subject = %s
        '''.format(table), (predicate, subject))
    elif (rdf_object):
        cursor.execute('''
            SELECT * FROM {}
            WHERE predicate = %s and rdf_object = %s
        '''.format(table), (predicate, rdf_object))
    else:
        raise ValueError('Specify either subject, object or both.')

    return cursor


def predicate_id_from_raw(namespace, predicate, cursor=None):
    """
    Get a predicate ID from namespace and predicate strings.
    """
    cursor = check_cursor(cursor)

    namespace_id(namespace, cursor)
    namespace_db_id, = cursor.fetchone()
    predicate_id(
        {'namespace': namespace_db_id, 'predicate': predicate},
        cursor
    )

    return cursor
