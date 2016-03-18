"""
Functions to help with FOXML.
"""

from lxml import etree

import dgi_repo.database.read.datastreams as read_datastreams
from dgi_repo import utilities as utils

FOXML_NAMESPACE = 'info:fedora/fedora-system:def/foxml#'
SCHEMA_NAMESPACE = 'http://www.w3.org/2001/XMLSchema-instance'
SCHEMA_LOCATION = ('info:fedora/fedora-system:def/foxml# '
                   'http://www.fedora.info/definitions/1/0/foxml1-1.xsd')


def generate_foxml(pid, base_url='http://localhost:8080/fedora',
                   archival=False, inline_to_managed=False, cursor=None):
    """
    Generate FOXML from a PID as a SpooledTemporaryFile.
    """
    foxml_file = utils.SpooledTemporaryFile()
    # Using a spooled temp file, double buffering will just eat memory.
    with etree.xmlfile(foxml_file, buffered=False, encoding="utf-8") as foxml:
        foxml.write_declaration(version='1.0')
        populate_foxml_etree(foxml, pid, base_url=base_url, archival=archival,
                             inline_to_managed=inline_to_managed,
                             cursor=cursor)
        return foxml_file
    return None


def populate_foxml_etree(foxml, pid, base_url='http://localhost:8080/fedora',
                         archival=False, inline_to_managed=False, cursor=None):
    """
    Add FOXML from a PID into an lxml etree.
    """
    from dgi_repo.database.read.repo_objects import object_info_from_raw

    attributes = {
        'VERSION': '1.1',
        'PID': pid,
        '{{{}}}schemaLocation'.format(SCHEMA_NAMESPACE): SCHEMA_LOCATION
    }

    with foxml.element('{{{0}}}digitalObject'.format(FOXML_NAMESPACE),
                       **attributes):
        cursor = object_info_from_raw(pid, cursor=cursor)
        object_info = cursor.fetchone()
        populate_foxml_properties(foxml, object_info, cursor=cursor)
        populate_foxml_datastreams(foxml, pid, object_info, base_url, archival,
                                   inline_to_managed, cursor)


def populate_foxml_properties(foxml, object_info, cursor=None):
    """
    Add FOXML properties into an lxml etree.
    """
    from dgi_repo.database.read.sources import user
    from dgi_repo.fcrepo3 import relations

    object_state_map = {'A': 'Active', 'I': 'Inactive', 'D': 'Deleted'}

    with foxml.element('{{{0}}}objectProperties'.format(FOXML_NAMESPACE)):
        property_element = '{{{0}}}property'.format(FOXML_NAMESPACE)

        state_attributes = {
            'VALUE': object_state_map[object_info['state']],
            'NAME': '{}state'.format(relations.FEDORA_MODEL_NAMESPACE),
        }
        foxml.write(etree.Element(property_element, state_attributes))

        label_attributes = {
            'VALUE': object_info['label'] if object_info['label'] else '',
            'NAME': '{}label'.format(relations.FEDORA_MODEL_NAMESPACE),
        }
        foxml.write(etree.Element(property_element, label_attributes))

        user(object_info['owner'], cursor=cursor)
        owner_information = cursor.fetchone()
        owner_attributes = {
            'VALUE': owner_information['username'],
            'NAME': '{}ownerId'.format(relations.FEDORA_MODEL_NAMESPACE),
        }
        foxml.write(etree.Element(property_element, owner_attributes))

        created_date_attributes = {
            'VALUE': object_info['created'].isoformat(),
            'NAME': '{}createdDate'.format(relations.FEDORA_MODEL_NAMESPACE),
        }
        foxml.write(etree.Element(property_element,
                                  created_date_attributes))

        modified_date_attributes = {
            'VALUE': object_info['modified'].isoformat(),
            'NAME': 'info:fedora/fedora-system:def/view#lastModifiedDate',
        }
        foxml.write(etree.Element(property_element,
                                  modified_date_attributes))


