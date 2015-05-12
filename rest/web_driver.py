from utils.bottlehelpers import route, Routeable
from bottle import response, request
import datetime

__author__ = 'mqm'


class WebDriverController (Routeable):


    def __init__(self, web_driver_engine):
        super(WebDriverController, self).__init__()
        self._web_driver_engine = web_driver_engine
        self._sessions = {}

    @route('/wd/hub/status', method='GET')
    def get_server_status(self):
        return {"build": {"version": 1.0, "time": "2015-05-07T12:21:30.208824"}, "os": {"name": "linux"}}

    @route('/wd/hub/sessions', method='GET')
    def get_active_sessions(self):
        result = self._web_driver_engine.get_sessions()
        return result

    @route('/wd/hub/session', method='POST')
    def create_session(self):
        required_capabilities = request.json.get("requiredCapabilities", {})
        desired_capabilities = request.json.get("desiredCapabilities", {})
        session = self._web_driver_engine.create_new_session(required_capabilities, desired_capabilities)
        session_id = datetime.datetime.utcnow().isoformat()
        self._sessions[session_id] = session
        return {"sessionId": session_id, "status": 0, "value": desired_capabilities}
