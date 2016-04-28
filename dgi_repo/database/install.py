"""
Install related DB functions.
"""

import logging
from os.path import join, dirname

from psycopg2.extensions import ISOLATION_LEVEL_REPEATABLE_READ

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
            with db_connection.cursor() as cursor:
                cursor.execute(schema_file.read())
    db_connection.close()
    logger.info('Installed schema.')


def install_base_data():
    """
    Install the application's base data to the database.
    """
    import dgi_repo.database.write.relations as relations_writer

    db_connection = get_connection(
        isolation_level=ISOLATION_LEVEL_REPEATABLE_READ
    )
    with db_connection, db_connection.cursor() as cursor:
        for namespace, predicates in rels.RELATIONS.items():
            # Default relationship data.
            relations_writer.upsert_namespace(namespace, cursor=cursor)
            namespace_id, = cursor.fetchone()
            for predicate in predicates:
                relations_writer.upsert_predicate(
                    {'namespace': namespace_id, 'predicate': predicate},
                    cursor=cursor
                )

            # @TODO: default object data.

    db_connection.close()
    logger.info('Installed base data.')
