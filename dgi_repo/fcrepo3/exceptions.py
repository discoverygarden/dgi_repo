"""
Custom exceptions and handlers.
"""
import falcon


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


def handle_exception(ex, req, resp, params):
    """
    Custom Falcon exception handler that ensures we send 500s.
    """
    raise falcon.HTTPError('500 Internal Server Error')
