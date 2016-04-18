"""
Falcon Resource implementations.
"""

import base64
import logging
import io

import dgi_repo.database.write.repo_objects as object_writer
from dgi_repo.database import filestore
from dgi_repo import utilities as utils
from dgi_repo.fcrepo3 import api, foxml
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
    def _respond(self, xf, method, kwargs):
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
    def on_get(self, req, resp, pid):
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
    def on_post(self, req, resp, pid, dsid):
        super().on_post(req, resp, pid, dsid)
        # TODO: Persist the new datastream.
        pass

    def on_put(self, req, resp, pid, dsid):
        super().on_put(req, resp, pid, dsid)
        # TODO: Commit the modification to the datastream.
        pass

    def on_delete(self, req, resp, pid, dsid):
        super().on_delete(req, resp, pid, dsid)
        # TODO: Purge the datastream (or range of versions).
        pass

    def _get_datastream_info(self, pid, dsid, asOfDateTime=None, **kwargs):
        # TODO: Get the ds* values in a dict, to build the datastream profile.
        pass


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
