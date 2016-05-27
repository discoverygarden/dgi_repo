"""
Custom exceptions.
"""


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


class ReferencedObjectDoesNotExistError(ObjectDoesNotExistError):
    """
    Used to indicate a referenced (RELS) object doesn't exist.
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


class ObjectConflictsError(Exception):
    """
    Used to indicate an object change conflicts.
    """

    def __init__(self, pid, modified_time, request_time):
        """
        Constructor for exception.
        """
        self.pid = pid
        self.modified_time = modified_time
        self.request_time = request_time
        super().__init__(pid, modified_time, request_time)


class DatastreamConflictsError(Exception):
    """
    Used to indicate a datastream change conflicts.
    """

    def __init__(self, pid, dsid, modified_time, request_time):
        """
        Constructor for exception.
        """
        self.pid = pid
        self.dsid = dsid
        self.modified_time = modified_time
        self.request_time = request_time
        super().__init__(pid, dsid, modified_time, request_time)


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

class ReferencedDatastreamDoesNotExist(DatastreamDoesNotExistError):
    """
    Used to indicate a referenced (RELS) datastream does not exist.
    """


class ExternalDatastreamsNotSupported(ValueError):
    """
    Raised when one tries to create an external datastream.
    """
