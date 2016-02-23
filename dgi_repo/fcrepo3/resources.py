"""
Falcon Resource implementations.
"""

from . import api
import base64
import io

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
        if method == '{{{0}}}getDatastreamDissemination'.format(api.FEDORA_TYPES_URI):
            with xf.element('{{{0}}}getDatastreamDisseminationResponse'.format(api.FEDORA_TYPES_URI)):
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
            with xf.element('{{{0}}}exportResponse'.format(api.FEDORA_TYPES_URI)):
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
    def _store(self, uploaded_file):
        # TODO: Copy the file somewhere semi-persistent and return a URI to it.
        pass


@route('/objects/nextPID')
class PidResource(api.PidResource):
    def _get_pids(self, numPIDs=1, namespace=None):
        # TODO: Allocate PIDs and return in iterable (method as generator or a
        # list or otherwise).
        return ("{0}:{1}".format(namespace, i) for i in range(0, numPIDs))


@route('/objects/{pid}')
class ObjectResource(api.ObjectResource):
    def on_post(self, req, resp, pid):
        super().on_post(req, resp, pid)
        # TODO: Create the new object.
        pass

    def on_get(self, req, resp, pid):
        super().on_get(req, resp, pid)
        # TODO: Generate the object profile XML.
        pass

    def on_put(self, req, resp, pid):
        super().on_put(req, resp, pid)
        # TODO: Commit the object modification.
        pass

    def on_delete(self, req, resp, pid):
        super().on_delete(req, resp, pid)
        # TODO: Purge the object.
        pass


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
