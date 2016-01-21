import falcon
from falcon_multipart.middleware import MultipartMiddleware
from talons.auth import middleware
from talons.auth.external import Authenticator, Authorizer
from dgi_repo.utilities import bootstrap
from dgi_repo.configuration import configuration
from dgi_repo.auth.drupal import SiteBasicIdentifier as Identifier, authenticate
from .authorize import authorize
from . import resources

bootstrap()

auth_middleware = middleware.create_middleware(
    identify_with=[Identifier],
    authenticate_with=Authenticator(
        external_authn_callable=authenticate,
        external_set_groups=True
    ),
    authorize_with=Authorizer(external_authz_callable=authorize)
)

app = falcon.API(
    before=[auth_middleware],
    middleware=[
         MultipartMiddleware()
    ]
)

for route, resource_class in resources.route_map.items():
    # XXX: Injecting the "fedora" path component...
    app.add_route('/fedora{0}'.format(route), resource_class())
