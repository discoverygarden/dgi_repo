"""
Falcon resource abstract base classes.

@TODO: move remaining API level logging/responses from implementations to here.
"""
import logging
from abc import ABC, abstractmethod

import falcon
from lxml import etree
from dgi_repo.utilities import SpooledTemporaryFile
from dgi_repo.fcrepo3.exceptions import ObjectDoesNotExistError
from dgi_repo.fcrepo3.exceptions import DatastreamDoesNotExistError
from dgi_repo.fcrepo3.exceptions import ObjectExistsError

logger = logging.getLogger(__name__)

FEDORA_ACCESS_URI = 'http://www.fedora.info/definitions/1/0/access/'
FEDORA_MANAGEMENT_URI = 'http://www.fedora.info/definitions/1/0/management/'
FEDORA_TYPES_URI = 'http://www.fedora.info/definitions/1/0/types/'


def _parse_xml_body(req, resp, resource, params):
    """
    Helper to parse SOAP XML messages.
    """
    req._params['envelope'] = etree.parse(req.stream)


class FakeSoapResource(ABC):
    """
    Helper class for pseudo-SOAP endpoints.

    The endpoints we need target specifically include:
    - /services/access (for getDatastreamDissemination) and
    - /services/management (for export)
    """
    SOAP_NS = 'http://schemas.xmlsoap.org/soap/envelope/'

    @falcon.before(_parse_xml_body)
    def on_post(self, req, resp):
        """
        Parse SOAP message and respond accordingly.
        """
        soap_xml_out = SpooledTemporaryFile()
        with etree.xmlfile(soap_xml_out) as xf:
            with xf.element('{{{0}}}Envelope'.format(self.__class__.SOAP_NS)):
                with xf.element('{{{0}}}Body'.format(self.__class__.SOAP_NS)):
                    for method, kwargs in self._parse(req):
                        self._respond(xf, method, kwargs)
                        logger.info('Responding to : %s with params %s.',
                                    method, kwargs)
        length = soap_xml_out.tell()
        soap_xml_out.seek(0)
        resp.set_stream(soap_xml_out, length)
        resp.content_type = 'application/soap+xml'

    @abstractmethod
    def _respond(self, xf, method, kwargs):
        """
        Write method response to XML.

        Args:
            xf: An iterative XML writer, as per
                http://lxml.de/api.html#incremental-xml-generation
            method: A method name in our funky format:
                "{namespace://URI}method-name"
            kwargs: The dictionary of parameters passed for the particular
                method.
        """
        pass

    def _parse(self, req):
        """
        Parse out Fedora messages from a SOAP body.

        Generates two-tuples, each containing:
        - the method name in "{namespace://URI}method-name" form, and
        - a dictionary of parameters passed to the method.
        """
        for method_el in req._params['envelope'].xpath(
            '/s:Envelope/s:Body/t:*', namespaces={'s': self.__class__.SOAP_NS,
                                                  't': FEDORA_TYPES_URI}):
            yield (
                method_el.tag,
                {child.tag: child.text for child in method_el.getchildren()}
            )


class UploadResource(ABC):
    """
    Abstract Falcon "Resource" to handle file uploads.
    """
    def on_post(self, req, resp):
        uploaded_file = req.get_param('file', required=True).file
        resp.body = self._store(uploaded_file)
        resp.status = falcon.HTTP_202

    @abstractmethod
    def _store(self, uploaded_file):
        """
        Persist the file somewhere.

        Args:
            uploaded_file: A file-like object representing the uploaded file.

        Returns:
            A URI which we can dereference server-side during ingest.
        """
        pass


class DescribeResource(object):
    """
    Falcon "Resource" to serve the repository description.
    """
    def on_get(self, req, resp):
        resp.content_type = 'application/xml'
        resp.body = """<?xml version="1.0" encoding="UTF-8"?>
<fedoraRepository
  xmlns="{0}">
  <repositoryVersion>{1}</repositoryVersion>
</fedoraRepository>
""".format(FEDORA_ACCESS_URI, '3.py')


