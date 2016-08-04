"""
Custom exception handler.
"""
import logging

import falcon
from psycopg2.extensions import TransactionRollbackError

from dgi_repo.database.read import cache

logger = logging.getLogger(__name__)


def handle_exception(e, req, resp, params):
    """
    Custom Falcon exception handler that ensures we send relevant HTTP codes.
    """
    # Clear all registered caches because the data could be rolled back.
    cache.clear_cache()

    if isinstance(e, TransactionRollbackError):
        logger.exception('Transaction issue:')
        raise falcon.HTTPError('409 Conflict') from e
    elif not isinstance(e, (falcon.HTTPError, falcon.HTTPStatus)):
        logger.exception('Uncaught exception:')
        raise falcon.HTTPError('500 Internal Server Error') from e
    else:
        raise e
