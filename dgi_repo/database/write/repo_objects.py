"""
Database helpers directly related to repository objects.

Each DB helper takes an optional cursor as its final argument as transaction
control.
"""

import logging

from dgi_repo.configuration import configuration as _config
from dgi_repo.database.utilities import check_cursor
import dgi_repo.database.read.repo_objects as object_reader
import dgi_repo.database.read.sources as source_reader

logger = logging.getLogger(__name__)


def get_pid_id(namespace=None, cursor=None):
    """
    Get an auto-incremented PID from the given namespace.
    """
    if namespace is None:
        namespace = _config['default_namespace']

    cursor = get_pid_ids(namespace, cursor=cursor)

    logger.debug("Retrieved a new PID in %s.", namespace)

    return cursor


def get_pid_ids(namespace=None, num_pids=1, cursor=None):
    """
    Get auto-incremented PIDs from the given namespace.
    """
    cursor = check_cursor(cursor)

    if namespace is None:
        namespace = _config['default_namespace']

    cursor.execute('''
        INSERT INTO pid_namespaces (namespace, highest_id)
        VALUES (%(namespace)s, %(num_pids)s)
        ON CONFLICT (namespace) DO UPDATE
        SET highest_id = pid_namespaces.highest_id + %(num_pids)s
        RETURNING highest_id, id
    ''', ({'namespace': namespace, 'num_pids': num_pids}))

    logger.debug("Retrieved new PIDs in %s.", namespace)

    return cursor


def upsert_namespace(namespace, cursor=None):
    """
    Upsert a namespace in the repository.
    """
    cursor = check_cursor(cursor)

    cursor.execute('''
        INSERT INTO pid_namespaces (namespace, highest_id)
        VALUES (%s, 0)
        ON CONFLICT (namespace) DO NOTHING
        RETURNING id
    ''', (namespace,))

    if not cursor.rowcount:
        cursor = object_reader.namespace_id(namespace, cursor=cursor)

    logger.debug("Upserted namespace %s.", namespace)

    return cursor


def upsert_object(data, cursor=None):
    """
    Upsert an object in the repository.
    """
    cursor = check_cursor(cursor)
    data = _set_object_defaults(data, cursor)

    cursor.execute('''
        INSERT INTO objects (pid_id, namespace, state, owner, label, versioned,
                             log, created, modified)
        VALUES (%(pid_id)s, %(namespace)s, %(state)s, %(owner)s, %(label)s,
                %(versioned)s, %(log)s,  %(created)s, %(modified)s)
        ON CONFLICT (pid_id, namespace) DO UPDATE
        SET (pid_id, namespace, state, owner, label, versioned, log,
             modified) = (%(pid_id)s, %(namespace)s, %(state)s, %(owner)s,
             %(label)s, %(versioned)s, %(log)s, %(modified)s)
        RETURNING id
    ''', data)

    logger.info("Upserted into namespace: %s with PID ID: %s.",
                data['namespace'], data['pid_id'])

    return cursor


def write_object(data, cursor=None):
    """
    Write an object in the repository.
    """
    cursor = check_cursor(cursor)
    data = _set_object_defaults(data, cursor)

    cursor.execute('''
        INSERT INTO objects (pid_id, namespace, state, owner, label, versioned,
                             log, created, modified)
        VALUES (%(pid_id)s, %(namespace)s, %(state)s, %(owner)s, %(label)s,
                %(versioned)s, %(log)s, %(created)s, %(modified)s)
        RETURNING id
    ''', data)

    logger.debug(
        "Wrote into namespace: %s with PID ID: %s.", data['namespace'],
        data['pid_id']
    )

    return cursor


def _set_object_defaults(data, cursor):
    """
    Populate defaults if not provided in the data.
    """
    data.setdefault('log')
    data.setdefault('label')
    data.setdefault('state', 'A')
    data.setdefault('versioned', True)
    data.setdefault('created', 'now')
    data.setdefault('modified', 'now')

    if 'owner' not in data:
        data['owner'] = source_reader.user_id_from_raw(
            _config['self']['source'],
            _config['self']['username'],
            cursor=cursor
        ).fetchone()['id']

    return data


def upsert_old_object(data, cursor=None):
    """
    Upsert an old object version in the repository.
    """
    cursor = check_cursor(cursor)

    cursor.execute('''
        INSERT INTO old_objects (object, log, state, owner, committed)
        VALUES (%(object)s, %(log)s, %(state)s, %(owner)s, %(committed)s)
        ON CONFLICT (object, committed) DO NOTHING
        RETURNING id
    ''', data)

    if not cursor.rowcount:
        cursor = object_reader.old_object_id(data, cursor=cursor)

    logger.debug(
        'Upserted old object version for %(object)s at %(committed)s.',
        data
    )

    return cursor


def jump_pids(namespace_id, pid_id, cursor=None):
    """
    Raise the namespace's highest pid_id to the indicated point.
    """
    cursor = check_cursor(cursor)

    if pid_id.isdecimal():
        pid_id = int(pid_id)
        cursor.execute('''
            UPDATE pid_namespaces
            SET highest_id =  %(pid_id)s
            WHERE highest_id < %(pid_id)s and id = %(id)s
        ''', ({'id': namespace_id, 'pid_id': pid_id}))

        logger.debug("Ensured PIDs will increment after %s.", pid_id)

    return cursor
