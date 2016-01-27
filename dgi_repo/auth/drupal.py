"""
Authentication helpers.

Will need some means of configuring Drupal endpoints, likely as a dictionary of
dictionaries, mapping our site-identifying keys to maps of DB creds and some
key identifying the DB driver to use... And possibly the query (could we have a
default?)... Or materialization directly out of YAML
(http://pyyaml.org/wiki/PyYAMLDocumentation#YAMLtagsandPythontypes)?
"""
import logging
import talons.auth.basicauth
from dgi_repo.configuration import configuration

logger = logging.getLogger(__name__)

def authenticate(identity):
    """
    Check if the given identity is valid, and set the relevant roles.

    Likely used with talons.auth.external.Authenticator.

    Parameters:
        identity: An talons.auth.interfaces.Identity instance.

    Returns:
        A boolean indicating if the given identity authenticates.
    """
    if not hasattr(identity, 'site'):
        logger.warn('Got request without site token.')
        return False

    if identity.login == 'anonymous' and identity.key == 'anonymous':
        # Quick anonymous check...
        identity.drupal_user_id = 0
        identity.roles.add('anonymous user')
        logger.debug('Anonymous user logged in from %s.', identity.site)
        return True

    # Grab the config for the selected site.
    db_info = configuration['drupal_sites'][identity.site]['database']
    query = db_info.pop('query', '''SELECT DISTINCT u.uid, r.name
FROM (
  users u
    LEFT JOIN
  users_roles ON u.uid=users_roles.uid
  )
    LEFT JOIN role r ON r.rid=users_roles.rid
WHERE u.name=%s AND u.pass=%s''')

    try:
        # Get a DB connection and cursor for the selected site.
        conn = get_connection(identity.site)
        cursor = conn.cursor()

        # Check the credentials against the selected site (using provided
        # query or a default).
        cursor.execute(query, (identity.login, identity.key))

        if cursor.rowcount > 0:
            identity.drupal_user_id = None
            for uid, role in cursor:
                if identity.drupal_user_id is None:
                    identity.drupal_user_id = uid
                identity.roles.add(role)
            identity.roles.add('authenticated user')
            logger.info('Authenticated %s:%s with roles: %s', identity.site, identity.login, identity.roles)
            return True
        else:
            logger.info('Failed to authenticate %s:%s.', identity.site, identity.login)
            return False
    except:
        logger.exception('Error while authenticating using Drupal credentials.')
    finally:
        try:
            cursor.close()
        except UnboundLocalError:
            logger.debug('Failed before allocating DB cursor.')
        try:
            conn.close()
        except UnboundLocalError:
            logger.debug('Failed before creating DB connection.')
    return False


class SiteBasicIdentifier(talons.auth.basicauth.Identifier):
    """
    Determine against which site to validate credentials.
    """
    def identify(self, req):
        """
        Look at the headers in the request for our identifying header.
        """
        result = super().identify(req)

        if result:
            identity = req.env[self.IDENTITY_ENV_KEY]
            if req.user_agent is not None and not hasattr(identity, 'site'):
                # Sniff custom header to identify the particular origin site.
                us, sep, site = req.user_agent.partition('/')
                identity.site = site if us == 'Tuque' else None

        return result

_connectors = dict()
def get_connection(site):
    config = configuration['drupal_sites'][site]['database']
    return _connectors[config['type']](config['connection'])


try:
    import pymysql
    def _get_mysql_connection(config):
        return pymysql.connect(
            host=config.pop('host'),
            db=config.pop('name'),
            user=config.pop('username'),
            password=config.pop('password', ''),
            port=config.pop('port')
        )
    _connectors['mysql'] = _get_mysql_connection
except:
    logger.debug('MySQL driver not found.')

try:
    import psycopg2
    def _get_postgresql_driver(config):
        return psycopg2.connect(
            database=config.pop('name'),
            user=config.pop('username'),
            password=config.pop('password'),
            host=config.pop('host'),
            port=config.pop('port')
        )
    _connectors['postgres'] = _get_postgresql_driver
except:
    logger.debug('PostgreSQL driver not found.')

def _get_ioc_driver(config):
    args = config.pop('args', [])
    kwargs = config.pop('kwargs', {})
    return config['callable'](*args, **kwargs)
_connectors['ioc'] = _get_ioc_driver
