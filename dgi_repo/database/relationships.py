"""
Relationship resolution.
"""
import logging

from lxml import etree

import dgi_repo.fcrepo3.relations as relations
import dgi_repo.database.read.repo_objects as object_reader
import dgi_repo.database.read.datastreams as datastream_reader
import dgi_repo.database.write.sources as source_writer
from dgi_repo.exceptions import (ReferencedObjectDoesNotExistError,
                                 ReferencedDatastreamDoesNotExist)
from dgi_repo.fcrepo3.utilities import (RDF_NAMESPACE, pid_from_fedora_uri,
                                        dsid_from_fedora_uri)
from dgi_repo.database.utilities import (DATASTREAM_RELATION_MAP,
                                         OBJECT_RELATION_MAP,
                                         LITERAL_RDF_OBJECT, URI_RDF_OBJECT,
                                         DATASTREAM_RDF_OBJECT,
                                         OBJECT_RDF_OBJECT, USER_RDF_OBJECT,
                                         ROLE_RDF_OBJECT)

logger = logging.getLogger(__name__)

def _element_predicate(relation):
    """
    Helper; get the namespace and localname tuple for the element's name.
    """
    qname = etree.QName(relation)
    return (qname.namespace, qname.localname)


def repo_object_rdf_object_from_element(relation, *args, **kwargs):
    """
    Resolve a repo object's relationship object.
    """
    return _require_mapped(relation, OBJECT_RELATION_MAP, *args, **kwargs)


def datastream_rdf_object_from_element(relation, *args, **kwargs):
    """
    Resolve a datastream's relationship object.
    """
    return _require_mapped(relation, DATASTREAM_RELATION_MAP, *args, **kwargs)


def _require_mapped(relation, rel_map, *args, **kwargs):
    """
    Map the object if we have specific table for it; otherwise, return raw.
    """
    predicate = _element_predicate(relation)
    if predicate in rel_map:
        return _rdf_object_from_element(predicate, relation, *args, **kwargs)

    try:
        return (relation.attrib['{{{}}}resource'.format(RDF_NAMESPACE)],
                URI_RDF_OBJECT)
    except KeyError:
        if relation.text:
            return (relation.text, LITERAL_RDF_OBJECT)
        else:
            raise ValueError(('Empty relationship node; we require either a '
                              'populated text node or resource reference for '
                              '%s.'), predicate)


def _rdf_object_from_element(predicate, relation, source, cursor):
    """
    Pull out an RDF object form an RDF XML element.

    Returns:
        A tuple of:
        - the resolved RDF object
        - the type; one of:
            - OBJECT_RDF_OBJECT
            - DATASTREAM_RDF_OBJECT
            - USER_RDF_OBJECT
            - ROLE_RDF_OBJECT

    Raises:
        ReferencedObjectDoesNotExistError: If the value appeared to
            reference a repo object, but it could not be found.
        ValueError: If the value could not be resolved in general.
    """
    user_tags = frozenset([
        (relations.ISLANDORA_RELS_EXT_NAMESPACE,
         relations.IS_VIEWABLE_BY_USER_PREDICATE),
        (relations.ISLANDORA_RELS_INT_NAMESPACE,
         relations.IS_VIEWABLE_BY_USER_PREDICATE),
        (relations.ISLANDORA_RELS_EXT_NAMESPACE,
         relations.IS_MANAGEABLE_BY_USER_PREDICATE),
        (relations.ISLANDORA_RELS_INT_NAMESPACE,
         relations.IS_MANAGEABLE_BY_USER_PREDICATE),
    ])
    role_tags = frozenset([
        (relations.ISLANDORA_RELS_EXT_NAMESPACE,
         relations.IS_VIEWABLE_BY_ROLE_PREDICATE),
        (relations.ISLANDORA_RELS_INT_NAMESPACE,
         relations.IS_VIEWABLE_BY_ROLE_PREDICATE),
        (relations.ISLANDORA_RELS_EXT_NAMESPACE,
         relations.IS_MANAGEABLE_BY_ROLE_PREDICATE),
        (relations.ISLANDORA_RELS_INT_NAMESPACE,
         relations.IS_MANAGEABLE_BY_ROLE_PREDICATE),
    ])
    if relation.text:
        if predicate in user_tags:
            cursor = source_writer.upsert_user({'name': relation.text,
                                                'source': source},
                                               cursor=cursor)
            return (cursor.fetchone()['id'], USER_RDF_OBJECT)
        elif predicate in role_tags:
            cursor = source_writer.upsert_role({'role': relation.text,
                                                'source': source},
                                               cursor=cursor)
            return (cursor.fetchone()['id'], ROLE_RDF_OBJECT)
        raise ValueError('Failed to resolve relationship %s with value %s.',
                         predicate, relation.text)
    else:
        resource = relation.attrib['{{{}}}resource'.format(RDF_NAMESPACE)]

        pid = pid_from_fedora_uri(resource)
        dsid = dsid_from_fedora_uri(resource)
        if pid:
            cursor = object_reader.object_info_from_raw(pid, cursor=cursor)
            try:
                object_id = cursor.fetchone()['id']
            except TypeError as e:
                logger.error('Referenced object %s does not exist.', pid)
                raise ReferencedObjectDoesNotExistError(pid) from e
            else:
                if dsid:
                    try:
                        cursor = datastream_reader.datastream_id(
                            {'object_id': object_id, 'dsid': dsid},
                            cursor=cursor
                        )
                        return (cursor.fetchone()['id'], DATASTREAM_RDF_OBJECT)
                    except TypeError as e:
                        logger.error(
                            'Referenced datastream %s/%s does not exist.',
                            pid,
                            dsid
                        )
                        raise ReferencedDatastreamDoesNotExist(pid,
                                                               dsid) from e

                return (object_id, OBJECT_RDF_OBJECT)

        raise ValueError('Failed to resolve relationship %s with value %s.',
                         predicate, resource)
