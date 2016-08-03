"""
Cache enabled database reads.
"""

from functools import lru_cache, wraps

from dgi_repo.database.read import repo_objects as object_reader
from dgi_repo.database.read import relations as relation_reader
from dgi_repo.configuration import configuration as _config


def no_none_cache(func):
    """
    A decorator that clears the lru_cache if the result is None.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if result is None:
            func.cache_clear()
        return result
    return wrapper


@no_none_cache
@lru_cache(maxsize=_config['database']['cache_size'])
def repo_object_namespace_id(namespace, cursor=None):
    """
    Get a repo object namespace ID, using a configurable cache if available.
    """
    cursor = object_reader.namespace_id(namespace, cursor=cursor)

    if not cursor.rowcount:
        return None

    return cursor.fetchone()['id']
