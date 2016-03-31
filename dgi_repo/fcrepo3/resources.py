"""
Falcon Resource implementations.
"""

import base64
import logging
import io

import dateutil.parser
import falcon
from psycopg2 import IntegrityError
from psycopg2.extensions import ISOLATION_LEVEL_READ_COMMITTED

import dgi_repo.database.read.object_relations as object_relation_reader
import dgi_repo.database.delete.repo_objects as object_purger
import dgi_repo.database.write.repo_objects as object_writer
import dgi_repo.database.read.repo_objects as object_reader
import dgi_repo.database.write.sources as source_writer
import dgi_repo.database.read.sources as source_reader
import dgi_repo.database.write.log as log_writer
from dgi_repo.configuration import configuration as _configuration
from dgi_repo.database.utilities import check_cursor
from dgi_repo.fcrepo3 import api, foxml, relations
from dgi_repo.database import filestore
from dgi_repo import utilities as utils

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
                    foxml = io.BytesIO(b"""<?xml version="1.0" encoding="UTF-8"?>
<foxml:digitalObject VERSION="1.1" PID="islandora:root" FEDORA_URI="info:fedora/islandora:root"
xmlns:foxml="info:fedora/fedora-system:def/foxml#"
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xsi:schemaLocation="info:fedora/fedora-system:def/foxml# http://www.fedora.info/definitions/1/0/foxml1-1.xsd">
<foxml:objectProperties>
<foxml:property NAME="info:fedora/fedora-system:def/model#state" VALUE="Active"/>
<foxml:property NAME="info:fedora/fedora-system:def/model#label" VALUE="Top-level Collection"/>
<foxml:property NAME="info:fedora/fedora-system:def/model#ownerId" VALUE="fedoraAdmin"/>
<foxml:property NAME="info:fedora/fedora-system:def/model#createdDate" VALUE="2013-07-23T19:19:35.600Z"/>
<foxml:property NAME="info:fedora/fedora-system:def/view#lastModifiedDate" VALUE="2013-07-23T19:19:35.600Z"/>
</foxml:objectProperties>
<foxml:datastream ID="RELS-EXT" FEDORA_URI="info:fedora/islandora:root/RELS-EXT" STATE="A" CONTROL_GROUP="X" VERSIONABLE="true">
<foxml:datastreamVersion ID="RELS-EXT.0" LABEL="Fedora Object to Object Relationship Metadata." CREATED="2013-07-23T19:19:35.600Z" MIMETYPE="application/rdf+xml" FORMAT_URI="info:fedora/fedora-system:FedoraRELSExt-1.0" SIZE="443">
<foxml:xmlContent>
<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:fedora="info:fedora/fedora-system:def/relations-external#" xmlns:fedora-model="info:fedora/fedora-system:def/model#" xmlns:islandora="http://islandora.ca/ontology/relsext#">
  <rdf:Description rdf:about="info:fedora/islandora:root">
    <fedora-model:hasModel rdf:resource="info:fedora/islandora:collectionCModel"></fedora-model:hasModel>
  </rdf:Description>
</rdf:RDF>
</foxml:xmlContent>
</foxml:datastreamVersion>
</foxml:datastream>
<foxml:datastream ID="COLLECTION_POLICY" FEDORA_URI="info:fedora/islandora:root/COLLECTION_POLICY" STATE="A" CONTROL_GROUP="X" VERSIONABLE="true">
<foxml:datastreamVersion ID="COLLECTION_POLICY.0" LABEL="Collection policy" CREATED="2013-07-23T19:19:35.600Z" MIMETYPE="text/xml" SIZE="1226">
<foxml:xmlContent>
<collection_policy xmlns="http://www.islandora.ca" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" name="" xsi:schemaLocation="http://www.islandora.ca http://syn.lib.umanitoba.ca/collection_policy.xsd">
    <content_models>
        <content_model dsid="ISLANDORACM" name="Collection" namespace="islandora:collection" pid="islandora:collectionCModel"></content_model>
    </content_models>
    <search_terms>
        <term field="dc.title">dc.title</term>
        <term field="dc.creator">dc.creator</term>
        <term default="true" field="dc.description">dc.description</term>
        <term field="dc.date">dc.date</term>
        <term field="dc.identifier">dc.identifier</term>
        <term field="dc.language">dc.language</term>
        <term field="dc.publisher">dc.publisher</term>
        <term field="dc.rights">dc.rights</term>
        <term field="dc.subject">dc.subject</term>
        <term field="dc.relation">dc.relation</term>
        <term field="dcterms.temporal">dcterms.temporal</term>
        <term field="dcterms.spatial">dcterms.spatial</term>
        <term field="fgs.DS.first.text">Full text</term>
    </search_terms>
    <relationship>isMemberOfCollection</relationship>
</collection_policy>
</foxml:xmlContent>
</foxml:datastreamVersion>
</foxml:datastream>
<foxml:datastream ID="TN" FEDORA_URI="info:fedora/islandora:root/TN" STATE="A" CONTROL_GROUP="M" VERSIONABLE="true">
<foxml:datastreamVersion ID="TN.0" LABEL="Thumbnail" CREATED="2013-07-23T19:19:35.600Z" MIMETYPE="image/png" SIZE="5137">
<foxml:contentLocation TYPE="INTERNAL_ID" REF="http://localhost:8080/fedora/get/islandora:root/TN/2013-07-23T19:19:35.600Z"/>
</foxml:datastreamVersion>
</foxml:datastream>
<foxml:datastream ID="DC" FEDORA_URI="info:fedora/islandora:root/DC" STATE="A" CONTROL_GROUP="X" VERSIONABLE="true">
<foxml:datastreamVersion ID="DC1.0" LABEL="Dublin Core Record for this object" CREATED="2013-07-23T19:19:35.600Z" MIMETYPE="text/xml" FORMAT_URI="http://www.openarchives.org/OAI/2.0/oai_dc/" SIZE="387">
<foxml:xmlContent>
<oai_dc:dc xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/oai_dc/ http://www.openarchives.org/OAI/2.0/oai_dc.xsd">
  <dc:title>Top-level Collection</dc:title>
  <dc:identifier>islandora:root</dc:identifier>
</oai_dc:dc>
</foxml:xmlContent>
</foxml:datastreamVersion>
</foxml:datastream>
</foxml:digitalObject>""")
                    # TODO: Replace "foxml" with correct file-like
                    # object.
                    base64.encode(foxml, xf)


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
            namespace = _configuration['default_namespace']

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


