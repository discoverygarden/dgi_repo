from lxml import etree

import dgi_repo.fcrepo3.relations as relations
import dgi_repo.database.read.repo_objects as object_reader
from dgi_repo.exceptions import ReferencedObjectDoesNotExistError
from dgi_repo.fcrepo3.utilities import (RDF_NAMESPACE, pid_from_fedora_uri,
                                        dsid_from_fedora_uri)
from dgi_repo.database.utilities import (DATASTREAM_RELATION_MAP,
                                         OBJECT_RELATION_MAP,
                                         LITERAL_RDF_OBJECT, URI_RDF_OBJECT,
                                         DATASTREAM_RDF_OBJECT,
                                         OBJECT_RDF_OBJECT, USER_RDF_OBJECT,
                                         ROLE_RDF_OBJECT, RAW_RDF_OBJECT)

def _element_predicate(relation):
    """
    Helper; get the namespace and localname tuple for the element's name.
    """
    qname = etree.QName(relation)
    return (qname.namespace, qname.localname)

def repo_object_rdf_object_from_element(relation, *args, **kwargs):
    return _require_mapped(relation, OBJECT_RELATION_MAP, *args, **kwargs)

def datastream_rdf_object_from_element(relation, *args, **kwargs):
    return _require_mapped(relation, DATASTREAM_RELATION_MAP, *args, **kwargs)

def _require_mapped(relation, rel_map, *args, **kwargs):
    """
    Map the object if we have specific table for it; otherwise, return raw.
    """
    predicate = _element_predicate(relation)
    if predicate in rel_map:
        return _rdf_object_from_element(predicate, relation, *args, **kwargs)

    try:
        return (URI_RDF_OBJECT, relation.attrib['{{{}}}resource'.format(RDF_NAMESPACE)])
    except KeyError:
        return (LITERAL_RDF_OBJECT, relation.text)

def _rdf_object_from_element(predicate, relation, source, cursor):
    """
    Pull out an RDF object form an RDF XML element.

    Returns a tuple of:
        - the resolved RDF object
        - the type; one of:
            - OBJECT_RDF_OBJECT
            - DATASTREAM_RDF_OBJECT
            - USER_RDF_OBJECT
            - ROLE_RDF_OBJECT
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
        if relation.tag in user_tags:
            upsert_user({'name': relation.text, 'source': source},
                        cursor=cursor)
            return (cursor.fetchone()['id'], USER_RDF_OBJECT)
        elif relation.tag in role_tags:
            upsert_role({'role': relation.text, 'source': source},
                        cursor=cursor)
            return (cursor.fetchone()['id'], ROLE_RDF_OBJECT)
        raise ValueError('Failed to resolve relationship %s with value %s.', predicate, relation.text)
    else:
        resource = relation.attrib['{{{}}}resource'.format(RDF_NAMESPACE)]

        pid = pid_from_fedora_uri(resource)
        dsid = dsid_from_fedora_uri(resource)
        if dsid:
            object_reader.object_info_from_raw(pid, cursor=cursor)
            object_id = cursor.fetchone()['id']
            datastream_reader.datastream_id(
                {'object_id': object_id, 'dsid': dsid},
                cursor=cursor
            )
            return (cursor.fetchone()['id'], DATASTREAM_RDF_OBJECT)
        elif pid:
            rdf_info = object_reader.object_info_from_raw(
                pid,
                cursor=cursor
            ).fetchone()
            try:
                return (rdf_info['id'], OBJECT_RDF_OBJECT)
            except TypeError as e:
                logger.error('Referenced object %s does not exist.', pid)
                raise ReferencedObjectDoesNotExistError(pid) from e

        raise ValueError('Failed to resolve relationship %s with value %s.', predicate, resource)
