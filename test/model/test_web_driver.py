import unittest
from model.web_driver import WebDriverEngine

__author__ = 'mqm'

class TestWebDriverEngine (unittest.TestCase):

    def test_newly_created_engine_has_no_sessions (self):
        engine = WebDriverEngine()
        assert (len(engine.get_sessions()), 0, "A new engine has no seesions")

    def test_a_session_can_be_created (self):
        engine = WebDriverEngine()
        [session_id, session] = engine.create_new_session({"foo": 5, "bar": 7}, {"fooz": 5, "barz": 7})
        assert (len(engine.get_sessions()), 1, "Engine created")