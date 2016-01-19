#!/usr/bin/env python

from abc import ABC, abstractmethod
import falcon
from libxml import etree
from tempfile import SpooledTemporaryFile
from time import strptime

FEDORA_ACCESS_URI = 'http://www.fedora.info/definitions/1/0/access/'
FEDORA_MANAGEMENT_URI = 'http://www.fedora.info/definitions/1/0/management/'
FEDORA_TYPES_URI = 'http://www.fedora.info/definitions/1/0/types/'

class FakeSoapResource(ABC):
    '''
    Helper class for pseudo-SOAP endpoints.

    The endpoints we need target specifically include:
    -  :8080/fedora/services/access (for getDatastreamDissemination) and
    -  :8080/fedora/services/management (for export)
    '''
    SOAP_NS = 'http://schemas.xmlsoap.org/soap/envelope/'
    def on_get(self, req, resp):
        '''
        Used to acquire the relevant WSDL files for given paths.
        '''
        if req.get_param_as_bool('wsdl', required=True, blank_as_true=True):
            self._dump_wsdl(resp)

    def on_post(self, req, resp):
        '''
        Parse SOAP message and respond accordingly.
        '''
        soap_xml_out = getTempFile()
        with etree.xmlfile(soap_xml_out) as xf:
            with xf.element('{http://schemas.xmlsoap.org/soap/envelope/}Envelope'):
                with xf.element('{http://schemas.xmlsoap.org/soap/envelope/}Body'):
                    for method, kwargs in self._parse(req):
                        self._respond(xf, method, kwargs)
        length = soap_xml_out.tell()
        soap_xml_out.seek(0)
        resp.set_stream(soap_xml_out, length)

    @abstractmethod
    def _dump_wsdl(resp):
        '''
        Output the WSDL for the given endpoint.
        '''
        pass

    @abstractmethod
    def _respond(self, xf, method, kwargs):
        '''
        Write method response to XML.

        Parameters:
            xf: An iterative XML writer, as per
                http://lxml.de/api.html#incremental-xml-generation
            method: A method name in our funky format:
                "{namespace://URI}method-name"
            kwargs: The dictionary of parameters passed for the particular
                method.
        '''
        pass

    def _parse(self, req):
        '''
        Parse out Fedora messages from a SOAP body.

        Generates two-tuples, each containing:
            - the method name in "{namespace://URI}method-name" form, and
            - a dictionary of parameters passed to the method.
        '''
        envelope = etree.parse(req.stream)
        for method_el in envelope.xpath('/{{0}}Envelope/{{0}}Body/{{1}}*'.format(self.__class__.SOAP_NS, FEDORA_TYPES_URI)):
            yield (method_el.tag, {child.tag: child.text for child in method_el.getchildren()})


class UploadResource(ABC):
    def on_post(self, req, resp):
        uploaded_file = req.get_param('file', required=True)
        resp.body = self._store(uploaded_file)
        resp.status = falcon.HTTP_202

    @abstractmethod
    def _store(self, uploaded_file):
        '''
        Persist the file somewhere.

        Parameters:
            uploaded_file: A file-like object representing the uploaded file.

        Returns:
            A URI which we can dereference server-side during ingest.
        '''
        pass

class DescribeResource(object):
    def on_get(self, req, resp):
        resp.body = '''
<?xml version="1.0" encoding="UTF-8"?>
<fedoraRepository
  xmlns="{0}">
  <repositoryVersion>{1}</repositoryVersion>
</fedoraRepository>
'''.format(FEDORA_ACCESS_URI, '3.py')

class PidResource(ABC):
    def on_post(self, req, resp):
        params = dict()
        req.get_param_as_int('numPids', min=1, store=params)
        req.get_param('namespace', store=params)

        xml_out = getTempFile()
        with etree.xml_file(xml_out) as xf:
            with xf.element('{{0}}pidList'.format(FEDORA_ACCESS_URI)):
                for pid in self._get_pids(**params):
                    with xf.element('{{0}}pid'.format(FEDORA_ACCESS_URI)):
                        xf.write(pid)
        length = xml_out.tell()
        xml_out.seek(0)
        resp.set_stream(xml_out, length)

    @abstractmethod
    def _get_pids(self, number=1, namespace=None):
        '''
        Allocate a number of PIDs and return them in an iterable.

        This method could be a generator, but needs not be.

        Parameters:
            number: An integer representing the number of PIDs to allocate.
            namespace: A string indicating the namespace in which to allocate
                the PIDs. If "None", the default configuration should be used.
        '''
        pass

