"""
Falcon Resource implementations.
"""
import datetime
import base64
import logging

import falcon

import dgi_repo.database.write.repo_objects as object_writer
import dgi_repo.fcrepo3.utilities as fedora_utils
import dgi_repo.database.read.datastreams as ds_reader
import dgi_repo.database.read.repo_objects as object_reader
from dgi_repo.database import filestore
from dgi_repo import utilities as utils
from dgi_repo.fcrepo3 import api, foxml
from dgi_repo.fcrepo3.exceptions import ObjectDoesNotExistError
from dgi_repo.fcrepo3.exceptions import DatastreamDoesNotExistError
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
            datastream_info = ds_reader.datastream_from_raw(
                pid,
                dsid,
                cursor=cursor
            ).fetchone()
            resource_info = ds_reader.resource(
                datastream_info['resource'],
                cursor=cursor
            ).fetchone()
            mime_info = ds_reader.mime(
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
        """
        with get_connection() as conn, conn.cursor() as cursor:
            object_info = object_reader.object_info_from_raw(
                pid,
                cursor=cursor
            ).fetchone()
            try:
                object_id = object_info['id']
            except TypeError as e:
                raise ObjectDoesNotExistError(pid) from e
            raw_datastreams = ds_reader.datastreams(
                object_id,
                cursor=cursor
            ).fetchall()
            datastreams = []
            for datastream in raw_datastreams:
                mime = ds_reader.mime_from_resource(
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
    """
    Provide the datastream content endpoint.
    """
    def _get_ds_dissemination(self, req, resp, pid, dsid):
        """
        Provide datastream content.
        """
        with get_connection() as conn, conn.cursor() as cursor:
            object_info = object_reader.object_id_from_raw(
                pid,
                cursor=cursor
            ).fetchone()
            if object_info is None:
                raise ObjectDoesNotExistError(pid)

            time = utils.iso8601_to_datetime(req.get_param('asOfDateTime'))
            ds_info = ds_reader.datastream(
                {'object': object_info['id'], 'dsid': dsid},
                cursor=cursor
            ).fetchone()
            self._check_ds(ds_info, dsid, resp, pid)
            if time is not None:
                ds_info = ds_reader.datastream_as_of_time(
                    ds_info['id'],
                    time,
                    cursor
                )
            self._check_ds(ds_info, dsid, resp, pid, time=time)

            try:
                resource_info = ds_reader.resource(
                    ds_info['resource']
                ).fetchone()
            except KeyError:
                return

            mime_info = ds_reader.mime_from_resource(resource_info['id'],
                                                     cursor=cursor).fetchone()
            if mime_info:
                resp.content_type = mime_info['mime']

            # Redirect if we are a redirect DS.
            if ds_info['control_group'] == 'R':
                resp.status = falcon.HTTP_307
                resp.location = resource_info['uri']
                return

            # Send data if we are not a redirect DS.
            file_path = filestore.resolve_uri(resource_info['uri'])
            resp.stream = open(file_path, 'rb')
            return


@route('/objects/{pid}/datastreams/{dsid}/history')
class DatastreamHistoryResource(api.DatastreamHistoryResource):
    """
    Provide the datastream history endpoint.
    """
    def _get_datastream_versions(self, pid, dsid):
        """
        Get an iterable of datastream versions.
        """
        with get_connection() as conn, conn.cursor() as cursor:
            try:
                ds_info = ds_reader.datastream_from_raw(
                    pid,
                    dsid,
                    cursor=cursor
                ).fetchone()
            except TypeError as e:
                raise ObjectDoesNotExistError(pid) from e
            if ds_info is None:
                raise DatastreamDoesNotExistError(pid, dsid)

            datastream_versions = []
            old_dss = ds_reader.old_datastreams(ds_info['id'],
                                                cursor=cursor).fetchall()
            version = 0
            temp_ds = ds_info.copy()
            # Not using enumerate as we use the version var outside the loop.
            for old_ds in old_dss:
                temp_ds.update(old_ds)
                temp_ds['modified'] = old_ds['committed']
                datastream_versions.append(fedora_utils.datastream_to_profile(
                    temp_ds,
                    cursor,
                    version=version
                ))
                version += 1
            datastream_versions.append(fedora_utils.datastream_to_profile(
                ds_info,
                cursor,
                version=version
            ))

            return datastream_versions
