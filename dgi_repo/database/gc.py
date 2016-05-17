import logging
from datetime import timedelta

import click

from dgi_repo.configuration import configuration as _config
from dgi_repo.database.utilities import get_connection
from dgi_repo.database.filestore import purge_all

logger = logging.getLogger(__name__)

@click.command()
def collect():
    age = timedelta(**_config['unreferenced_age'])

    with get_connection() as conn, conn.cursor() as cursor:
        cursor.execute("""
            CREATE TEMPORARY TABLE garbage
            ON COMMIT DROP
            AS
                SELECT id
                FROM resource_refcounts
                WHERE refcount = 0 and age(now(), touched) > %s
            WITH DATA
        """, (age, ))
        named_cursor = conn.cursor('dgi_repo_gc', scrollable=False)
        named_cursor.execute('SELECT id FROM garbage')
        purge_all((resource_id for (resource_id, ) in named_cursor))

if __name__ == '__main__':
    collect()
