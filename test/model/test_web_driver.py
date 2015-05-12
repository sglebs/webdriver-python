import unittest
from model.web_driver import WebDriverEngine

__author__ = 'mqm'

class TestWebDriverEngine (unittest.TestCase):

    def test_newly_created_engine_has_no_sessions (self):
        engine = WebDriverEngine()
        assert (len(engine.get_sessions()), 0, "A new engine has no seesions")