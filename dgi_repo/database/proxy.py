"""
DB proxy.
"""

import falcon
import simplejson as json
from psycopg2 import connect

class ProxyResource(object):
    """
    Falcon resource for our DB proxy endpoint.
    """
    def on_post(self, req, resp):
        if req.content_type is not 'application/json':
            raise falcon.HTTPUnsupportedMediaType('Only "application/json" is supported on this endpoint.')
        info = json.load(req.stream)
        connection = self._get_conenction()
        with connection as conn:
            with conn.cursor(name=__name__) as cursor:
                try:
                    cursor.execute(info['query'], info['replacements'])
                    json.dump(cursor, resp.stream)
                except KeyError:
                    raise falcon.HTTPBadRequest('Missing value in JSON POST.', 'The POSTed JSON object must contain "query" and "replacements".')

        connection.close()


    def _get_connection(self):
        """
        Helper to get a connection with reduced permissions.
        """
        from dgi_repo.configuration import configuration as config
        return connect(
            host=config['database']['host'],
            database=config['database']['name'],
            user=config['db_proxy']['username'],
            password=config['db_proxy']['password'],
        )
