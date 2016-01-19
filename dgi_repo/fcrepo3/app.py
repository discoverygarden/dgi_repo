#!/usr/bin/env python

import falcon
from dgi_repo.configuration import configuration
import dgi_repo.auth.drupal import SiteBasicIdentifier as Identifier, authenticate
from talons.auth import middleware
from talons.auth.external import Authenticator
from falcon_multipart.middleware import MultipartMiddleware

auth_middleware = middleware.create_middleware(
    identify_with=[Identifier],
    authenticate_with=Authenticator(external_authn_callable=authenticate, external_set_groups=True)
)

app = falcon.API(
    before=[auth_middleware],
    middleware=[
         MultipartMiddleware()
    ]
)

for route, resource_class in configuration['fcrepo-implementation'].route_map:
    app.add_route(route, resource_class())

if __name__ == '__main__':
    from wsgiref import simple_server
    httpd = simple_server.make_server('', 8000, app)
