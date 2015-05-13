#from utils.bottlehelpers import get, post, route, Routeable
from bottle import get, put, post, delete, route
from bottle import request
import execjs
from error_codes import *

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
    #desired_capabilities["javascriptEnabled"] = False # Can' do this. Xebium refuses. we are meant to drive a desktop app. No JS supported
    [session_id, session] = _web_driver_engine.create_new_session(required_capabilities, desired_capabilities)
    return {"sessionId": session_id, "status": Success, "value": desired_capabilities}

@delete('/wd/hub/session/<session_id:int>')  # https://code.google.com/p/selenium/wiki/JsonWireProtocol#/session/:sessionId/window_handle
def delete_session(session_id):
    _web_driver_engine.delete_session(session_id)
    return {"sessionId": session_id, "status": Success, "value": 0}

@get('/wd/hub/session/<session_id:int>/window_handle') # https://code.google.com/p/selenium/wiki/JsonWireProtocol#/session/:sessionId/window_handle
def get_current_window_handle(session_id):
    session = _web_driver_engine.get_session(session_id)
    current_window_handle = session.get_current_window_handle()
    return {"sessionId": session_id, "status": Success, "value": current_window_handle}

@post('/wd/hub/session/<session_id:int>/timeouts/async_script')  # https://code.google.com/p/selenium/wiki/JsonWireProtocol#/session/:sessionId/timeouts/async_script
def set_async_script_timeout(session_id):
    session = _web_driver_engine.get_session(session_id)
    timeout = request.json and request.json.get("ms", session.get_default_timeout()) or session.get_default_timeout()
    session.set_async_script_timeout(timeout)
    return {"sessionId": session_id, "status": Success, "value": timeout}

@post('/wd/hub/session/<session_id:int>/timeouts')  # https://code.google.com/p/selenium/wiki/JsonWireProtocol#/session/:sessionId/timeouts
def set_timeouts(session_id):
    session = _web_driver_engine.get_session(session_id)
    timeout_type = request.json and request.json.get("type", "default") or "default"
    timeout = request.json and request.json.get("ms", session.get_default_timeout()) or session.get_default_timeout()
    session.set_timeout(timeout_type, timeout)
    return {"sessionId": session_id, "status": Success, "value": timeout}

@post('/wd/hub/session/<session_id:int>/url')  # https://code.google.com/p/selenium/wiki/JsonWireProtocol#/session/:sessionId/url
def open_url(session_id):
    session = _web_driver_engine.get_session(session_id)
    url_to_open = request.json and request.json.get("url", "/") or "/"
    opened = session.open_url(url_to_open)
    return {"sessionId": session_id,
            "status": Success if opened else NoSuchWindow,
            "value": url_to_open}

@post('/wd/hub/session/<session_id:int>/element')  # https://code.google.com/p/selenium/wiki/JsonWireProtocol#/session/:sessionId/element
def find_element(session_id):
    session = _web_driver_engine.get_session(session_id)
    lookup_method = request.json and request.json.get("using", "id") or "id"
    value_of_locator = request.json and request.json.get("value", None) or None
    is_id_present = False
    if lookup_method == "id": # find element by id
        is_id_present = session.is_id_present(value_of_locator)
    return {"sessionId": session_id,
            "status": Success if is_id_present else NoSuchElement,
            "value": {"ELEMENT": "%s" % value_of_locator if is_id_present else None}}

@get('/wd/hub/session/<session_id:int>/element/<element_name>/name')  # saw with protocol tracing
def find_element_by_name(session_id,element_name):
    session = _web_driver_engine.get_session(session_id)
    element_name = element_name[1:] # the name comes with a + prefix
    is_name_present = session.is_name_present(element_name)
    return {"sessionId": session_id,
            "status": Success if is_name_present else NoSuchElement,
            "value": {"ELEMENT": "%s" % element_name if is_name_present else None}}

#@post('/wd/hub/session/<session_id:int>/execute_async')  # https://code.google.com/p/selenium/wiki/JsonWireProtocol#/session/:sessionId/execute_async
@post('/wd/hub/session/<session_id:int>/execute')  # https://code.google.com/p/selenium/wiki/JsonWireProtocol#/session/:sessionId/execute
def execute_script(session_id):
    session = _web_driver_engine.get_session(session_id)
    script = request.json and request.json.get("script", "") or ""
    eval_result = ""
    # try:
    #     eval_result = execjs.eval(script) #TODO: one JS VM per session, not a global one
    # except SyntaxError:
    #     eval_result = None
    # except RuntimeError, e:
    #     eval_result = None
    return {"sessionId": session_id,
            "status": Success if eval_result is not None else JavaScriptError,
            "value": "%s" % eval_result if eval_result is not None else None}

