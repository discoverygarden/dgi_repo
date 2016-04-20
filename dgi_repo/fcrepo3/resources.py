"""
Falcon Resource implementations.
"""

import base64
import logging
import io

from psycopg2.extensions import ISOLATION_LEVEL_READ_COMMITTED

import dgi_repo.database.write.repo_objects as object_writer
import dgi_repo.database.read.repo_objects as object_reader
import dgi_repo.database.delete.datastreams as ds_purger
import dgi_repo.database.read.datastreams as ds_reader
from dgi_repo.database import filestore
from dgi_repo import utilities as utils
from dgi_repo.fcrepo3 import api, foxml
from dgi_repo.fcrepo3.utilities import resolve_log, create_ds
from dgi_repo.configuration import configuration as _config
from dgi_repo.database.utilities import get_connection

logger = logging.getLogger(__name__)

route_map = {
    '/describe': api.DescribeResource
}


def route(*routes):
    """
    Helper pull all our routes together.
    """
    def add(cls):
        for route in routes:
            route_map[route] = cls
        return cls

    return add


@route('/services/access')
class SoapAccessResource(api.FakeSoapResource):
    def _respond(self, xf, method, kwargs):
        if method == '{{{0}}}getDatastreamDissemination'.format(
                api.FEDORA_TYPES_URI):
            with xf.element('{{{0}}}getDatastreamDisseminationResponse'.format(
                    api.FEDORA_TYPES_URI)):
                with xf.element('MIMEType'):
                    # TODO: Write the "real" MIME-type.
                    xf.write('application/octet-stream')
                if True:
                    # TODO: Make condition: only if datastream is managed or
                    # externally referenced.
                    with xf.element('stream'):
                        datastream = io.BytesIO(b"""<?xml version="1.0" encoding="UTF-8"?>
<mods xmlns="http://www.loc.gov/mods/v3">
    <titleInfo>
        <title>lol title</title>
    </titleInfo>
</mods>
""")
                        # TODO: Replace "datastream" with correct file-like
                        # object.
                        base64.encode(datastream, xf)
                with xf.element('header'):
                    # Element doesn't appear to be necessary, nor appear to
                    # contain anything necessary here... Unclear as to what
                    # _might_ be supposed to be here.
                    pass


@route('/services/management')
class SoapManagementResource(api.FakeSoapResource):
    """
    Provide the services/management endpoint.
    """

    def _respond(self, xf, method, kwargs):
        """
        Set a base64 encoded FOXML export.
        """
        if method == '{{{0}}}export'.format(api.FEDORA_TYPES_URI):
            with xf.element('{{{0}}}exportResponse'.format(
                    api.FEDORA_TYPES_URI)):
                with xf.element('objectXML'):
                    base64.encode(foxml.generate_foxml(kwargs['pid']), xf)
            logger.info('Exporting: %s.', kwargs['pid'])


@route('/upload')
class UploadResource(api.UploadResource):
    """
    Provide the upload endpoint.
    """

    def _store(self, uploaded_file):
        """
        Store a file as an upload.
        """

        return filestore.stash(uploaded_file)[1]


@route('/objects/nextPID')
class PidResource(api.PidResource):
    """
    Provide the get next PID endpoint.
    """

    def _get_pids(self, numPIDs=1, namespace=None):
        """
        Get a set number of PIDs from a namespace.
        """
        if namespace is None:
            namespace = _config['default_namespace']

        namespace_info = object_writer.get_pid_ids(namespace, numPIDs)
        highest_id = namespace_info.fetchone()['highest_id']
        pids = []

        for pid_id in range(highest_id - numPIDs + 1, highest_id + 1):
            pids.append(utils.make_pid(namespace, pid_id))

        if numPIDs == 1:
            pids_to_log = pids
        else:
            pids_to_log = '{}-{}'.format(pids[0], pids[-1])
        logger.info('Getting new PID(s): %s.', pids_to_log)

        return pids


@route('/objects/{pid}/export', '/objects/{pid}/objectXML')
class ObjectResourceExport(api.ObjectResourceExport):
    """
    Provide export and objectXML endpoints.
    """
    def on_get(self, req, resp, pid):
        """
        Provide a FOXML export.
        """
        super().on_get(req, resp, pid)
        archival = req.get_param('context') == 'archive'
        with get_connection() as conn:
            with conn.cursor() as cursor:
                resp.stream = foxml.generate_foxml(pid, archival=archival,
                                                   cursor=cursor)
                logger.info('Exporting: %s.', pid)


@route('/objects/{pid}/datastreams')
class DatastreamListResource(api.DatastreamListResource):
    def _get_datastreams(self, pid, asOfDateTime=None):
        # TODO: Get actual datastreams from the object.
        return [{
            'dsid': 'NOT_A_DATASTREAM',
            'label': 'Stop looking!',
            'mimeType': 'application/octet-stream'
        }]


