"""
Custom exceptions.
"""


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
