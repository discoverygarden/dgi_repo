"""
Custom exception handler.
"""
import logging

import falcon

logger = logging.getLogger(__name__)


def handle_exception(ex, req, resp, params):
    """
    Custom Falcon exception handler that ensures we send 500s.
    """
    if not isinstance(ex, falcon.HTTPError):
        logger.exception('Uncaught exception:')
        raise falcon.HTTPError('500 Internal Server Error') from ex
    else:
        raise ex
