"""
Database helpers relating to the object relations.
"""

import logging

from dgi_repo.database.utilities import check_cursor

logger = logging.getLogger(__name__)

RELATION_FUNCTION_MAP = {}


def read_relationship(rdf_namespace, rdf_predicate, rdf_subject):
    """
    """
