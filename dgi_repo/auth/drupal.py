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
        user_id = 0
        identity.roles.add('anonymous user')
        logger.debug('Anonymous user logged in from %s.', identity.site)
        return True

    # Grab the config for the selected site.
    config = {
        'args': [],
        'kwargs': {},
        'uid_query': '''SELECT uid
FROM users
WHERE name=%s AND pass=%s''',
        'role_query': '''SELECT r.name
FROM
    users_roles AS ur
        INNER JOIN
    role AS r
        ON ur.rid = r.rid
WHERE
    ur.uid = %s'''
    }

    config.update(configuration['drupal_sites'][identity.site]['database']['connection'])

    try:
        # Get a DB cursor for the selected site.
        conn = config['callable'](*args, **kwargs)
        cursor = conn.cursor()

        # Check the credentials against the selected site (using provided
        # query or a default).
        cursor.execute(uid_query, (identity.login, identity.key))
        try:
            user_id, = cursor.fetchone()
        except:
            logger.info('Invalid credentials for %s:%s.', identity.site, identity.login)
            return False

        cursor.execute(role_query, user_id)
        identity.roles.add('authenticated user')
        for role, in cursor:
            identity.roles.add(role)
        logger.info('Authenticated %s:%s with roles: %s', identity.site, identity.login, identity.roles)
        return True
    except:
        logger.exception('Error while authenticating using Drupal credentials.')
    finally:
        cursor.close()
        conn.close()
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
