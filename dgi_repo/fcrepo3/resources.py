"""
Falcon Resource implementations.
"""

import base64
import logging

import dgi_repo.database.write.repo_objects as object_writer
from dgi_repo.database import filestore
from dgi_repo import utilities as utils
from dgi_repo.fcrepo3 import api, foxml
from dgi_repo.fcrepo3.exceptions import ObjectExistsError
from dgi_repo.configuration import configuration as _config
from dgi_repo.database.utilities import get_connection
import dgi_repo.database.read.datastreams as datastream_reader
import dgi_repo.database.read.repo_objects as object_reader

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
                control_group, uri, mime = self._get_info(
                    kwargs['pid'],
                    kwargs['dsID']
                )
                is_redirect = control_group == 'R'

                with xf.element('MIMEType'):
                    xf.write('application/fedora-redirect' if is_redirect
                             else mime)
                with xf.element('stream'):
                    if is_redirect:
                        xf.write(base64.encodebytes(uri.encode()))
                    else:
                        with open(filestore.resolve_uri(uri), 'rb') as ds_file:
                            base64.encode(ds_file, xf)
                with xf.element('header'):
                    # Element doesn't appear to be necessary, nor appear to
                    # contain anything necessary here... Unclear as to what
                    # _might_ be supposed to be here.
                    pass

    def _get_info(self, pid, dsid):
        """
        Get the MIME-type and URI of the given datastream.

        Returns:
            A three-tuple comprising:
            - the datastream control group
            - the URI of the resource the datastream represents
            - the MIME type of the datastream's resource
        """
        with get_connection() as conn, conn.cursor() as cursor:
            datastream_info = datastream_reader.datastream_from_raw(
                pid,
                dsid,
                cursor=cursor
            ).fetchone()
            resource_info = datastream_reader.resource(
                datastream_info['resource'],
                cursor=cursor
            ).fetchone()
            mime_info = datastream_reader.mime(
                resource_info['mime'],
                cursor=cursor
            ).fetchone()

            return (
                datastream_info['control_group'],
                resource_info['uri'],
                mime_info['mime']
            )


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
    """
    Povide the list datastreams endpoint.
    """
    def _get_datastreams(self, pid, asOfDateTime=None):
        """
        Retrieve the list of datastreams.

        @XXX: not respecting asOfDateTime as we don't use it.
        """
        with get_connection() as conn, conn.cursor() as cursor:
            object_info = object_reader.object_info_from_raw(
                pid,
                cursor=cursor
            ).fetchone()
            try:
                object_id = object_info['id']
            except TypeError as e:
                raise ObjectExistsError(pid) from e
            raw_datastreams = datastream_reader.datastreams(
                object_id,
                cursor=cursor
            ).fetchall()
            datastreams = []
            for datastream in raw_datastreams:
                mime = datastream_reader.mime_from_resource(
                    datastream['resource'],
                    cursor=cursor
                ).fetchone()
                datastreams.append({
                    'dsid': datastream['dsid'],
                    'label': datastream['label'],
                    'mimeType': mime['mime'] if mime is not None else '',
                })
            return datastreams


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
