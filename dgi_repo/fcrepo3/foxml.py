"""
Functions to help with FOXML.
"""
import base64
from io import BytesIO

import requests
from lxml import etree
from psycopg2 import IntegrityError
from psycopg2.extensions import ISOLATION_LEVEL_READ_COMMITTED

import dgi_repo.database.write.datastreams as datastream_writer
import dgi_repo.database.read.datastreams as datastream_reader
import dgi_repo.database.write.repo_objects as object_writer
import dgi_repo.database.read.repo_objects as object_reader
import dgi_repo.database.filestore as filestore
from dgi_repo.database.read.repo_objects import object_info_from_raw
from dgi_repo.configuration import configuration as _config
from dgi_repo.fcrepo3.exceptions import ObjectExistsError
from dgi_repo.database.write.sources import upsert_user
from dgi_repo.database.utilities import check_cursor
from dgi_repo.database.write.log import upsert_log
from dgi_repo.database.read.sources import user
from dgi_repo import utilities as utils
from dgi_repo.fcrepo3 import relations

FOXML_NAMESPACE = 'info:fedora/fedora-system:def/foxml#'
SCHEMA_NAMESPACE = 'http://www.w3.org/2001/XMLSchema-instance'
SCHEMA_LOCATION = ('info:fedora/fedora-system:def/foxml# '
                   'http://www.fedora.info/definitions/1/0/foxml1-1.xsd')

OBJECT_STATE_MAP = {'A': 'Active', 'I': 'Inactive', 'D': 'Deleted'}
OBJECT_STATE_LABEL_MAP = {'Active': 'A', 'Inactive': 'I', 'Deleted': 'D'}


def import_foxml(xml, source, cursor=None):
    """
    Create a repo object out of a FOXML file.
    """
    foxml_importer = etree.XMLParser(target=FoxmlTarget(source, cursor=cursor))
    return etree.parse(xml, foxml_importer)


def create_default_dc_ds(object_id, pid, cursor=None):
    """
    Populate a minimal DC DS as Fedora does.
    """
    cursor = check_cursor(cursor, ISOLATION_LEVEL_READ_COMMITTED)

    dc_tree = etree.fromstring('''
        <oai_dc:dc xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/"
         xmlns:dc="http://purl.org/dc/elements/1.1/"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/oai_dc/
         http://www.openarchives.org/OAI/2.0/oai_dc.xsd">
          <dc:identifier></dc:identifier>
        </oai_dc:dc>
    ''')
    dc_tree[0].text = pid

    log = upsert_log('Automatically generated DC.').fetchone()[0]

    filestore.create_datastream_from_data(
        {
            'object': object_id,
            'dsid': 'DC',
            'label': 'DC Record',
            'log': log,
            'control_group': 'X'
        },
        etree.tostring(dc_tree),
        'application/xml',
        cursor=cursor
    )


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
    with foxml.element('{{{0}}}objectProperties'.format(FOXML_NAMESPACE)):
        property_element = '{{{0}}}property'.format(FOXML_NAMESPACE)

        state_attributes = {
            'VALUE': OBJECT_STATE_MAP[object_info['state']],
            'NAME': '{}{}'.format(relations.FEDORA_MODEL_NAMESPACE,
                                  relations.STATE_PREDICATE),
        }
        foxml.write(etree.Element(property_element, state_attributes))

        label_attributes = {
            'VALUE': object_info['label'] if object_info['label'] else '',
            'NAME': '{}{}'.format(relations.FEDORA_MODEL_NAMESPACE,
                                  relations.LABEL_PREDICATE),
        }
        foxml.write(etree.Element(property_element, label_attributes))

        user(object_info['owner'], cursor=cursor)
        owner_information = cursor.fetchone()
        owner_attributes = {
            'VALUE': owner_information['username'],
            'NAME': '{}{}'.format(relations.FEDORA_MODEL_NAMESPACE,
                                  relations.OWNER_PREDICATE),
        }
        foxml.write(etree.Element(property_element, owner_attributes))

        created_date_attributes = {
            'VALUE': object_info['created'].isoformat(),
            'NAME': '{}{}'.format(relations.FEDORA_MODEL_NAMESPACE,
                                  relations.CREATED_DATE_PREDICATE),
        }
        foxml.write(etree.Element(property_element,
                                  created_date_attributes))

        modified_date_attributes = {
            'VALUE': object_info['modified'].isoformat(),
            'NAME': '{}{}'.format(relations.FEDORA_VIEW_NAMESPACE,
                                  relations.LAST_MODIFIED_DATE_PREDICATE)
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
    cursor = datastream_reader.datastreams(object_info['id'])
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
    datastream_attributes = {
        'ID': datastream['dsid'],
        'STATE': datastream['state'],
        'CONTROL_GROUP': datastream['control_group'],
        'VERSIONABLE': str(datastream['versioned']).lower(),
    }
    with foxml.element('{{{0}}}datastream'.format(FOXML_NAMESPACE),
                       datastream_attributes):
        versions = list(datastream_reader.old_datastreams(datastream['id']))
        versions.append(datastream)

        for index, version in enumerate(versions):
            datastream_reader.resource(version['resource'], cursor=cursor)
            resource_info = cursor.fetchone()
            datastream_reader.mime(resource_info['mime'], cursor=cursor)
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

                datastream_reader.checksums(version['resource'],
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

                if datastream['control_group'] == 'X' and (not
                                                           inline_to_managed):
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
                                    'content?asOfDateTime={}').format(
                                        base_url,
                                        pid,
                                        datastream['dsid'],
                                        created
                                    ),
                        }

                    foxml.write(etree.Element(
                        '{{{0}}}contentLocation'.format(FOXML_NAMESPACE),
                        content_attributes
                    ))


