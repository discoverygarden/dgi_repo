"""
Custom exceptions and handlers.
"""
import logging

import falcon

logger = logging.getLogger(__name__)


class ObjectDoesNotExistError(Exception):
    """
    Used to indicate an object expected to exist does not.
    """

    def __init__(self, pid):
        """
        Constructor for exception.
        """
        self.pid = pid
        super().__init__(pid)


class ObjectExistsError(Exception):
    """
    Used to indicate an object already exists when trying to ingest.
    """

    def __init__(self, pid):
        """
        Constructor for exception.
        """
        self.pid = pid
        super().__init__(pid)


class DatastreamDoesNotExistError(Exception):
    """
    Used to indicate a datastream expected to exist does not.
    """

    def __init__(self, pid, dsid, time=None):
        """
        Constructor for exception.
        """
        self.pid = pid
        self.dsid = dsid
        self.time = time if time is not None else 'now'
        super().__init__(pid, dsid, time)


def handle_exception(ex, req, resp, params):
    """
    Custom Falcon exception handler that ensures we send 500s.
    """
    if not isinstance(ex, falcon.HTTPError):
        logger.exception('Uncaught exception:')
        raise falcon.HTTPError('500 Internal Server Error') from ex
    else:
        raise ex