class PidResource(ABC):
    """
    Falcon "Resource" to allocate PIDs.
    """
    def on_post(self, req, resp):
        params = dict()
        req.get_param_as_int('numPIDs', min=1, store=params)
        req.get_param('namespace', store=params)

        xml_out = SpooledTemporaryFile()
        with etree.xmlfile(xml_out) as xf:
            with xf.element('{{{0}}}pidList'.format(FEDORA_ACCESS_URI)):
                for pid in self._get_pids(**params):
                    with xf.element('{{{0}}}pid'.format(FEDORA_ACCESS_URI)):
                        xf.write(pid)
        length = xml_out.tell()
        xml_out.seek(0)
        resp.set_stream(xml_out, length)
        resp.content_type = 'application/xml'

    @abstractmethod
    def _get_pids(self, numPIDs=1, namespace=None):
        """
        Allocate a number of PIDs and return them in an iterable.

        This method could be a generator, but needs not be.

        Args:
            numPIDs: An integer representing the number of PIDs to allocate.
            namespace: A string indicating the namespace in which to allocate
                the PIDs. If "None", the default configuration should be used.
        """
        pass


class ObjectResource(ABC):
    """
    Falcon "Resource" for basic object interactions.
    """
    def on_post(self, req, resp, pid):
        """
        Ingest a new object.
        """
        try:
            # The PID we have right now may not be the final PID.
            pid = self._create_object(req, pid)
        except ObjectExistsError as e:
            logger.info('Did not ingest %s as it already existed.', e.pid)
            raise falcon.HTTPError('500 Internal Server Error') from e
        resp.content_type = 'text/plain'
        resp.body = 'Ingested {}.'.format(pid)
        logger.info('Ingested %s.', pid)

    @abstractmethod
    def _create_object(self, req, pid):
        """
        Create an object

        Raises:
            ObjectExistsError: The object already exist.
        """
        pass

    def on_get(self, req, resp, pid):
        """
        Get object profile.

        @TODO: handle calling _get_object_profile at this level.
        """
        resp.content_type = 'application/xml'
        try:
            resp.body = self._get_object(req, pid)
        except ObjectDoesNotExistError:
            logger.info('Did not retrieve object %s as it did not exist.', pid)
            _send_object_404(pid, resp)
        logger.info('Retrieved object: %s.', pid)

    @abstractmethod
    def _get_object(self, req, pid):
        """
        Get an object's profile.

        Raises:
            ObjectDoesNotExistError: The object doesn't exist.
        """
        pass

    def on_put(self, req, resp, pid):
        """
        Update an object.

        @TODO: Bring 409 to this level.
        """
        try:
            self._update_object(req, pid)
        except ObjectDoesNotExistError:
            logger.info('Did not update object %s as it did not exist.', pid)
            _send_object_404(pid, resp)
        logger.info('Updated object: %s.', pid)

    @abstractmethod
    def _update_object(self, req, pid):
        """
        Update an object.

        Raises:
            ObjectDoesNotExistError: The object doesn't exist.
        """
        pass

    def on_delete(self, req, resp, pid):
        """
        Purge an object.
        """
        resp.content_type = 'text/plain'
        try:
            self._purge_object(req, pid)
        except ObjectDoesNotExistError:
            logger.info('Did not purge object %s as it did not exist.', pid)
            _send_object_404(pid, resp)
        resp.body = 'Purged {}'.format(pid)
        logger.info('Purged object: %s.', pid)

    @abstractmethod
    def _purge_object(self, req, pid):
        """
        Purge an object.

        Raises:
            ObjectDoesNotExistError: The object doesn't exist.
        """
        pass

    def _get_object_profile(self, pid, label, models, created,
                            modified, state, owner):
        """
        Build up object profile XML.
        """
        tree = etree.fromstring('''<?xml version="1.0"?>
        <objectProfile
          xmlns="http://www.fedora.info/definitions/1/0/access/"
          xmlns:xsd="http://www.w3.org/2001/XMLSchema"
          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:schemaLocation="http://www.fedora.info/definitions/1/0/access/
                  http://www.fedora.info/definitions/1/0/objectProfile.xsd">
          <objModels>
            <model>info:fedora/fedora-system:FedoraObject-3.0</model>
          </objModels>
          </objectProfile>
        ''')

        model_xpath = etree.ETXPath(
         '//{{{}}}objModels'.format(FEDORA_ACCESS_URI)
        )
        models_element = model_xpath(tree)[0]
        for model in models:
            model_element = etree.SubElement(
                models_element,
                '{{{}}}model'.format(FEDORA_ACCESS_URI)
            )
            model_element.text = model

        tree.attrib['pid'] = pid

        if label:
            label_element = etree.SubElement(
                tree,
                '{{{}}}objLabel'.format(FEDORA_ACCESS_URI)
            )
            label_element.text = label

        state_element = etree.SubElement(
            tree,
            '{{{}}}objState'.format(FEDORA_ACCESS_URI)
        )
        state_element.text = state

        owner_element = etree.SubElement(
            tree,
            '{{{}}}objOwnerId'.format(FEDORA_ACCESS_URI)
        )
        owner_element.text = owner

        created_element = etree.SubElement(
            tree,
            '{{{}}}objCreateDate'.format(FEDORA_ACCESS_URI)
        )
        created_element.text = created.isoformat()

        modified_element = etree.SubElement(
            tree,
            '{{{}}}objLastModDate'.format(FEDORA_ACCESS_URI)
        )
        modified_element.text = modified.isoformat()

        return etree.tostring(tree, xml_declaration=True, encoding="UTF-8")