class ObjectResource(ABC):
    def on_post(self, req, resp):
        '''
        Ingest a new object.
        '''
        pass

    def on_get(self, req, resp):
        '''
        Get object profile.
        '''
        pass

    def on_put(self, req, resp):
        '''
        Update an object.
        '''
        pass

    def on_delete(self, req, resp):
        '''
        Purge an object.
        '''
        pass


class ObjectResourceExport(ABC):
    def on_get(self, req, resp):
        '''
        Dump out FOXML export.
        '''
        pass

class DatastreamListResource(ABC):
    def on_get(self, req, resp):
        params = dict()
        req.get_param('pid', store=params)
        parseDateTime(req, field, 'asOfDateTime', params)

        xml_out = getTempFile()
        with etree.xml_file(xml_out) as xf:
            with xf.element('{{0}}objectDatastreams'.format(FEDORA_ACCESS_URI)):
                for datastream in self._get_datastreams(**params):
                    with xf.element('{{0}}datastream'.format(FEDORA_ACCESS_URI), attribs=datastream):
                        pass
        length = xml_out.tell()
        xml_out.seek(0)
        resp.set_stream(xml_out, length)

    @abstractmethod
    def _get_datastreams(self, pid, asOfDateTime=None):
        '''
        Get datastreams.

        Returns:
            An iterable of dicts, each containing:
                dsid: The datastream ID,
                label: The datastream label, and
                mimeType: The datastream MIME-type.
        '''
        pass

def parseDateTime(req, field, params):
    '''
    Helper to parse ISO 8601 datetimes.

    Parameters:
        req: The request from which the value to parse should be grabbed.
        field: The field to grab from the request (and to store in params)
        params: A dictionary in which to store the parsed timestamp.
    '''
    value = req.get_param(field)
    if value is not None:
        try:
            params[field] = strptime(value, '%Y-%m-%dT%H:%M:%S.%fZ')
        except ValueError:
            raise falcon.HTTPBadRequest('Failed to parse {0} date: {1}'.format(field, value))

class DatastreamResource(ABC):
    def on_post(self, req, resp):
        '''
        Ingest new datastream.
        '''
        pass

    def on_get(self, req, resp):
        '''
        Get datastream info.
        '''
        xml_out = getTempFile()
        with etree.xml_file(xml_out) as xf:
            for datastream in self._get_datastream_versions(**req.params):
                writeDatastreamProfile(xf, datastream)
        length = xml_out.tell()
        xml_out.seek(0)
        resp.set_stream(xml_out, length)

    def on_put(self, req, resp):
        '''
        Update datastream.
        '''
        pass

    def on_delete(self, req, resp):
        '''
        Purge datastream.
        '''
        pass


class DatastreamDisseminationResource(ABC):
    def on_get(self, req, resp):
        '''
        Dump datastream content.
        '''
        pass


class DatastreamHistoryResource(ABC):
    def on_get(self, req, resp):
        '''
        Dump the datastream history.
        '''
        xml_out = getTempFile()
        with etree.xml_file(xml_out) as xf:
            with xf.element('{{0}}datastreamHistory'.format(FEDORA_MANAGEMENT_URI)):
                for datastream in self._get_datastream_versions(**req.params):
                    writeDatastreamProfile(xf, datastream)
        length = xml_out.tell()
        xml_out.seek(0)
        resp.set_stream(xml_out, length)

    @abstractmethod
    def _get_datastream_versions(self, pid, startDT=None, endDT=None, **kwargs):
        '''
        Get an iterable of datastream versions.
        '''
        pass


def writeDatastreamProfile(xf, datastream_info):
    with xf.element('{{0}}datastreamProfile'.format(FEDORA_MANAGEMENT_URI)):
        # TODO: Probably some mapping require here.
        for key, value in datastream_info.iteritems():
            with xf.element('{{0}}{1}'.format(FEDORA_MANAGEMENT_URI, key)):
                xf.write(value)

def getTempFile():
    '''
    Helper for temp file acquisition.

    Returns:
        A file object which should be automatically deleted when it is closed.
    '''
    # TODO: Expose "max_size" as configuration, for tuning.
    return SpooledTemporaryFile(max_size=4096)
