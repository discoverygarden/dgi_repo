"""
Custom exceptions.
"""


class ObjectExistsError(Exception):
    """
    Used to indicate an object already exists when trying to ingest.

    First arg should be a PID.
    """
