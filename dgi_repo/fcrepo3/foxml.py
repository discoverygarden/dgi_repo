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


def generate_foxml(pid, archival=False, inline_to_managed=False, cursor=None):
    """
    Generate FOXML from a PID as a SpooledTemporaryFile.
    """
    foxml_file = utils.SpooledTemporaryFile()
    # Using a spooled temp file, double buffering will just eat memory.
    with etree.xmlfile(foxml_file, buffered=False, encoding="utf-8") as foxml:
        foxml.write_declaration(version='1.0')
        populate_foxml_etree(foxml, pid, cursor=cursor, archival=archival)
        return foxml_file
    return None


def populate_foxml_etree(foxml, pid, archival=False, inline_to_managed=False,
                         cursor=None,):
    """
    Add FOXML from a PID into an lxml etree.
    """
    from dgi_repo.database.read.repo_objects import object_info_from_raw

    pid_namespace, pid_id = utils.break_pid(pid)

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
        populate_foxml_datastreams(foxml, object_info, archival,
                                   inline_to_managed, cursor)


def populate_foxml_properties(foxml, object_info, cursor=None):
    """
    Add FOXML properties into an lxml etree.
    """
    from dgi_repo.database.read.sources import user
    from dgi_repo.fcrepo3 import relations

    object_state_map = {'A': 'Active', 'I': 'Inactive', 'D': 'Deleted'}

    with foxml.element('{{{0}}}objectProperties'.format(FOXML_NAMESPACE)):

        elements = []
        property_element = '{{{0}}}property'.format(FOXML_NAMESPACE)

        state_attributes = {
            'VALUE': object_state_map[object_info['state']],
            'NAME': '{}state'.format(relations.FEDORA_MODEL_NAMESPACE),
        }
        elements.append(etree.Element(property_element, state_attributes))

        label_attributes = {
            'VALUE': object_info['label'] if object_info['label'] else '',
            'NAME': '{}label'.format(relations.FEDORA_MODEL_NAMESPACE),
        }
        elements.append(etree.Element(property_element, label_attributes))

        user(object_info['owner'], cursor=cursor)
        owner_information = cursor.fetchone()
        owner_attributes = {
            'VALUE': owner_information['username'],
            'NAME': '{}ownerId'.format(relations.FEDORA_MODEL_NAMESPACE),
        }
        elements.append(etree.Element(property_element, owner_attributes))

        created_date_attributes = {
            'VALUE': object_info['created'].isoformat(),
            'NAME': '{}createdDate'.format(relations.FEDORA_MODEL_NAMESPACE),
        }
        elements.append(etree.Element(property_element,
                                      created_date_attributes))

        modified_date_attributes = {
            'VALUE': object_info['modified'].isoformat(),
            'NAME': 'info:fedora/fedora-system:def/view#lastModifiedDate',
        }
        elements.append(etree.Element(property_element,
                                      modified_date_attributes))

        for element in elements:
            foxml.write(element)


def populate_foxml_datastreams(foxml, object_info, archival=False,
                               inline_to_managed=False, cursor=None):
    """
    Add FOXML datastreams into an lxml etree.
    """
    cursor = read_datastreams.datastreams(object_info['id'])
    datastream_list = cursor.fetchall()

    for datastream in datastream_list:
        populate_foxml_datastream(foxml, datastream, archival,
                                  inline_to_managed, cursor)


def populate_foxml_datastream(foxml, datastream, archival=False,
                              inline_to_managed=False, cursor=None):
    """
    Add FOXML datastreams into an lxml etree.
    """
    from dgi_repo.database.filestore import uri_size

    datastream_attributes = {
        'ID': datastream['dsid'],
        'STATE': datastream['state'],
        'CONTROL_GROUP': datastream['control_group'],
        'VERSIONABLE': str(datastream['versioned']).lower(),
    }
    with foxml.element('{{{0}}}datastream'.format(FOXML_NAMESPACE),
                       datastream_attributes):
        versions = [datastream]
        versions.extend(read_datastreams.old_datastreams(datastream['id']))

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
            if datastream['control_group'] is not 'R':
                size = uri_size(resource_info['uri'])
                version_attributes['SIZE'] = str(size)

            version_element = etree.Element(
                '{{{0}}}datastreamVersion'.format(FOXML_NAMESPACE),
                version_attributes
            )

            read_datastreams.checksums(version['resource_id'], cursor=cursor)
            checksums = cursor.fetchall()
            for checksum in checksums:
                etree.SubElement(
                    version_element,
                    '{{{0}}}datastreamDigest'.format(FOXML_NAMESPACE),
                    {'TYPE': checksum['type'], 'DIGEST': checksum['checksum']}
                )

            # @todo: Handle inline.
            # @todo: Handle content location.
            # @todo: Handle binary content.

            foxml.write(version_element)
