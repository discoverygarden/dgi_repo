"""
Setup for the Falcon application.
"""
import falcon
from falcon_multipart.middleware import MultipartMiddleware
from talons.auth import middleware
from talons.auth.external import Authenticator, Authorizer

from dgi_repo.auth.drupal import SiteBasicIdentifier as Identifier
from dgi_repo.auth.drupal import authenticate
from dgi_repo.database.proxy import ProxyResource
from dgi_repo.utilities import bootstrap
from dgi_repo.fcrepo3 import resources
from dgi_repo.fcrepo3.object_resource import ObjectResource
from dgi_repo.fcrepo3.authorize import authorize
from dgi_repo.fcrepo3.exceptions import handle_exception

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

# Dynamically add resources from the main file.
for route, resource_class in resources.route_map.items():
    app.add_route(route, resource_class())

app.add_route('/query_proxy', ProxyResource())
app.add_route('/objects/{pid}', ObjectResource())

# Custom error handler to ensure 500s on any error.
app.add_error_handler(Exception, handle_exception)