class ObjectResourceExport(ABC):
    """
    Base Falcon "Resource" to handle object exports.
    """
    def on_get(self, req, resp, pid):
        """
        Dump out FOXML export.
        """
        resp.content_type = 'application/xml'


class DatastreamListResource(ABC):
    """
    Base Falcon "Resource" to handle datastream listings.
    """
    def on_get(self, req, resp, pid):
        params = {
            'pid': pid
        }

        xml_out = SpooledTemporaryFile()
        with etree.xmlfile(xml_out) as xf:
            with xf.element('{{{0}}}objectDatastreams'.format(
                    FEDORA_ACCESS_URI)):
                try:
                    for datastream in self._get_datastreams(**params):
                        with xf.element('{{{0}}}datastream'.format(
                                FEDORA_ACCESS_URI), attrib=datastream):
                            pass
                except ObjectDoesNotExistError:
                    logger.info(('Datastream list not retrieved for %s as '
                                'object did not exist.'), pid)
                    raise falcon.HTTPNotFound()
        length = xml_out.tell()
        xml_out.seek(0)
        resp.set_stream(xml_out, length)
        resp.content_type = 'application/xml'
        logger.info('Datastream list retrieved for %s.', pid)

    @abstractmethod
    def _get_datastreams(self, pid, asOfDateTime=None):
        """
        Get datastreams.

        @XXX: not respecting asOfDateTime as we don't use it.

        Returns:
            An iterable of dicts, each containing:
                dsid: The datastream ID,
                label: The datastream label, and
                mimeType: The datastream MIME-type.
        Raises:
            ObjectDoesNotExistError: The object doesn't exist.
        """
        pass


