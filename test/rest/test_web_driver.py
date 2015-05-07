import unittest
import json
from test.fixture.restfixture import RestTester
from werkzeug.test import Client
from werkzeug.wrappers import BaseResponse
import bottle
from utils import bottlehelpers
import server_setup

__author__ = 'mqm'

class TestRestWebDriver (unittest.TestCase, RestTester):

    def setUp(self):
        self._setup()

    def tearDown(self):
        self._tearDown()

    def _setup (self):
        self.application = bottle.default_app()
        bottle.debug(True)
        self.application.catchall = False
        server_setup.setup_server(self.application)
        self.http = Client(self.application, BaseResponse)
        self.reset_values_sent()
        self._cached_previous_response = None

    def _teardown_server (self):
        bottlehelpers.clear_routes()

    def test_initially_the_web_driver_has_no_sessions (self):
        self.reset_values_sent()
        self.set_method("GET")
        self.setURI("/sessions")
        self.fetch_url()
        self.assertEqual(self.statusCode(), 200, "Should be able to fetch the sessions")
        jsonResult = self.expected_json()
        sessions = json.loads(jsonResult)
        self.assertEqual(0, len(sessions), "Initially there are no sessions")
