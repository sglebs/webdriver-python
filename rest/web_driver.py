from utils.bottlehelpers import route, Routeable
from bottle import response, request


__author__ = 'mqm'


class WebDriverController (Routeable):


    def __init__(self, web_driver_engine):
        super(WebDriverController, self).__init__()
        self._web_driver_engine = web_driver_engine

    @route('/wd/hub/status', method='GET')
    def get_server_status(self):
        return {"build": {"version": 1.0, "time": "2015-05-07T12:21:30.208824"}, "os": {"name": "linux"}}

    @route('/wd/hub/sessions', method='GET')
    def get_active_sessions(self):
        result = self._web_driver_engine.get_sessions()
        return result

    @route('/wd/hub/session', method='POST')
    def create_session(self):
        required_capabilities = request.json and request.json.get("requiredCapabilities", {}) or {}
        desired_capabilities = request.json and request.json.get("desiredCapabilities", {}) or {}
        [session_id, session] = self._web_driver_engine.create_new_session(required_capabilities, desired_capabilities)
        return {"sessionId": session_id, "status": 0, "value": desired_capabilities}

    @route('/wd/hub/session/<session_id>/window_handle', method='GET')
    def get_current_window_handle(self, session_id):
        session = self._web_driver_engine.get_session(session_id)
        current_window_handle = session.get_current_window_handle()
        return {"sessionId": session_id, "status": 0, "value": current_window_handle}
