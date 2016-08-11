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


# Create caches.
object_ns_cache = LRUCache(maxsize=_config['database']['cache_size'])
rdf_ns_cache = LRUCache(maxsize=_config['database']['cache_size'])
predicate_cache = LRUCache(maxsize=_config['database']['cache_size'])
raw_predicate_cache = LRUCache(maxsize=_config['database']['cache_size'])


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
    Clear all the caches.
    """
    repo_object_namespace_id.cache_clear()
    rdf_namespace_id.cache_clear()
    predicate_id.cache_clear()
    predicate_id_from_raw.cache_clear()


@no_none_cache
@cached(object_ns_cache, key=lambda namespace, cursor=None: hashkey(namespace))
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
@cached(rdf_ns_cache, key=lambda namespace, cursor=None: hashkey(namespace))
def rdf_namespace_id(namespace, cursor=None):
    """
    Get a RDF namespace ID, creating it if necessary.
    """
    cursor = relations_reader.namespace_id(namespace, cursor=cursor)

    if not cursor.rowcount:
        relations_writer.upsert_namespace(namespace, cursor=cursor)

    return cursor.fetchone()['id']


@no_none_cache
@cached(
    predicate_cache,
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


@no_none_cache
@cached(
    raw_predicate_cache,
    key=lambda namespace, predicate, cursor=None: hashkey(namespace, predicate)
)
def predicate_id_from_raw(namespace, predicate, cursor=None):
    """
    Get a RDF predicate ID from string values, creating it if necessary.
    """
    cursor = check_cursor(cursor)

    namespace_id = rdf_namespace_id(namespace, cursor=cursor)

    return predicate_id(namespace_id, predicate, cursor=cursor)


# Add cache_clear tooling to functions.
repo_object_namespace_id.cache_clear = lambda: object_ns_cache.clear()
rdf_namespace_id.cache_clear = lambda: rdf_ns_cache.clear()
predicate_id.cache_clear = lambda: predicate_cache.clear()
predicate_id_from_raw.cache_clear = lambda: raw_predicate_cache.clear()
