"""
Cache enabled database reads.
"""

from cachetools import LRUCache, cached
from cachetools.keys import hashkey

import dgi_repo.database.write.repo_objects as object_writer
import dgi_repo.database.read.repo_objects as object_reader
import dgi_repo.database.read.relations as relations_reader
import dgi_repo.database.write.relations as relations_writer
from dgi_repo.database.utilities import check_cursor
from dgi_repo.configuration import configuration as _config


_caches = list()


def _cache(key=hashkey):
    """
    Decorator; establish a clearable LRU cache on a function.

    Clear the caches registered with this module by calling the
    "dgi_repo.database.cache.clear_cache()" method.

    Args:
        key: A callable to process the arguments passed to the wrapped
            function into a key in the cache. The default uses all arguments.
    """
    def decorator(func):
        cache = LRUCache(maxsize=_config['database']['cache_size'])
        _caches.append(cache)
        wrapped = cached(cache, key=key)(func)
        return wrapped
    return decorator


def clear_cache():
    """
    Clear ALL the caches!
    """
    for cache in _caches:
        cache.clear()


@_cache(key=lambda namespace, cursor=None: hashkey(namespace))
def repo_object_namespace_id(namespace, cursor=None):
    """
    Get a repo object namespace, ID creating it if necessary.
    """
    cursor = object_reader.namespace_id(namespace, cursor=cursor)

    if not cursor.rowcount:
        # @XXX burns the first PID in a namespace.
        object_writer.get_pid_id(namespace, cursor=cursor)

    return cursor.fetchone()['id']


@_cache(key=lambda namespace, cursor=None: hashkey(namespace))
def rdf_namespace_id(namespace, cursor=None):
    """
    Get a RDF namespace ID, creating it if necessary.
    """
    cursor = relations_reader.namespace_id(namespace, cursor=cursor)

    if not cursor.rowcount:
        relations_writer.upsert_namespace(namespace, cursor=cursor)

    return cursor.fetchone()['id']


@_cache(
    key=lambda namespace, predicate, cursor=None: hashkey(namespace, predicate)
)
def predicate_id(namespace, predicate, cursor=None):
    """
    Get a RDF predicate ID, creating it if necessary.
    """
    data = {'namespace': namespace, 'predicate': predicate}
    cursor = relations_reader.predicate_id(data, cursor=cursor)

    if not cursor.rowcount:
        relations_writer.upsert_predicate(data, cursor=cursor)

    return cursor.fetchone()['id']


@_cache(
    key=lambda namespace, predicate, cursor=None: hashkey(namespace, predicate)
)
def predicate_id_from_raw(namespace, predicate, cursor=None):
    """
    Get a RDF predicate ID from string values, creating it if necessary.
    """
    cursor = check_cursor(cursor)

    namespace_id = rdf_namespace_id(namespace, cursor=cursor)

    return predicate_id(namespace_id, predicate, cursor=cursor)
