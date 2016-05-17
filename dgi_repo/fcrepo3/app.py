"""
Setup for the Falcon application.
"""
import falcon
from falcon_multipart.middleware import MultipartMiddleware

from dgi_repo.database.proxy import ProxyResource
from dgi_repo.utilities import bootstrap
from dgi_repo.fcrepo3 import resources
from dgi_repo.fcrepo3.object_resource import ObjectResource
from dgi_repo.fcrepo3.datastream_resource import DatastreamResource
from dgi_repo.fcrepo3.authorize import AuthMiddleware
from dgi_repo.fcrepo3.exceptions import handle_exception

bootstrap()


app = falcon.API(
    middleware=[
        AuthMiddleware(),
        MultipartMiddleware()
    ]
)

# Dynamically add resources from the main file.
for route, resource_class in resources.route_map.items():
    app.add_route(route, resource_class())

app.add_route('/query_proxy', ProxyResource())
app.add_route('/objects/{pid}', ObjectResource())
app.add_route('/objects/{pid}/datastreams/{dsid}', DatastreamResource())

# Custom error handler to ensure 500s on any error.
app.add_error_handler(Exception, handle_exception)