@route('/objects/{pid}/datastreams/{dsid}')
class DatastreamResource(api.DatastreamResource):
    """
    Provide the datastream CRUD endpoints.
    """

    def on_post(self, req, resp, pid, dsid):
        """
        Persist the new datastream.
        """
        super().on_post(req, resp, pid, dsid)
        with get_connection(ISOLATION_LEVEL_READ_COMMITTED) as conn:
            with conn.cursor() as cursor:
                control_group = req.get_param('controlGroup', default='M')
                ds_location = req.get_param('dsLocation')
                data_ref = None
                data = None
                if ds_location is not None:
                    if control_group == 'R':
                        data_ref = {
                            'TYPE': 'URL',
                            'REF': ds_location,
                        }
                    else:
                        data_ref = {
                            'TYPE': 'INTERNAL_ID',
                            'REF': ds_location,
                        }
                else:
                    data = req.get_param('file').file
                checksums = None
                checksum = req.get_param('checksum')
                if checksum is not None:
                    checksums.append({
                        'checksum': checksum,
                        'type': req.get_param('checksumType'),
                    }),
                object_reader.object_id_from_raw(pid, cursor=cursor)
                create_ds(
                    {
                        'dsid': dsid,
                        'object': cursor.fetchone()['id'],
                        'log': resolve_log(req, cursor),
                        'control_group': control_group,
                        'label': req.get_param('dsLabel'),
                        'versioned': req.get_param('versionable') != 'false',
                        'state': req.get_param('dsState', default='A'),
                        'checksums': checksums,
                        'mimetype': req.get_param('mimeType'),
                        'data_ref': data_ref,
                        'data': data,
                    },
                    cursor=cursor
                )
                logger.info('Created DS %s:%s', pid, dsid)

    def on_put(self, req, resp, pid, dsid):
        """
        Commit the modification to the datastream.

        @TODO: commit DS.
        @TODO: create old versions.
        """
        super().on_put(req, resp, pid, dsid)
        with get_connection() as conn:
            with conn.cursor() as cursor:
                log = resolve_log(req, cursor)
                logger.info('Updated DS %s:%s', pid, dsid)

    def on_delete(self, req, resp, pid, dsid):
        """
        Purge the datastream (or range of versions).

        @TODO: handle startDT/endDT
        @TODO: handle logMessage when audit is dealt with.
        """
        super().on_delete(req, resp, pid, dsid)
        with get_connection() as conn:
            with conn.cursor() as cursor:
                ds_purger.delete_datastream_from_raw(pid, dsid, cursor=cursor)
                logger.info('Purged DS %s:%s', pid, dsid)

    def _get_datastream_info(self, pid, dsid, asOfDateTime=None, **kwargs):
        """
        Get the ds* values in a dict, to build the datastream profile.

        @TODO: handle as of date time.
        """
        with get_connection() as conn:
            with conn.cursor() as cursor:
                ds_reader.datastream_from_raw(pid, dsid, cursor=cursor)
                ds_info = cursor.fetchone()
                if ds_info is None:
                    return None
                versionable = 'true' if ds_info['versioned'] else 'false'
                location = None
                location_type = 'INTERNAL_ID'
                mime = None
                checksum = 'none'
                checksum_type = 'DISABLED'
                size = None
                if ds_info['resource'] is not None:
                    ds_reader.resource(ds_info['resource'], cursor=cursor)
                    resource_info = cursor.fetchone()
                    if resource_info is not None:
                        location = resource_info['uri']
                        if ds_info['control_group'] != 'R':
                            size = filestore.uri_size(resource_info['uri'])
                        else:
                            location_type = 'URL'

                        ds_reader.mime(resource_info['mime'], cursor=cursor)
                        mime = cursor.fetchone()['mime']

                        ds_reader.checksums(ds_info['resource'], cursor=cursor)
                        checksum_info = cursor.fetchone()
                        if checksum_info is not None:
                            checksum = checksum_info['checksum']
                            checksum_type = checksum_info['type']
                            cursor.fetchall()
                return {
                    'dsLabel': ds_info['label'],
                    'dsCreateDate': ds_info['modified'].isoformat(),
                    'dsState': ds_info['state'],
                    'dsMime': mime,
                    'dsConrolGroup': ds_info['control_group'],
                    'dsVersionable': versionable,
                    'dsChecksumType': checksum_type,
                    'dsChecksum': checksum,
                    'dsSize': size,
                    'dsLocation': location,
                    'dsLocationType': location_type,
                }


@route('/objects/{pid}/datastreams/{dsid}/content')
class DatastreamDisseminationResource(api.DatastreamDisseminationResource):
    def on_get(self, req, resp, pid, dsid):
        super().on_get(req, resp, pid, dsid)
        # TODO: Dump, redirect or pipe datastream content, based on datastream
        # "content group".
        pass


@route('/objects/{pid}/datastreams/{dsid}/history')
class DatastreamHistoryResource(api.DatastreamHistoryResource):
    def _get_datastream_versions(self, pid, dsid, startDT=None, endDT=None):
        # TODO: Get an iterable of datastream versions.
        pass