class DatastreamResource(ABC):
    """
    Base Falcon "Resource" for datastream interactions.
    """
    def on_post(self, req, resp, pid, dsid):
        """
        Ingest new datastream.
        """
        try:
            self._create_datastream(req, pid, dsid)
        except ObjectDoesNotExistError:
            logger.info(('Did not create datastream %s on  %s as the object '
                         'did not exist.'), dsid, pid)
            _send_object_404(pid, resp)

        resp.status = falcon.HTTP_201
        logger.info('Created DS %s on %s.', dsid, pid)

    @abstractmethod
    def _create_datastream(self, req, pid, dsid):
        """
        Create a datastream.

        Raises:
            ObjectDoesNotExistError: The object doesn't exist.
        """
        pass

    def on_get(self, req, resp, pid, dsid):
        """
        Get datastream info.
        """
        xml_out = SpooledTemporaryFile()
        try:
            datastream_info = self._get_datastream_info(pid, dsid,
                                                        **req.params)

        except ObjectDoesNotExistError:
            logger.info(('Datastream not retrieved for %s on '
                         '%s as object did not exist.'), dsid, pid)
            _send_object_404(pid, resp)
        except DatastreamDoesNotExistError as e:
                resp.content_type = 'text/plain'
                logger.info(('Datastream not retrieved for %s not found on %s '
                             'as it did not exist.'), dsid, pid)
                resp.body = 'Datastream {} not found on {}.'.format(dsid, pid)
                raise falcon.HTTPNotFound() from e
        with etree.xmlfile(xml_out) as xf:
            _writeDatastreamProfile(xf, datastream_info)
        length = xml_out.tell()
        xml_out.seek(0)
        resp.set_stream(xml_out, length)
        resp.content_type = 'application/xml'
        return

    def on_put(self, req, resp, pid, dsid):
        """
        Update datastream.
        """
        try:
            self._update_datastream(req, pid, dsid)
        except ObjectDoesNotExistError:
            logger.info(('Datastream not updated for %s on '
                         '%s as object did not exist.'), dsid, pid)
            _send_object_404(pid, resp)
        except DatastreamDoesNotExistError as e:
            logger.info(('Datastream not updated for %s on '
                         '%s as datastream did not exist.'), dsid, pid)
            resp.body = ('Datastream not updated for %s on %s as datastream '
                         'did not exist.').format(dsid, pid)
            raise falcon.HTTPNotFound() from e

    @abstractmethod
    def _update_datastream(self, req, pid, dsid):
        """
        Update a datastream.

        Raises:
            ObjectDoesNotExistError: The object doesn't exist.
            DatastreamDoesNotExistError: The datastream doesn't exist.
        """
        pass

    def on_delete(self, req, resp, pid, dsid):
        """
        Purge datastream.
        """
        self._delete_datastream(req, pid, dsid)

    @abstractmethod
    def _delete_datastream(self, req, pid, dsid):
        """
        Delete a datastream.
        """
        pass

    @abstractmethod
    def _get_datastream_info(self, pid, dsid, asOfDateTime=None, **kwargs):
        """
        Get the relevant datastream info.
        """
        pass


class DatastreamDisseminationResource(ABC):
    """
    Base Falcon "Resource" to handle datastream dissemination.
    """
    def on_get(self, req, resp, pid, dsid):
        """
        Dump datastream content.
        """
        try:
            self._get_ds_dissemination(req, resp, pid, dsid)
        except ObjectDoesNotExistError:
            logger.info(('Did not get datastream dissemination for %s as the '
                         'object %s did not exist.'), dsid, pid)
            _send_object_404(pid, resp)
        logger.info('Retrieved datastream content for %s on %s.', dsid, pid)

    @abstractmethod
    def _get_ds_dissemination(self, req, resp, pid, dsid):
        """
        Prep datastream content response.

        @TODO: Get rid of the need for passing resp.

        Raises:
            ObjectDoesNotExistError: The object doesn't exist.
        """
        pass

    def _check_ds(self, ds_info, dsid, resp, pid, time=None):
        """
        Check if ds_info is populated or send 404.
        """
        time = time if time else 'now'
        if ds_info is None:
            resp.content_type = 'text/plain'
            logger.info('Datastream %s not found on %s as of %s.',
                        dsid, pid, time)
            resp.body = 'Datastream {} not found on {} as of {}.'.format(dsid,
                                                                         pid,
                                                                         time)
            raise falcon.HTTPNotFound()