def populate_foxml_datastreams(foxml, pid, object_info,
                               base_url='http://localhost:8080/fedora',
                               archival=False, inline_to_managed=False,
                               cursor=None):
    """
    Add FOXML datastreams into an lxml etree.
    """
    cursor = read_datastreams.datastreams(object_info['id'])
    datastream_list = cursor.fetchall()

    for datastream in datastream_list:
        populate_foxml_datastream(foxml, pid, datastream, base_url=base_url,
                                  archival=archival,
                                  inline_to_managed=inline_to_managed,
                                  cursor=cursor)


def populate_foxml_datastream(foxml, pid, datastream,
                              base_url='http://localhost:8080/fedora',
                              archival=False, inline_to_managed=False,
                              cursor=None):
    """
    Add a FOXML datastream into an lxml etree.
    """
    import base64

    import dgi_repo.database.filestore as filestore

    datastream_attributes = {
        'ID': datastream['dsid'],
        'STATE': datastream['state'],
        'CONTROL_GROUP': datastream['control_group'],
        'VERSIONABLE': str(datastream['versioned']).lower(),
    }
    with foxml.element('{{{0}}}datastream'.format(FOXML_NAMESPACE),
                       datastream_attributes):
        versions = list(read_datastreams.old_datastreams(datastream['id']))
        versions.append(datastream)

        for index, version in enumerate(versions):
            read_datastreams.resource(version['resource_id'], cursor=cursor)
            resource_info = cursor.fetchone()
            read_datastreams.mime(resource_info['mime'], cursor=cursor)
            mime_info = cursor.fetchone()
            try:
                created = version['committed'].isoformat()
            except KeyError:
                created = datastream['created'].isoformat()

            version_attributes = {
                'ID': '{}.{}'.format(datastream['dsid'], index),
                'LABEL': version['label'] if version['label'] else '',
                'CREATED': created,
                'MIMETYPE': mime_info['mime'],
            }
            if datastream['control_group'] != 'R':
                size = filestore.uri_size(resource_info['uri'])
                version_attributes['SIZE'] = str(size)

            with foxml.element('{{{0}}}datastreamVersion'.format(
                FOXML_NAMESPACE), version_attributes):

                read_datastreams.checksums(version['resource_id'],
                                           cursor=cursor)
                checksums = cursor.fetchall()
                for checksum in checksums:
                    foxml.write(etree.Element(
                        '{{{0}}}datastreamDigest'.format(FOXML_NAMESPACE),
                        {
                            'TYPE': checksum['type'],
                            'DIGEST': checksum['checksum']
                        }
                    ))

                if datastream['control_group'] == 'X' and not inline_to_managed:
                    content_element = etree.Element(
                        '{{{0}}}xmlContent'.format(FOXML_NAMESPACE)
                    )
                    uri = filestore.resolve_uri(resource_info['uri'])
                    xml_etree = etree.parse(uri)
                    content_element.append(xml_etree.getroot())
                    foxml.write(content_element)
                elif datastream['control_group'] in ['M', 'X'] and archival:
                    uri = filestore.resolve_uri(resource_info['uri'])
                    with open(uri, 'rb') as ds_file:
                        with foxml.element('{{{0}}}binaryContent'.format(
                                           FOXML_NAMESPACE)):
                            base64.encode(ds_file, foxml)
                else:
                    if datastream['control_group'] == 'R':
                        content_attributes = {
                            'TYPE': 'URL',
                            'REF': resource_info['uri'],
                        }
                    else:
                        content_attributes = {
                            'TYPE': 'INTERNAL_ID',
                            'REF': ('{}/objects/{}/datastreams/{}/'
                                    'content?asOfDateTime={}').format(base_url,
                                        pid, datastream['dsid'], created),
                        }

                    foxml.write(etree.Element(
                        '{{{0}}}contentLocation'.format(FOXML_NAMESPACE),
                        content_attributes
                    ))
