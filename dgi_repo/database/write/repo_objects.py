"""
Database helpers directly related to repository objects.

Each DB helper takes an optional cursor as its final argument as transaction
control.
"""

import logging

from dgi_repo.configuration import configuration as _configuration
from dgi_repo.database.utilities import check_cursor
from dgi_repo.database.read.repo_objects import old_object_id, namespace_info

logger = logging.getLogger(__name__)


def get_pid_id(namespace=None, cursor=None):
    """
    Get an auto-incremented PID from the given namespace.
    """
    if namespace is None:
        namespace = _configuration['default_namespace']

    cursor = get_pid_ids(namespace, cursor=cursor)

    logger.debug("Retrieved a new PID in %s.", namespace)

    return cursor


def get_pid_ids(namespace=None, num_pids=1, cursor=None):
    """
    Get auto-incremented PIDs from the given namespace.
    """
    cursor = check_cursor(cursor)

    if namespace is None:
        namespace = _configuration['default_namespace']

    cursor.execute('''
        INSERT INTO pid_namespaces (namespace, highest_id)
        VALUES (%(namespace)s, %(num_pids)s)
        ON CONFLICT (namespace) DO UPDATE
        SET highest_id = pid_namespaces.highest_id + %(num_pids)s
        RETURNING highest_id, id
    ''', ({'namespace': namespace, 'num_pids': num_pids}))

    logger.debug("Retrieved new PIDs in %s.", namespace)

    return cursor


def upsert_object(data, cursor=None):
    """
    Upsert an object in the repository.
    """
    cursor = check_cursor(cursor)
    data = _set_object_defaults(data)

    cursor.execute('''
        INSERT INTO objects (pid_id, namespace, state, owner, label, versioned,
                             log, created, modified)
        VALUES (%(pid_id)s, %(namespace)s, %(state)s, %(owner)s, %(label)s,
                %(versioned)s, %(log)s, now(), now())
        ON CONFLICT (pid_id, namespace) DO UPDATE
        SET (pid_id, namespace, state, owner, label, versioned, log,
             modified) = (%(pid_id)s, %(namespace)s, %(state)s, %(owner)s,
             %(label)s, %(versioned)s, %(log)s, now())
        RETURNING id
    ''', data)

    logger.debug(
        "Upserted into namespace: %s with PID ID: %s.", data['namespace'],
        data['pid_id']
    )

    return cursor


def write_object(data, cursor=None):
    """
    Write an object in the repository.
    """
    cursor = check_cursor(cursor)
    data = _set_object_defaults(data)

    cursor.execute('''
        INSERT INTO objects (pid_id, namespace, state, owner, label, versioned,
                             log, created, modified)
        VALUES (%(pid_id)s, %(namespace)s, %(state)s, %(owner)s, %(label)s,
                %(versioned)s, %(log)s, now(), now())
        RETURNING id
    ''', data)

    logger.debug(
        "Wrote into namespace: %s with PID ID: %s.", data['namespace'],
        data['pid_id']
    )

    return cursor


def _set_object_defaults(data):
    """
    Populate defaults if not provided in the data.
    """
    if 'namespace' not in data:
        data['namespace'] = _configuration['default_namespace']
    if 'state' not in data:
        data['state'] = 'A'
    if 'label' not in data:
        data['label'] = None
    if 'versioned' not in data:
        data['versioned'] = True
    if 'log' not in data:
        data['log'] = None

    return data


def upsert_old_object(data, cursor=None):
    """
    Upsert an old object version in the repository.
    """
    cursor = check_cursor(cursor)

    cursor.execute('''
        INSERT INTO old_objects (current_object, log, state, owner, committed)
        VALUES (%(object)s, %(log)s, %(state)s, %(owner)s, %(committed)s)
        ON CONFLICT (current_object, committed) DO NOTHING
        RETURNING id
    ''', data)

    if not cursor.rowcount:
        cursor = old_object_id(data, cursor)

    logger.debug(
        'Upserted old object version for %(object)s at %(committed)s.',
        data
    )

    return cursor


def jump_pids(namespace_id, pid_id, cursor=None):
    """
    Raise the namespace's highest pid_id to the indicated point.
    """
    if pid_id.isdigit():
        pid_id = int(pid_id)
        namespace_info(namespace_id, cursor=cursor)
        namespace = cursor.fetchone()
        if namespace['highest_id'] < pid_id:
            get_pid_ids(namespace['namespace'],
                        namespace['highest_id'] - pid_id,
                        cursor=cursor)
    return cursor
