"""
Database helpers relating to datastream relations.

Each DB helper takes an optional cursor as its final argument as transaction
control.
"""

import logging

from dgi_repo.database.utilities import check_cursor

logger = logging.getLogger(__name__)

RELATION_FUNCTION_MAP = {}


def write_relationship(rdf_namespace, rdf_predicate, rdf_subject, rdf_object):
    """
    """
