"""
Database utility functions.
"""


def get_connection():
    """
    Get a connection to the application database.
    """

    from psycopg2 import connect

    from dgi_repo.configuration import configuration

    connection_string = 'dbname={} user={} password={} host={}'.format(
        configuration['database']['name'],
        configuration['database']['username'],
        configuration['database']['password'],
        configuration['database']['host']
    )

    return connect(connection_string)

def install_schema():
    """
    Install the application schema to the database.
    """

    from os.path import join, dirname
    db_connection = get_connection()
    with db_connection:
        with open(join(dirname(__file__), 'resources', 'dgi_repo.sql'), 'r') as schema_file:
            with db_connection.cursor() as db_cursor:
                db_cursor.execute(schema_file.read())
    db_connection.close()