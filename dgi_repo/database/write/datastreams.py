"""
Database helpers relating to datastreams.

Each DB helper takes an optional cursor as its final argument as transaction
control.
"""

import logging

from dgi_repo.database.utilities import check_cursor
from dgi_repo.database.read.datastreams import mime_id, old_datastream_id

logger = logging.getLogger(__name__)


def upsert_datastream(data, cursor=None):
    """
    Upsert a datastream in the repository.
    """
    cursor = check_cursor(cursor)

    data.setdefault('log')
    data.setdefault('label')
    data.setdefault('resource')
    data.setdefault('state', 'A')
    data.setdefault('archival', False)
    data.setdefault('versioned', False)
    data.setdefault('modified', 'now()')
    data.setdefault('created', 'now()')

    cursor.execute('''
        INSERT INTO datastreams (
            object,
            label,
            dsid,
            resource,
            versioned,
            archival,
            control_group,
            state,
            log,
            modified,
            created
        )
        VALUES (
            %(object)s,
            %(label)s,
            %(dsid)s,
            %(resource)s,
            %(versioned)s,
            %(archival)s,
            %(control_group)s,
            %(state)s,
            %(log)s,
            %(modified)s,
            %(created)s
        )
        ON CONFLICT (object, dsid) DO UPDATE
        SET (
                object,
                label,
                dsid,
                resource,
                versioned,
                archival,
                control_group,
                state,
                log,
                modified
            ) =
            (
                %(object)s,
                %(label)s,
                %(dsid)s,
                %(resource)s,
                %(versioned)s,
                %(archival)s,
                %(control_group)s,
                %(state)s,
                %(log)s,
                %(modified)s
            )
        RETURNING id
    ''', data)

    logger.debug('Upserted DS %(dsid)s on %(object)s.', data)

    return cursor


def upsert_resource(data, cursor=None):
    """
    Upsert a resource in the repository.
    """
    cursor = check_cursor(cursor)

    cursor.execute('''
        INSERT INTO resources (uri, mime)
        VALUES (%(uri)s, %(mime)s)
        ON CONFLICT (uri) DO UPDATE
        SET (uri, mime) = (%(uri)s, %(mime)s)
        RETURNING id
    ''', data)

    logger.debug('Upserted resource %(uri)s.', data)

    return cursor


def upsert_mime(mime, cursor=None):
    """
    Upsert a mime in the repository.
    """
    cursor = check_cursor(cursor)

    cursor.execute('''
        INSERT INTO mimes (mime)
        VALUES (%s)
        ON CONFLICT (mime) DO NOTHING
        RETURNING id
    ''', (mime,))

    if not cursor.rowcount:
        cursor = mime_id(mime, cursor)

    logger.debug('Upserted mime: %s.', mime)

    return cursor


def upsert_checksum(data, cursor=None):
    """
    Upsert a checksum in the repository.
    """
    cursor = check_cursor(cursor)

    cursor.execute('''
        INSERT INTO checksums (checksum, resource, type)
        VALUES (%(checksum)s, %(resource)s, %(type)s)
        ON CONFLICT (resource, type) DO UPDATE
        SET (checksum) = (%(checksum)s)
        RETURNING id
    ''', data)

    logger.debug('Upserted checksum for resource: %(resource)s.', data)

    return cursor


def upsert_old_datastream(data, cursor=None):
    """
    Upsert an old datastream version in the repository.
    """
    cursor = check_cursor(cursor)

    data.setdefault('log')

    cursor.execute('''
        INSERT INTO old_datastreams (
            current_datastream,
            log,
            state,
            label,
            resource,
            committed
        )
        VALUES (
            %(datastream)s,
            %(log)s,
            %(state)s,
            %(label)s,
            %(resource)s,
            %(committed)s
        )
        ON CONFLICT (current_datastream, committed) DO NOTHING
        RETURNING id
    ''', data)

    if not cursor.rowcount:
        cursor = old_datastream_id(data, cursor)

    logger.debug(
        'Upserted old datastream version for %(datastream)s at %(committed)s.',
        data
    )

    return cursor
