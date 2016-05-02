"""
Install related DB functions.
"""

import logging
from os.path import join, dirname

from psycopg2.extensions import ISOLATION_LEVEL_READ_COMMITTED

import dgi_repo.fcrepo3.relations as rels
import dgi_repo.fcrepo3.foxml as foxml
import dgi_repo.database.write.repo_objects as object_writer
import dgi_repo.database.write.relations as relations_writer
import dgi_repo.database.write.sources as source_writer
import dgi_repo.utilities as utils
from dgi_repo.database.utilities import get_connection
from dgi_repo.configuration import configuration as _config

logger = logging.getLogger(__name__)

BASE_NAMESPACES = ['islandora', 'fedora-system']
BASE_OBJECTS = [
    'fedora-system:ContentModel-3.0',
    'fedora-system:FedoraObject-3.0',
    'fedora-system:ServiceDefinition-3.0',
    'fedora-system:ServiceDeployment-3.0',
]


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
    db_connection = get_connection(
        isolation_level=ISOLATION_LEVEL_READ_COMMITTED
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

            # Default user data.
            source_id = source_writer.upsert_source(
                _config['self']['source'],
                cursor=cursor
            ).fetchone()['id']
            user_id = source_writer.upsert_user(
                {'source': source_id, 'name': _config['self']['username']},
                cursor=cursor
            ).fetchone()['id']

            # Default namespace data.
            ns_map = {}
            for namespace in BASE_NAMESPACES:
                ns_map[namespace] = object_writer.upsert_namespace(
                    namespace,
                    cursor=cursor
                ).fetchone()['id']

            # Default object data.
            for obj in BASE_OBJECTS:
                namespace, pid_id = utils.break_pid(obj)
                obj_info = object_writer.upsert_object(
                    {
                        'namespace': ns_map[namespace],
                        'owner': user_id,
                        'pid_id': pid_id,
                    },
                    cursor=cursor
                ).fetchone()
                # Add DC DS as Fedora objects have DC and Islandora expects it.
                foxml.create_default_dc_ds(obj_info['id'], obj, cursor=cursor)

    db_connection.close()
    logger.info('Installed base data.')
