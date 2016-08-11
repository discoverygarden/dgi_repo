"""
Cache enabled database reads.
"""

from functools import wraps

from cachetools import LRUCache, cached, hashkey

import dgi_repo.database.write.repo_objects as object_writer
import dgi_repo.database.read.repo_objects as object_reader
import dgi_repo.database.read.relations as relations_reader
import dgi_repo.database.write.relations as relations_writer
from dgi_repo.database.utilities import check_cursor
from dgi_repo.configuration import configuration as _config


_caches = list()


def _cache(key=lambda *args, cursor=None, **kwargs: hashkey(*args, **kwargs)):
    """
    Decorator; establish a clearable LRU cache on a function.

    The caches registered with this module by either:
    - calling "cache_clear()" method of wrapped functions, or
    - calling the "dgi_repo.database.cache.clear_cache()" method.

    Args:
        key: A callable to process the arguments passed to the wrapped
            function into a key in the cache. The default uses all arguments
            except "cursor".
    """
    def decorator(func):
        cache = LRUCache(maxsize=_config['database']['cache_size'])
        _caches.append(cache)
        wrapped = cached(func)(cache, key=key)
        wrapped.cache_clear = lambda: cache.clear()
        return wrapped
    return decorator


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


def clear_cache():
    """
    Clear ALL the caches!
    """
    for cache in _caches:
        cache.clear()


@no_none_cache
@_cache()
def repo_object_namespace_id(namespace, cursor=None):
    """
    Get a repo object namespace, ID creating it if necessary.
    """
    cursor = object_reader.namespace_id(namespace, cursor=cursor)

    if not cursor.rowcount:
        # @XXX burns the first PID in a namespace.
        object_writer.get_pid_id(namespace, cursor=cursor)

    return cursor.fetchone()['id']


@no_none_cache
@_cache()
def rdf_namespace_id(namespace, cursor=None):
    """
    Get a RDF namespace ID, creating it if necessary.
    """
    cursor = relations_reader.namespace_id(namespace, cursor=cursor)

    if not cursor.rowcount:
        relations_writer.upsert_namespace(namespace, cursor=cursor)

    return cursor.fetchone()['id']


@no_none_cache
@_cache()
def predicate_id(namespace, predicate, cursor=None):
    """
    Get a RDF predicate ID, creating it if necessary.
    """
    data = {'namespace': namespace, 'predicate': predicate}
    cursor = relations_reader.predicate_id(data, cursor=cursor)

    if not cursor.rowcount:
        relations_writer.upsert_predicate(data, cursor=cursor)

    return cursor.fetchone()['id']


@no_none_cache
@_cache()
def predicate_id_from_raw(namespace, predicate, cursor=None):
    """
    Get a RDF predicate ID from string values, creating it if necessary.
    """
    cursor = check_cursor(cursor)

    namespace_id = rdf_namespace_id(namespace, cursor=cursor)

    return predicate_id(namespace_id, predicate, cursor=cursor)
