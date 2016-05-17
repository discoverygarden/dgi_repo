"""
Custom exception handler.
"""
import logging

import falcon

logger = logging.getLogger(__name__)


def handle_exception(e, req, resp, params):
    """
    Custom Falcon exception handler that ensures we send 500s.
    """
    if not isinstance(e, (falcon.HTTPError, falcon.HTTPStatus)):
        logger.exception('Uncaught exception:')
        raise falcon.HTTPError('500 Internal Server Error') from e
    else:
        raise e