class DatastreamHistoryResource(ABC):
    """
    Base Falcon "Resource" to handle listing of datastream versions.
    """
    def on_get(self, req, resp, pid, dsid):
        """
        Dump the datastream history.
        """
        xml_out = SpooledTemporaryFile()
        with etree.xmlfile(xml_out) as xf:
            with xf.element('{{0}}datastreamHistory'.format(
                    FEDORA_MANAGEMENT_URI)):
                try:
                    for datastream in self._get_datastream_versions(pid, dsid):
                        _writeDatastreamProfile(xf, datastream)
                except ObjectDoesNotExistError:
                    logger.info(('Datastream history not retrieved for %s on '
                                 '%s as object did not exist.'), dsid, pid)
                    _send_object_404(pid, resp)
                except DatastreamDoesNotExistError as e:
                    resp.content_type = 'text/xml'
                    logger.info(('Datastream history not retrieved for %s on '
                                 '%s as datastream did not exist.'), dsid, pid)
                    resp.body = ('Datastream history not retrieved for %s on '
                                 '%s as datastream did not exist.').format(
                                 dsid, pid)
                    raise falcon.HTTPNotFound() from e
        length = xml_out.tell()
        xml_out.seek(0)
        resp.set_stream(xml_out, length)
        resp.content_type = 'application/xml'
        logger.info('Retrieved DS history for %s on %s', dsid, pid)

    @abstractmethod
    def _get_datastream_versions(self, pid, dsid):
        """
        Get an iterable of datastream versions.

        Raises:
            ObjectDoesNotExistError: The object doesn't exist.
            DatastreamDoesNotExistError: The datastream doesn't exist.
        """
        pass


def _writeDatastreamProfile(xf, datastream_info):
    """
    Write a datastream profile for the given datastream.

    Args:
        xf: A lxml incremental XML generator instance.
        datastream_info: A dict representing the datastream profile, mapping
        element names to values. For example:
        {
            'dsLabel': 'DC Record',
            'dsVersionID': 'DC1.0',
            'dsCreateDate': '2016-02-19T08:02.5000Z',
            'dsState': 'A',
            'dsMime': 'application/xml',
            'dsFormatURI': 'http://www.openarchives.org/OAI/2.0/oai_dc/',
            'dsControlGroup': 'X',
            'dsSize': '387',
            'dsVersionable': 'true',
            'dsInfoType': '',
            'dsLocation': 'islandora:root+DC+DC1.0',
            'dsLocationType': 'INTERNAL_ID',
            'dsChecksumType': 'DISABLED',
            'dsChecksum': 'none',
        }
        and minimally:
        {
            'dsLabel': 'DC Record',
            'dsCreateDate': '2016-02-19T08:02.5000Z',
            'dsState': 'A',
            'dsMime': 'application/xml',
            'dsControlGroup': 'X',
            'dsSize': '387',
            'dsVersionable': 'true',
            'dsLocation': 'islandora:root+DC+DC1.0',
            'dsLocationType': 'INTERNAL_ID',
            'dsChecksumType': 'DISABLED',
            'dsChecksum': 'none',
        }
    """
    with xf.element('{{{}}}datastreamProfile'.format(FEDORA_MANAGEMENT_URI)):
        for key, value in datastream_info.items():
            if value is not None:
                with xf.element('{{{}}}{}'.format(FEDORA_MANAGEMENT_URI, key)):
                    xf.write(str(value))


def _send_object_404(pid, resp):
    """
    Send a Fedora like 404 when objects don't exist.
    """
    resp.content_type = 'text/plain'
    resp.body = 'Object not found in low-level storage: {}'.format(pid)
    raise falcon.HTTPNotFound()
