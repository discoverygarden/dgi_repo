"""
Authorize actions.
"""
import falcon
from talons.auth import middleware

from dgi_repo.auth.drupal import SiteBasicIdentifier as Identifier
from dgi_repo.auth.drupal import authenticate as drupal_auth
from dgi_repo.auth.system import (authenticate as system_authenticator,
                                  Authorize as SystemAuthorize)
from dgi_repo.auth.utilities import Authenticator, Authorizer


def authorize(identity, action):
    """
    An external authorizor, as for talons.auth.external.Authorizer.

    Args:
        identity: A talons.auth.interfaces.Identity instance
        action: A talons.auth.interfaces.ResourceAction instance, with
                properties:
            request: The falcon.Request object of the HTTP request.
            params: The dict of parameters.

    Returns:
        A boolean indicating if the action should be allowed by the given
        agent.
    """
    # TODO: Apply "global" and object-level policies.
    return True


class AuthMiddleware(object):

    def __init__(self):
        """
        Constructor for the authentication middleware.
        """
        authenticator = Authenticator(
            drupal_auth,
            system_authenticator
        )
        authorizer = Authorizer(
          authorize,
          SystemAuthorize().authorize
        )
        self._auth_middleware = middleware.create_middleware(
            identify_with=[Identifier],
            authenticate_with=authenticator,
            authorize_with=authorizer
        )

        self._auth_middleware.raise_401_no_identity = self._raise_no_ident
        self._auth_middleware.raise_401_fail_authenticate = self._raise_failed

    def _raise_no_ident(self):
        """
        Raise an unauthorized exception for no identity information.
        """
        raise falcon.HTTPUnauthorized('Authentication required',
                                      'No identity information found.',
                                      ['basic'])

    def _raise_failed(self):
        """
        Raise an unauthorized exception for failure.
        """
        raise falcon.HTTPUnauthorized('Authentication required',
                                      'Authentication failed.', ['basic'])

    def process_request(self, req, resp):
        """
        Route the request through talons.
        """
        return self._auth_middleware(req, resp, req.params)
