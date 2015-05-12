#from utils.bottlehelpers import get, post, route, Routeable
from bottle import get, put, post, delete, route

from bottle import request


__author__ = 'mqm'


_web_driver_engine = None # inject here

@get('/wd/hub/status')
def get_server_status():
    return {"build": {"version": 1.0, "time": "2015-05-07T12:21:30.208824"}, "os": {"name": "linux"}}

@get('/wd/hub/sessions')
def get_active_sessions():
    result = _web_driver_engine.get_sessions()
    return result

@post('/wd/hub/session')
def create_session():
    required_capabilities = request.json and request.json.get("requiredCapabilities", {}) or {}
    desired_capabilities = request.json and request.json.get("desiredCapabilities", {}) or {}
    [session_id, session] = _web_driver_engine.create_new_session(required_capabilities, desired_capabilities)
    return {"sessionId": session_id, "status": 0, "value": desired_capabilities}

@get('/wd/hub/session/<session_id:int>/window_handle')
def get_current_window_handle(session_id):
    session = _web_driver_engine.get_session(session_id)
    current_window_handle = session.get_current_window_handle()
    return {"sessionId": session_id, "status": 0, "value": current_window_handle}

@post('/wd/hub/session/<session_id:int>/timeouts/async_script')
def get_current_window_handle(session_id):
    session = _web_driver_engine.get_session(session_id)
    timeout = request.json and request.json.get("ms", session.get_default_timeout()) or session.get_default_timeout()
    session.set_async_script_timeout(timeout)
    return {"sessionId": session_id, "status": 0, "value": timeout}
