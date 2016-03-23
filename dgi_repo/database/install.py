"""
Install related DB functions.
"""

import logging
from os.path import join, dirname

import dgi_repo.fcrepo3.relations as rels
from dgi_repo.database.utilities import get_connection

logger = logging.getLogger(__name__)


def install_schema():
    """
    Install the application schema to the database.
    """
    db_connection = get_connection()
    with db_connection:
        sql_file_path = join(dirname(__file__), 'resources', 'dgi_repo.sql')
        with open(sql_file_path, 'r') as schema_file:
            with db_connection.cursor() as db_cursor:
                db_cursor.execute(schema_file.read())
    db_connection.close()
    logger.info('Installed schema.')


def install_base_data():
    """
    Install the application's base data to the database.
    """
    import dgi_repo.database.write.relations as relations_writer

    db_connection = get_connection()
    with db_connection:
        with db_connection.cursor() as cursor:
            for namespace, predicates in rels.RELATIONS.items():

                relations_writer.upsert_namespace(namespace, cursor)
                namespace_id, = cursor.fetchone()

                for predicate in predicates:
                    relations_writer.upsert_predicate(
                        {'namespace': namespace_id, 'predicate': predicate},
                        cursor
                    )

    db_connection.close()
    logger.info('Installed base data.')
