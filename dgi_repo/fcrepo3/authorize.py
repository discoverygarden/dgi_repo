"""
Authorize actions.
"""
import falcon
from talons.auth import middleware
from talons.auth.external import Authenticator, Authorizer

from dgi_repo.auth.drupal import SiteBasicIdentifier as Identifier
from dgi_repo.auth.drupal import authenticate


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
        self._auth_middleware = middleware.create_middleware(
            identify_with=[Identifier],
            authenticate_with=Authenticator(
                external_authn_callable=authenticate,
                external_set_groups=True
            ),
            authorize_with=Authorizer(external_authz_callable=authorize)
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
