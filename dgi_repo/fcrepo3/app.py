#!/usr/bin/env python

import falcon
from dgi_repo.utilities import bootstrap
from dgi_repo.configuration import configuration
from dgi_repo.auth.drupal import SiteBasicIdentifier as Identifier, authenticate
from dgi_repo.fcrepo3.authorize import authorize
from talons.auth import middleware
from talons.auth.external import Authenticator, Authorizer
from falcon_multipart.middleware import MultipartMiddleware

bootstrap()

auth_middleware = middleware.create_middleware(
    identify_with=[Identifier],
    authenticate_with=Authenticator(external_authn_callable=authenticate, external_set_groups=True),
    authorize_with=Authorizer(external_authz_callable=authorize)
)

app = falcon.API(
    before=[auth_middleware],
    middleware=[
         MultipartMiddleware()
    ]
)

for route, resource_class in configuration['fcrepo-implementation'].route_map.items():
    # XXX: Injecting the "fedora" path component...
    app.add_route('/fedora{0}'.format(route), resource_class())

def main():
    """
    Permit running with wsgiref.simple_server.

    Note: Appears to have issue dealing with streams, so SOAP and file uploads
    likely will not work correctly.
    """
    from wsgiref import simple_server
    httpd = simple_server.make_server('', 8000, app)
    httpd.serve_forever()


if __name__ == '__main__':
    main()
