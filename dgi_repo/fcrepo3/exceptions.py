"""
Custom exceptions.
"""


class ObjectExistsError(Exception):
    """
    Used to indicate an object already exists when tryign to ingest.

    First arg should be a PID.
    """
