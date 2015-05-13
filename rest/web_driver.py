#from utils.bottlehelpers import get, post, route, Routeable
from bottle import get, put, post, delete, route

from bottle import request


__author__ = 'mqm'


_web_driver_engine = None # inject here

@get('/wd/hub/status')  # https://code.google.com/p/selenium/wiki/JsonWireProtocol#/status
def get_server_status():
    return {"build": {"version": 1.0, "time": "2015-05-07T12:21:30.208824"}, "os": {"name": "linux"}}

@get('/wd/hub/sessions')  # https://code.google.com/p/selenium/wiki/JsonWireProtocol#/sessions
def get_active_sessions():
    result = _web_driver_engine.get_sessions()
    return result

@post('/wd/hub/session')  # https://code.google.com/p/selenium/wiki/JsonWireProtocol#/session
def create_session():
    required_capabilities = request.json and request.json.get("requiredCapabilities", {}) or {}
    desired_capabilities = request.json and request.json.get("desiredCapabilities", {}) or {}
    [session_id, session] = _web_driver_engine.create_new_session(required_capabilities, desired_capabilities)
    return {"sessionId": session_id, "status": 0, "value": desired_capabilities}

@delete('/wd/hub/session/<session_id:int>')  # https://code.google.com/p/selenium/wiki/JsonWireProtocol#/session/:sessionId/window_handle
def delete_session(session_id):
    _web_driver_engine.delete_session(session_id)
    return {"sessionId": session_id, "status": 0, "value": 0}

@get('/wd/hub/session/<session_id:int>/window_handle') # https://code.google.com/p/selenium/wiki/JsonWireProtocol#/session/:sessionId/window_handle
def get_current_window_handle(session_id):
    session = _web_driver_engine.get_session(session_id)
    current_window_handle = session.get_current_window_handle()
    return {"sessionId": session_id, "status": 0, "value": current_window_handle}

@post('/wd/hub/session/<session_id:int>/timeouts/async_script')  # https://code.google.com/p/selenium/wiki/JsonWireProtocol#/session/:sessionId/timeouts/async_script
def set_async_script_timeout(session_id):
    session = _web_driver_engine.get_session(session_id)
    timeout = request.json and request.json.get("ms", session.get_default_timeout()) or session.get_default_timeout()
    session.set_async_script_timeout(timeout)
    return {"sessionId": session_id, "status": 0, "value": timeout}

@post('/wd/hub/session/<session_id:int>/timeouts')  # https://code.google.com/p/selenium/wiki/JsonWireProtocol#/session/:sessionId/timeouts
def set_timeouts(session_id):
    session = _web_driver_engine.get_session(session_id)
    timeout_type = request.json and request.json.get("type", "default") or "default"
    timeout = request.json and request.json.get("ms", session.get_default_timeout()) or session.get_default_timeout()
    session.set_timeout(timeout_type, timeout)
    return {"sessionId": session_id, "status": 0, "value": timeout}

@post('/wd/hub/session/<session_id:int>/url')  # https://code.google.com/p/selenium/wiki/JsonWireProtocol#/session/:sessionId/url
def set_timeouts(session_id):
    session = _web_driver_engine.get_session(session_id)
    url_to_open = request.json and request.json.get("url", "/") or "/"
    open_result = session.open_url(url_to_open)
    return {"sessionId": session_id, "status": open_result, "value": url_to_open}

@post('/wd/hub/session/<session_id:int>/element')  # https://code.google.com/p/selenium/wiki/JsonWireProtocol#/session/:sessionId/element
def set_timeouts(session_id):
    session = _web_driver_engine.get_session(session_id)
    id_to_verify = request.json and request.json.get("id", None) or None
    is_id_present = False if id_to_verify is None else session.is_id_present(id_to_verify)
    return {"sessionId": session_id, "status": 0, "value": {"ELEMENT": id_to_verify if is_id_present else None}}

