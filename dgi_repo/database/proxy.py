"""
DB proxy.
"""

from contextlib import closing

import falcon
import simplejson as json
from psycopg2 import connect, DatabaseError, ProgrammingError

from dgi_repo.configuration import configuration as _config
from dgi_repo.utilities import SpooledTemporaryFile
from dgi_repo.fcrepo3.utilities import serialize_to_json


class ProxyResource(object):
    """
    Falcon resource for our DB proxy endpoint.
    """
    def on_post(self, req, resp):
        """
        Respond to a particular POST'd JSON with JSON (or error).

        POST'd JSON is expected to have the "application/json" Content-Type
        header set, and to be an object containing up to two properties:
        - "query": A required string containing the query to perform, and
        - "replacements": Depending on the replacement tokens used, either a
            list or an object to combine into the query.

        "query" and "replacements" correspond to the two parameters of
        cursor.execute(). For particulars, see:
        http://initd.org/psycopg/docs/usage.html#query-parameters

        On success, the response body will be a list of lists, representing
        the rows returned from the query.
        """
        if req.content_type != 'application/json':
            raise falcon.HTTPUnsupportedMediaType(
                'Only "application/json" is supported on this endpoint.'
            )
        info = json.load(req.stream)
        if 'query' not in info:
            raise falcon.HTTPMissingParam('query')

        # XXX: "mode" cannot be binary, as json.dump explicitly writes "str".
        resp.stream = SpooledTemporaryFile(mode='w')

        with closing(self._get_connection()) as conn:
            # XXX: Named cursor must _not_ be closed... so no "with".
            cursor = conn.cursor(name=__name__)
            try:
                if 'replacements' in info:
                    try:
                        cursor.execute(info['query'], info['replacements'])
                    except (TypeError, IndexError):
                        raise falcon.HTTPBadRequest(
                            'Bad query',
                            ('Query placeholders invalid for the given'
                             ' "replacements"?')
                        )
                else:
                    cursor.execute(info['query'])
            except ProgrammingError as pe:
                raise falcon.HTTPBadRequest('Bad query',
                                            pe.diag.message_primary)
            except DatabaseError as de:
                raise falcon.HTTPInternalServerError('Query failed',
                                                     de.diag.message_primary)
            else:
                json.dump(cursor, resp.stream, iterable_as_array=True, default=serialize_to_json)

    def _get_connection(self):
        """
        Helper to get a connection with reduced permissions.
        """
        connection = connect(
            host=_config['database']['host'],
            database=_config['database']['name'],
            user=_config['db_proxy']['username'],
            password=_config['db_proxy']['password'],
        )
        connection.set_session(readonly=True)
        return connection
