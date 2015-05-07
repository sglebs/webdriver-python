from werkzeug.test import Client
from werkzeug.wrappers import BaseResponse
import bottle
import os
import json
import re


# Inspired by http://bazaar.launchpad.net/~prime8/waferslim/main/view/head:/src/waferslim/examples/decision_table.py
# This enables tests to be written in xUnit format and/or in Fitnesse format
# the class is abstract so that concrete subclasses can plug themselves into teh actual rest server
# (the specifics vary depending if it is messenger-server or core-server)


class RestTester:
    ''' Class to be the system-under-test in fitnesse. '''

    def reset_values_sent(self):
        self._protocol_method = ""
        self._URI = ""
        self._response = None # invalidates the cached response
        self._content_type = u'application/json'
        self.set_params('null') # None will cause PUT methods that expect JSON to fail, so this is safer. It will send a valid JSON.
        self.query_string = None
        #self._headers = {'content-type': self._content_type}
        self._headers = dict()

    def _setup (self):
        self.application = bottle.default_app()
        bottle.debug(True)
        self.application.catchall = False
        self._setup_server()
        self.http = Client(self.application, BaseResponse)
        self.reset_values_sent()
        self._cached_previous_response = None


    def _tearDown (self):
        self._teardown_server()
        self.application = None

    def _teardown_server(self):
        self._ses.close()


    def _teardown_server (self):
        raise NotImplementedError( "Subclass must implemented this" )

    def _setup_server (self):
        raise NotImplementedError( "Subclass must implemented this" )


    def __init__(self):
        self._setup()

    #@convert_arg(to_type=string)
    def set_method(self, protocol_method):
        ''' Decorated method to set the protocol method '''
        self._protocol_method = protocol_method
        self._response = None # invalidates teh cached response

    def set_content_type(self, content_type):
        ''' Decorated method to set the content type '''
        self._content_type = content_type
        self._response = None # invalidates teh cached response

    def set_query_string(self, query_string):
        ''' Decorated method to set the query string '''
        query_string = self.replace_pseudo_vars(query_string)
        self.query_string = query_string
        self._response = None # invalidates teh cached response

    def set_params (self, params):
        ''' Decorated method to set the params to the request '''
        if params is not None:
            if len (params.strip()) > 0:
                self._params = params.encode('utf-8')
            else:
                self._params = 'null' # effectively a Fitnesse table cell full of spaces is just like null
        else:
            self._params = 'null'
        self._response = None # invalidates teh cached response

    #@convert_arg(to_type=string)
    def replace_pseudo_vars(self, a_string):
        if self._cached_previous_response is not None and self._cached_previous_response is not '': # we support variable replacing in the URL based on previous replies, to facilitate for Fitnesse
            previousJson = json.loads(self._cached_previous_response)
            if type(previousJson) == type({}): # we just do it for dictionaries
                for key, value in previousJson.items():
                    a_string = re.sub("__%s__" % key, str(value), a_string)
        return a_string

    def add_header(self, header):
        self._headers.update(header)

    def setURI(self, uri):
        ''' Decorated method to set the URI  '''
        uri = self.replace_pseudo_vars(uri)

        self._URI = uri
        self._response = None # invalidates teh cached response

    def statusCode (self):
        if self._response is None:
            self.fetch_url()
        return self._response.status_code

    def fetch_url (self):
        if self._protocol_method == "GET":
            self._response = self.http.get(self._URI, data=self._params, query_string = self.query_string, content_type=self._content_type) # updates the cached response
        if self._protocol_method == "DELETE":
            self._response = self.http.delete(self._URI, data=self._params, query_string = self.query_string, content_type=self._content_type) # updates the cached response
        if self._protocol_method == "PUT":
            self._response = self.http.put(self._URI, data=self._params, query_string = self.query_string, content_type=self._content_type) # updates the cached response
        if self._protocol_method == "POST":
            self._response = self.http.post(self._URI, data=self._params, query_string = self.query_string, content_type=self._content_type)  # updates the cached response

        if int(self._response.status_code) < 250 and self._response.data is not '': # we only cache successful replies that are not empty strings
            json_reply = json.loads (self._response.data)
            if type(json_reply)==type({}): # and we only do it for dictionaries
                self._cached_previous_response = self._response.data

    #@convert_result(using=_YESNO_CONVERTER)
    def expected_json (self):
        if self._response is None:
            self.fetch_url()
        return self._response.data

    def json_response(self):
        return json.loads(self.expected_json())

if __name__ == '__main__':
    print "Rest fixture"

