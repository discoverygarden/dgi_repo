#!/usr/bin/env python

import api

route_map = dict()

def route(route):
    '''
    Helper pull all our routes together.
    '''
    def add(cls):
        global route_map
        route_map[route] = cls
        return cls

    return add


@route('/services/access')
class SoapAccessResource(api.FakeSoapResource):
    def _dump_wsdl(resp):
        '''
        Output the WSDL for the given endpoint.
        '''
        pass

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


@route('/services/management')
class SoapManagementResource(api.FakeSoapResource):
    def _dump_wsdl(resp):
        '''
        Output the WSDL for the given endpoint.
        '''
        pass

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


@route('/upload')
class UploadResource(api.UploadResource):
    def _store(self, uploaded_file):
        '''
        Persist the file somewhere.

        Parameters:
            uploaded_file: A file-like object representing the uploaded file.

        Returns:
            A URI which we can dereference server-side during ingest.
        '''
        pass


@route('/objects/nextPID')
class PidResource(api.PidResource):
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


@route('/objects/{pid}')
class ObjectResource(api.ObjectResource):
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

@route('/objects/{pid}/export')
@route('/objects/{pid}/objectXML')
class ObjectResourceExport(api.ObjectResourceExport):
    def on_get(self, req, resp):
        '''
        Dump out FOXML export.
        '''
        pass


@route('/objects/{pid}/datastreams')
class DatastreamListResource(api.DatastreamListResource):
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


@route('/objects/{pid}/datastreams/{dsid}')
class DatastreamResource(api.DatastreamResource):
    def on_post(self, req, resp):
        '''
        Ingest new datastream.
        '''
        pass

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


@route('/objects/{pid}/datastreams/{dsid}/content')
class DatastreamDisseminationResource(api.DatastreamDisseminationResource):
    def on_get(self, req, resp):
        '''
        Dump, redirect or pipe datastream content.
        '''
        pass


@route('/objects/{pid}/datastreams/{dsid}/history')
class DatastreamHistoryResource(api.DatastreamHistoryResource):
    def _get_datastream_versions(self, pid, startDT=None, endDT=None, **kwargs):
        '''
        Get an iterable of datastream versions.
        '''
        pass
