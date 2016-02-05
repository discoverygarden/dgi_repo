"""
DB proxy.
"""

from contextlib import closing
from tempfile import SpooledTemporaryFile

import falcon
import simplejson as json
from psycopg2 import connect, DatabaseError, ProgrammingError


class ProxyResource(object):
    """
    Falcon resource for our DB proxy endpoint.
    """
    def on_post(self, req, resp):
        if req.content_type != 'application/json':
            raise falcon.HTTPUnsupportedMediaType('Only "application/json" is supported on this endpoint.')
        info = json.load(req.stream)
        if 'query' not in info:
            raise falcon.HTTPMissingParam('query')

        # XXX: "mode" cannot be binary, since json.dump explicitly writes "str".
        resp.stream = SpooledTemporaryFile(max_size=4096, mode='w')

        with closing(self._get_connection()) as conn:
            # XXX: Named cursor must _not_ be closed... so no "with".
            cursor = conn.cursor(name=__name__)
            try:
                if 'replacements' in info:
                    try:
                        cursor.execute(info['query'], info['replacements'])
                    except TypeError:
                        raise falcon.HTTPBadRequest('Bad query', 'Query placeholders invalid for the given "replacements"?')
                else:
                    cursor.execute(info['query'])
            except ProgrammingError as pe:
                raise falcon.HTTPBadRequest('Bad query', pe.diag.message_primary)
            except DatabaseError as de:
                raise falcon.HTTPInternalServerError('Query failed', de.diag.message_primary)
            else:
                json.dump(cursor, resp.stream, iterable_as_array=True)

    def _get_connection(self):
        """
        Helper to get a connection with reduced permissions.
        """
        from dgi_repo.configuration import configuration as config
        connection = connect(
            host=config['database']['host'],
            database=config['database']['name'],
            user=config['db_proxy']['username'],
            password=config['db_proxy']['password'],
        )
        connection.set_session(readonly=True)
        return connection
