"""
Helpers for determining authorization rules.
@todo: verify that there are restrictions before returning False.
"""
import dgi_repo.fcrepo3.relations as relations
import dgi_repo.database.read.datastream_relations as datastream_relations
import dgi_repo.database.read.object_relations as object_relations
from dgi_repo.database.utilities import check_cursor


def is_datastream_viewable(ds_db_id, user_id=None, roles=None, cursor=None):
    """
    Check if the datastream is viewable by the given user or roles.
    """
    cursor = check_cursor(cursor)

    if is_datastream_manageable(ds_db_id, user_id, roles, cursor):
        return True

    if user_id is not None:
        datastream_relations.read_relationship(
            relations.ISLANDORA_RELS_EXT_NAMESPACE,
            relations.IS_VIEWABLE_BY_USER_PREDICATE,
            ds_db_id,
            user_id,
            cursor=cursor
        )
        if cursor.fetchone():
            return True

    if roles:
        datastream_relations.read_relationship(
            relations.ISLANDORA_RELS_EXT_NAMESPACE,
            relations.IS_VIEWABLE_BY_ROLE_PREDICATE,
            ds_db_id,
            cursor=cursor
        )
        db_role_info = cursor.fetchall()
        db_roles = set()
        for db_role in db_role_info:
            db_roles.add(db_role['rdf_object'])

        if db_roles.intersection(roles):
            return True

    return False


def is_datastream_manageable(ds_db_id, user_id=None, roles=None, cursor=None):
    """
    Check if the datastream is manageable by the given user or roles.
    """
    cursor = check_cursor(cursor)

    if user_id is not None:
        datastream_relations.read_relationship(
            relations.ISLANDORA_RELS_EXT_NAMESPACE,
            relations.IS_MANAGEABLE_BY_USER_PREDICATE,
            ds_db_id,
            user_id,
            cursor=cursor
        )
        if cursor.fetchone():
            return True

    if roles:
        datastream_relations.read_relationship(
            relations.ISLANDORA_RELS_EXT_NAMESPACE,
            relations.IS_MANAGEABLE_BY_ROLE_PREDICATE,
            ds_db_id,
            cursor=cursor
        )
        db_role_info = cursor.fetchall()
        db_roles = set()
        for db_role in db_role_info:
            db_roles.add(db_role['rdf_object'])

        if db_roles.intersection(roles):
            return True

    return False


def is_object_viewable(object_db_id, user_id=None, roles=None, cursor=None):
    """
    Check if the object is viewable by the given user or roles.
    """
    cursor = check_cursor(cursor)

    if is_object_manageable(object_db_id, user_id, roles, cursor):
        return True

    if user_id is not None:
        object_relations.read_relationship(
            relations.ISLANDORA_RELS_EXT_NAMESPACE,
            relations.IS_VIEWABLE_BY_USER_PREDICATE,
            object_db_id,
            user_id,
            cursor=cursor
        )
        if cursor.fetchone():
            return True

    if roles:
        object_relations.read_relationship(
            relations.ISLANDORA_RELS_EXT_NAMESPACE,
            relations.IS_VIEWABLE_BY_USER_PREDICATE,
            object_db_id,
            cursor=cursor
        )
        db_role_info = cursor.fetchall()
        db_roles = set()
        for db_role in db_role_info:
            db_roles.add(db_role['rdf_object'])

        if db_roles.intersection(roles):
            return True

    return False


def is_object_manageable(object_db_id, user_id=None, roles=None, cursor=None):
    """
    Check if the object is manageable by the given user or roles.
    """
    cursor = check_cursor(cursor)

    if user_id is not None:
        object_relations.read_relationship(
            relations.ISLANDORA_RELS_EXT_NAMESPACE,
            relations.IS_MANAGEABLE_BY_USER_PREDICATE,
            object_db_id,
            user_id,
            cursor=cursor
        )
        if cursor.fetchone():
            return True

    if roles:
        object_relations.read_relationship(
            relations.ISLANDORA_RELS_EXT_NAMESPACE,
            relations.IS_MANAGEABLE_BY_ROLE_PREDICATE,
            object_db_id,
            cursor=cursor
        )
        db_role_info = cursor.fetchall()
        db_roles = set()
        for db_role in db_role_info:
            db_roles.add(db_role['rdf_object'])

        if db_roles.intersection(roles):
            return True

    return False