def internalize_rels_int(relations_file, cursor=None):
    """
    Store the RELS_INT information in the DB.
    @todo implement.
    """
    cursor = check_cursor(cursor, ISOLATION_LEVEL_READ_COMMITTED)
    relation_tree = etree.parse(relations_file)
    return cursor


def internalize_rels_dc(relations_file, cursor=None):
    """
    Store the DC relation information in the DB.
    @todo implement.
    """
    cursor = check_cursor(cursor, ISOLATION_LEVEL_READ_COMMITTED)
    relation_tree = etree.parse(relations_file)
    return cursor


def internalize_rels_ext(relations_file, cursor=None):
    """
    Store the RELS_EXT information in the DB.
    @todo implement.
    """
    cursor = check_cursor(cursor, ISOLATION_LEVEL_READ_COMMITTED)
    relation_tree = etree.parse(relations_file)
    return cursor


class FoxmlTarget(object):
    """
    Parser target for incremental reading/ingest of FOXML.
    """

    def __init__(self, source, cursor=None):
        """
        Prep for use.
        """
        self.cursor = check_cursor(cursor, ISOLATION_LEVEL_READ_COMMITTED)
        self.source = source
        self.object_info = {}
        self.ds_info = {}
        self.object_id = None
        self.rels_int = None
        self.ds_file = None
        self.tree_builder = None
        self.dsid = None

    def start(self, tag, attributes):
        """
        Grab data from the start of tags.
        """
        # Start up a file for content.
        if (tag == '{{{0}}}xmlContent'.format(FOXML_NAMESPACE) and
                self.dsid != 'AUDIT'):
            self.tree_builder = etree.TreeBuilder()
        elif self.tree_builder is not None:
            self.tree_builder.start(tag, attributes)

        if tag == '{{{0}}}binaryContent'.format(FOXML_NAMESPACE):
            self.ds_file = utils.SpooledTemporaryFile()

        if tag == '{{{0}}}contentLocation'.format(FOXML_NAMESPACE):
            self.ds_info[self.dsid]['versions'][-1]['data_ref'] = attributes

        # Record current DSID.
        if tag == '{{{0}}}datastream'.format(FOXML_NAMESPACE):
            self.dsid = attributes['ID']
            self.ds_info[attributes['ID']] = {'versions': []}

        # Store DS info.
        if (tag == '{{{0}}}datastream'.format(FOXML_NAMESPACE) and
                self.dsid != 'AUDIT'):
            self.ds_info[self.dsid].update(attributes)
        if (tag == '{{{0}}}datastreamVersion'.format(FOXML_NAMESPACE) and
                self.dsid != 'AUDIT'):
            attributes['data'] = None
            attributes['data_ref'] = None
            attributes['checksums'] = []
            self.ds_info[self.dsid]['versions'].append(attributes)

        # Store checksum info.
        if tag == '{{{0}}}contentDigest'.format(FOXML_NAMESPACE):
            checksum = {
                'type': attributes['TYPE'],
                'checksum': attributes['DIGEST'],
            }
            self.ds_info[self.dsid]['versions'][-1]['checksums'].append(
                checksum
            )

        # Store object info.
        if tag == '{{{0}}}property'.format(FOXML_NAMESPACE):
            self.object_info[attributes['NAME']] = attributes['VALUE']
        if tag == '{{{0}}}digitalObject'.format(FOXML_NAMESPACE):
            self.object_info['PID'] = attributes['PID']

    def end(self, tag):
        """
        Internalize data at the end of tags.
        """
        # Create the object.
        if tag == '{{{0}}}objectProperties'.format(FOXML_NAMESPACE):
            raw_namespace, pid_id = utils.break_pid(self.object_info['PID'])
            object_reader.namespace_id(raw_namespace, cursor=self.cursor)
            try:
                namespace = self.cursor.fetchone()['id']
            except TypeError:
                # @XXX burns the first PID in a namespace.
                object_writer.get_pid_id(raw_namespace, cursor=self.cursor)
                namespace = self.cursor.fetchone()['id']

            raw_log = 'Object created through FOXML import.'
            upsert_log(raw_log, cursor=self.cursor)
            log = self.cursor.fetchone()[0]

            raw_owner = self.object_info['{}{}'.format(
                relations.FEDORA_MODEL_NAMESPACE,
                relations.OWNER_PREDICATE
            )]
            upsert_user({'name': raw_owner, 'source': self.source},
                        cursor=self.cursor)
            owner = self.cursor.fetchone()[0]

            created = self.object_info['{}{}'.format(
                relations.FEDORA_MODEL_NAMESPACE,
                relations.CREATED_DATE_PREDICATE
            )]

            modified = self.object_info['{}{}'.format(
                relations.FEDORA_VIEW_NAMESPACE,
                relations.LAST_MODIFIED_DATE_PREDICATE
            )]

            state = OBJECT_STATE_LABEL_MAP[self.object_info['{}{}'.format(
                relations.FEDORA_MODEL_NAMESPACE,
                relations.STATE_PREDICATE
            )]]

            label = self.object_info['{}{}'.format(
                relations.FEDORA_MODEL_NAMESPACE,
                relations.LABEL_PREDICATE
            )]

            object_writer.jump_pids(namespace, pid_id, cursor=self.cursor)
            try:
                object_writer.write_object(
                    {
                        'namespace': namespace,
                        'state': state,
                        'label': label,
                        'log': log,
                        'pid_id': pid_id,
                        'owner': owner,
                        'created': created,
                        'modified': modified,
                    },
                    cursor=self.cursor
                )
            except IntegrityError:
                raise ObjectExistsError(self.object_info['PID'])
            self.object_id = self.cursor.fetchone()[0]

        # Stash content.
        if (tag == '{{{0}}}xmlContent'.format(FOXML_NAMESPACE) and
                self.dsid != 'AUDIT'):
            base_element = self.tree_builder.close()
            xml_ds = BytesIO(etree.tostring(base_element))
            self.ds_info[self.dsid]['versions'][-1]['data'] = xml_ds
            self.tree_builder = None
        elif self.tree_builder is not None:
            self.tree_builder.end(tag)

        if tag == '{{{0}}}binaryContent'.format(FOXML_NAMESPACE):
            self.ds_file.seek(0)
            decoded_file = utils.SpooledTemporaryFile()
            base64.decode(self.ds_file, decoded_file)
            self.ds_file.close()
            self.ds_file = None
            decoded_file.seek(0)
            self.ds_info[self.dsid]['versions'][-1]['data'] = decoded_file

        # Store old and current DSs, passing off RELS/DC.
        if (tag == '{{{0}}}datastream'.format(FOXML_NAMESPACE) and
                self.dsid != 'AUDIT'):
            last_ds = self.ds_info[self.dsid]['versions'].pop()
            last_ds.update(self.ds_info[self.dsid])
            try:
                last_ds['actually_created'] = (self.ds_info[self.dsid]
                                               ['versions'][0]['CREATED'])
            except IndexError:
                last_ds['actually_created'] = last_ds['CREATED']

            # Populate relations.
            if self.dsid == 'DC':
                internalize_rels_dc(last_ds['data'], cursor=self.cursor)
            if self.dsid == 'RELS-EXT':
                internalize_rels_ext(last_ds['data'], cursor=self.cursor)
            if self.dsid == 'RELS-INT':
                self.rels_int = last_ds['data']
            self.cursor.fetchall()

            # Write DS.
            ds_db_id = self._create_ds(last_ds)

            # Write old DSs.
            for ds_version in self.ds_info[self.dsid]['versions']:
                ds_version.update(self.ds_info[self.dsid])
                ds_version['datastream'] = ds_db_id
                ds_version['actually_created'] = None
                ds_db_id = self._create_ds(ds_version, old=True)

            # Reset current datastream.
            self.dsid = None

    def _create_ds(self, ds, old=False):
        """
        Create a datastream on the current object.
        """
        prepared_ds = ds.copy()
        prepared_ds.update({
            'object': self.object_id,
            'dsid': self.dsid,
            'label': ds['LABEL'],
            'versioned': True if ds['VERSIONABLE'] == 'TRUE' else False,
            'control_group': ds['CONTROL_GROUP'],
            'state': ds['STATE'],
            'modified': ds['CREATED'],
            'created': ds['actually_created'],
            'committed': ds['CREATED'],
        })
        if prepared_ds['data'] is not None:
            # We already have data.
            filestore.create_datastream_from_data(
                prepared_ds,
                prepared_ds['data'],
                mime=prepared_ds['MIMETYPE'],
                checksums=prepared_ds['checksums'],
                old=old,
                cursor=self.cursor
            )
        elif prepared_ds['data_ref'] is not None:
            if prepared_ds['data_ref']['TYPE'] == 'URL':
                # Data will remain external.
                if prepared_ds['CONTROL_GROUP'] == 'R':
                    datastream_writer.upsert_mime(prepared_ds['MIMETYPE'],
                                                  cursor=self.cursor)
                    datastream_writer.upsert_resource(
                        {
                            'uri': prepared_ds['data_ref']['REF'],
                            'mime': self.cursor.fetchone()['id'],
                        },
                        cursor=self.cursor)
                    prepared_ds['resource'] = self.cursor.fetchone()['id']
                    datastream_writer.upsert_datastream(prepared_ds,
                                                        cursor=self.cursor)
                else:
                    # Data has been uploaded.
                    filestore.create_datastream_from_upload(
                        prepared_ds,
                        prepared_ds['data_ref']['REF'],
                        mime=prepared_ds['MIMETYPE'],
                        checksums=prepared_ds['checksums'],
                        old=old,
                        cursor=self.cursor
                    )
            elif prepared_ds['data_ref']['TYPE'] == 'INTERNAL_ID':
                # We need to fetch data.
                ds_resp = requests.get(
                    prepared_ds['data_ref']['REF'], stream=True
                )
                # @XXX: we should be able to avoid creating this file by
                # wrapping the raw attribute on the response to decode on read.
                ds_file = utils.SpooledTemporaryFile()
                for chunk in ds_resp.iter_content(
                        _config['download_chunk_size']):
                    ds_file.write(chunk)
                ds_file.seek(0)

                filestore.create_datastream_from_data(
                    prepared_ds,
                    ds_file,
                    mime=prepared_ds['MIMETYPE'],
                    checksums=prepared_ds['checksums'],
                    old=old,
                    cursor=self.cursor
                )

        ds_db_id = self.cursor.fetchone()['id']

        return ds_db_id

    def data(self, data):
        """
        Handle character data (datastream content).

        @XXX Documentation on buffer size doesn't exist; this may be an issue.
        """
        # ds_file is None unless we are writing to a file.
        if self.ds_file is not None:
            self.ds_file.write(data.encode())
        elif self.tree_builder is not None:
            self.tree_builder.data(data)

    def comment(self, data):
        """
        Maintain comments from Inline XML.
        """
        if self.tree_builder is not None:
            self.tree_builder.comment(data)

    def close(self):
        """
        Prep for next use.

        We retain the current cursor.
        """
        # Create a default DC DS.
        if self.object_id is not None:
            if 'DC' not in self.ds_info:
                create_default_dc_ds(self.object_id, self.object_info['PID'])
        # Create RELS-INT relations once all DSs are made.
        if self.rels_int is not None:
            internalize_rels_int(self.rels_int, cursor=self.cursor)
            self.cursor.fetchall()
        # Reset for next use.
        pid = self.object_info['PID']
        self.__init__(self.cursor, self.source)

        return pid