@route('/objects/{pid}')
class ObjectResource(api.ObjectResource):
    """
    Provide the object endpoint.
    """

    def on_post(self, req, resp, pid):
        """
        Create the new object.
        """
        super().on_post(req, resp, pid)
        cursor = check_cursor(None, ISOLATION_LEVEL_READ_COMMITTED)

        xml = req.get_param('file')
        if xml is not None:
            # Import FOXML, getting PID.
            pid = foxml.import_foxml(xml.file)
        else:
            if not pid or pid == 'new':
                # Generate PID.
                raw_namespace = req.get_param(
                    'namespace',
                    default=_configuration['default_namespace']
                )
                object_writer.get_pid_id(raw_namespace, cursor=cursor)
                pid_id, namespace = cursor.fetchone()
                pid = utils.make_pid(raw_namespace, pid_id)
            else:
                # Reserve given PID in namespace.
                raw_namespace, pid_id = utils.break_pid(pid)
                object_reader.namespace_id(raw_namespace, cursor=cursor)
                try:
                    namespace = cursor.fetchone()[0]
                except TypeError:
                    # @XXX burns the first PID in a namespace.
                    object_writer.get_pid_id(raw_namespace, cursor=cursor)
                    namespace = cursor.fetchone()[1]

                # Jump up PIDs if needed.
                if pid_id.isdigit():
                    pid_id = int(pid_id)
                    object_reader.namespace_info(namespace, cursor=cursor)
                    highest_pid = cursor.fetchone()['highest_id']
                    if highest_pid < pid_id:
                        object_writer.get_pid_ids(raw_namespace,
                                                  highest_pid - pid_id,
                                                  cursor=cursor)

            # Figure out the owner's DB ID.
            raw_owner = req.get_param('ownerId')
            if raw_owner:
                source_writer.upsert_user(
                    {'name': raw_owner, 'source': req.identity.source_id},
                    cursor=cursor
                )
                owner = cursor.fetchone()[0]
            else:
                owner = req.env['wsgi.identity'].user_id

            # Figure out the log's DB ID.
            raw_log = req.get_param('log')
            if raw_log:
                log_writer.upsert_log(raw_log, cursor=cursor)
                log = cursor.fetchone()[0]
            else:
                log = None

            try:
                object_writer.write_object(
                    {
                        'namespace': namespace,
                        'state': req.get_param('state', default='A'),
                        'label': req.get_param('label'),
                        'log': log,
                        'pid_id': pid_id,
                        'owner': owner,
                    },
                    cursor=cursor
                )
            except IntegrityError:
                # Object exists return 500; @XXX it's what Fedora does.
                logger.info('Did not ingest %s as it already existed.', pid)
                raise falcon.HTTPError('500 Internal Server Error')

            foxml.create_default_dc_ds(cursor.fetchone()[0], pid)

        resp.body = 'Ingested {}'.format(pid)
        logger.info('Ingested %s with log: "%s".', pid, log)
        return

    def on_get(self, req, resp, pid):
        """
        Generate the object profile XML.

        This does not respect asOfDateTime from Fedora.
        """
        super().on_get(req, resp, pid)
        cursor = check_cursor(None)

        try:
            object_reader.object_info_from_raw(pid, cursor=cursor)
        except TypeError:
            self._send_404(pid, resp)

        # Get object info.
        object_info = cursor.fetchone()
        object_relation_reader.read_relationship(
            relations.FEDORA_MODEL_NAMESPACE,
            relations.HAS_MODEL_PREDICATE,
            object_info['id'],
            cursor=cursor
        )
        model_info = cursor.fetchall()
        models = set()
        for rdf_object_info in model_info:
            cursor = object_reader.object_info(rdf_object_info['rdf_object'],
                                               cursor=cursor)
            model_object_info = cursor.fetchone()

            object_reader.namespace_info(
                model_object_info['namespace'],
                cursor=cursor
            )
            namespace = cursor.fetchone()['namespace']

            model_pid = utils.make_pid(namespace, model_object_info['pid_id'])
            models.add('info:fedora/{}'.format(model_pid))
        source_reader.user(object_info['owner'], cursor=cursor)
        owner = cursor.fetchone()['username']

        resp.body = self._get_object_profile(
            pid,
            object_info['label'],
            models,
            object_info['created'],
            object_info['modified'],
            object_info['state'],
            owner
        )

        logger.info('Retrieved object: %s.', pid)
        return

    def on_put(self, req, resp, pid):
        """
        Commit the object modification.
        """
        super().on_put(req, resp, pid)
        cursor = check_cursor()
        #@todo: Get current object info.
        try:
            object_reader.object_info_from_raw(pid, cursor=cursor)
        except TypeError:
            self._send_404(pid, resp)

        object_info = cursor.fetchone()

        #@todo: Check modified date param, exiting if needed.
        modified_date = req.get_param('lastModifiedDate')
        if modified_date is not None:
            modified_date = dateutil.parser.parse(modified_date)
            logger.info(modified_date.isoformat())
            if object_info['modified'] > modified_date:
                #@todo: look into what Fedora is doing.
                raise falcon.HTTPConflict(
                    None,
                    '({}) ({})'.format(object_info['modified'].isoformat(),
                                       modified_date.isoformat())
                )

        #@todo: Create old version of object.

        #@todo: Update object info.

    def on_delete(self, req, resp, pid):
        """
        Purge the object.
        """
        super().on_delete(req, resp, pid)
        cursor = check_cursor()

        try:
            object_reader.object_info_from_raw(pid, cursor)
            object_id = cursor.fetchone()['id']
            object_purger.delete_object(object_id, cursor)
        except TypeError:
            self._send_404(pid, resp)

        resp.body = 'Purged {}'.format(pid)
        logger.info('Purged %s', pid)


@route('/objects/{pid}/export', '/objects/{pid}/objectXML')
class ObjectResourceExport(api.ObjectResourceExport):
    def on_get(self, req, resp, pid):
        super().on_get(req, resp, pid)
        # TODO: Generate and dump the FOXML.
        pass


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
        # TODO: Persist the new object.
        pass

    def on_put(self, req, resp, pid, dsid):
        super().on_put(req, resp, pid, dsid)
        # TODO: Commit the modification to the object.
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
