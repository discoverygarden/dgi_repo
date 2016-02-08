import falcon
from falcon_multipart.middleware import MultipartMiddleware
from talons.auth import middleware
from talons.auth.external import Authenticator, Authorizer
from dgi_repo.utilities import bootstrap
from dgi_repo.configuration import configuration
from dgi_repo.auth.drupal import SiteBasicIdentifier as Identifier, authenticate
from .authorize import authorize
from . import resources
from dgi_repo.database.proxy import ProxyResource

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
    app.add_route(route, resource_class())
app.add_route('/query_proxy', ProxyResource())
