#from utils.bottlehelpers import get, post, route, Routeable
from bottle import get, put, post, delete, route
from bottle import request
import execjs
from error_codes import *
import urllib
from base64 import b64encode
from StringIO import StringIO

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

@delete('/wd/hub/session/<session_id:int>/cookie')  # https://code.google.com/p/selenium/wiki/JsonWireProtocol#/session/:sessionId/cookie
def delete_session_cookie(session_id):
    return {"sessionId": session_id, "status": Success, "value": 0}


@get('/wd/hub/session/<session_id:int>/window_handle') # https://code.google.com/p/selenium/wiki/JsonWireProtocol#/session/:sessionId/window_handle
def get_current_window_handle(session_id):
    session = _web_driver_engine.get_session(session_id)
    current_window_id = session.get_current_window_id()
    return {"sessionId": session_id, "status": Success if current_window_id is not None else InvalidElementState, "value": urllib.quote_plus (current_window_id)}

@get('/wd/hub/session/<session_id:int>/window_handles') # https://code.google.com/p/selenium/wiki/JsonWireProtocol#/session/:sessionId/window_handles
def get_current_window_handles(session_id):
    session = _web_driver_engine.get_session(session_id)
    window_ids = session.get_window_ids()
    window_ids_encoded = [urllib.quote_plus (id) for id in window_ids]
    return {"sessionId": session_id, "status": Success, "value": window_ids_encoded}

@post('/wd/hub/session/<session_id:int>/timeouts/async_script')  # https://code.google.com/p/selenium/wiki/JsonWireProtocol#/session/:sessionId/timeouts/async_script
def set_async_script_timeout(session_id):
    session = _web_driver_engine.get_session(session_id)
    timeout = request.json and request.json.get("ms", session.get_default_timeout()) or session.get_default_timeout()
    session.set_async_script_timeout(timeout)
    return {"sessionId": session_id, "status": Success, "value": timeout}


@post('/wd/hub/session/<session_id:int>/timeouts/implicit_wait')  # https://code.google.com/p/selenium/wiki/JsonWireProtocol#/session/:sessionId/timeouts/implicit_wait
def set_implicit_wait(session_id):
    session = _web_driver_engine.get_session(session_id)
    implicit_wait = request.json and request.json.get("ms", session.get_default_implicit_wait()) or session.get_default_implicit_wait()
    session.set_implicit_wait(implicit_wait)
    return {"sessionId": session_id, "status": Success, "value": implicit_wait}

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

@post('/wd/hub/session/<session_id:int>/elements')  # https://code.google.com/p/selenium/wiki/JsonWireProtocol#/session/:sessionId/elements
def find_elements(session_id):
    session = _web_driver_engine.get_session(session_id)
    lookup_method = request.json and request.json.get("using", "id") or "id"
    value_of_locator = request.json and request.json.get("value", None) or None
    value_of_locator = urllib.unquote_plus (value_of_locator) #just in case it is an "escaped xpath id" by us
    element_locators = []
    if lookup_method == "id": # find element by id
        element_locators.extend (urllib.quote_plus (value_of_locator)) #escape xpath id
    elif lookup_method == "name": #find by name
        all_ids = session.get_all_ids_for_all_by_name(value_of_locator)
        element_locators = [urllib.quote_plus (element) for element in all_ids] #escape xpath id
    elif lookup_method == "xpath": #find by xpath
        all_ids = session.locate_with_xpath(value_of_locator)
        element_locators = [urllib.quote_plus (element) for element in all_ids] #escape xpath id
    return {"sessionId": session_id,
            "status": Success if len(element_locators) > 0 else NoSuchElement,
            "value": [{"ELEMENT": locator} for locator in element_locators]}

@post('/wd/hub/session/<session_id:int>/element')  # https://code.google.com/p/selenium/wiki/JsonWireProtocol#/session/:sessionId/element
def find_element(session_id):
    session = _web_driver_engine.get_session(session_id)
    lookup_method = request.json and request.json.get("using", "id") or "id"
    value_of_locator = request.json and request.json.get("value", None) or None
    value_of_locator = urllib.unquote_plus (value_of_locator) #just in case it is an "escaped xpath id" by us
    is_present = False
    if lookup_method == "id": # find element by id
        is_present = session.is_id_present(value_of_locator)
        value_of_locator = urllib.quote_plus (value_of_locator)
    elif lookup_method == "name": #find by name
        all_ids = session.get_all_ids_for_all_by_name(value_of_locator)
        if len(all_ids)>0 :
            is_present = True
            value_of_locator = urllib.quote_plus (all_ids[0]) #escape xpath id
    elif lookup_method == "xpath": #find by xpath
        all_ids = session.locate_with_xpath(value_of_locator)
        if len(all_ids)>0 :
            is_present = True
            value_of_locator = urllib.quote_plus (all_ids[0])
    return {"sessionId": session_id,
            "status": Success if is_present else NoSuchElement,
            "value": {"ELEMENT": "%s" % value_of_locator if is_present else None}}

@get('/wd/hub/session/<session_id:int>/element/<element_id>/displayed')  # https://code.google.com/p/selenium/wiki/JsonWireProtocol#/session/:sessionId/element/:id/displayed
def element_is_displayed(session_id, element_id):
    session = _web_driver_engine.get_session(session_id)
    element_id = urllib.unquote_plus(element_id) #just in case it is an "escaped xpath id" by us
    elements = session.get_all_by_id(element_id)
    is_displayed = session.is_element_displayed(elements[0]) if len(elements)>0 else False
    return {"sessionId": session_id,
            "status": Success,
            "value": is_displayed}

@get('/wd/hub/session/<session_id:int>/element/<element_id>/enabled')  # https://code.google.com/p/selenium/wiki/JsonWireProtocol#/session/:sessionId/element/:id/enabled
def element_is_enabled(session_id, element_id):
    session = _web_driver_engine.get_session(session_id)
    element_id = urllib.unquote_plus(element_id) #just in case it is an "escaped xpath id" by us
    elements = session.get_all_by_id(element_id)
    is_enabled = session.is_element_enabled(elements[0]) if len(elements)>0 else False
    return {"sessionId": session_id,
            "status": Success,
            "value": is_enabled}

@post('/wd/hub/session/<session_id:int>/element/<element_id>/click')  # https://code.google.com/p/selenium/wiki/JsonWireProtocol#/session/:sessionId/element/:id/click
def click_element(session_id, element_id):
    session = _web_driver_engine.get_session(session_id)
    element_id = urllib.unquote_plus(element_id) #just in case it is an "escaped xpath id" by us
    clicked = session.click (element_id)
    return {"sessionId": session_id,
            "status": Success if clicked is not None else NoSuchElement,
            "value": clicked}


@get('/wd/hub/session/<session_id:int>/element/<element_id>/name')  # saw with protocol tracing
def get_element_tag_name(session_id, element_id):
    session = _web_driver_engine.get_session(session_id)
    element_id = urllib.unquote_plus(element_id) #just in case it is an "escaped xpath id" by us
    elements = session.get_all_by_id(element_id)
    element_tag_name = session.get_element_tag_name(elements[0]) if len(elements)>0 else None
    return {"sessionId": session_id,
            "status": Success if element_tag_name is not None else NoSuchElement,
            "value": "%s" % element_tag_name}

#@post('/wd/hub/session/<session_id:int>/execute_async')  # https://code.google.com/p/selenium/wiki/JsonWireProtocol#/session/:sessionId/execute_async
@post('/wd/hub/session/<session_id:int>/execute')  # https://code.google.com/p/selenium/wiki/JsonWireProtocol#/session/:sessionId/execute
def execute_script(session_id):
    # session = _web_driver_engine.get_session(session_id)
    # script = request.json and request.json.get("script", "") or ""
    # eval_result = ""
    # try:
    #     eval_result = execjs.get("Node").eval(script) #TODO: one JS VM per session, not a global one
    # except SyntaxError:
    #     return {"sessionId": session_id, "status": JavaScriptError, "value": None}
    # except RuntimeError, e:
    #     return {"sessionId": session_id, "status": JavaScriptError, "value": None}
    # return {"sessionId": session_id,
    #         "status": Success if eval_result is not None else JavaScriptError,
    #         "value": "%s" % eval_result if eval_result is not None else None}
    return {"sessionId": session_id,
            "status": Success,
            "value": None}


@post('/wd/hub/session/<session_id:int>/frame')  # https://code.google.com/p/selenium/wiki/JsonWireProtocol#/session/:sessionId/frame
def select_frame (session_id):
    # For MacOS, we pretend a Dialog (a sheet) is a Selenium frame. https://developer.apple.com/library/mac/documentation/Cocoa/Conceptual/Sheets/Concepts/AboutSheets.html
    session = _web_driver_engine.get_session(session_id)
    value_of_locator = request.json and request.json.get("id", None) or None
    selected_ok = session.select_frame_by_id(value_of_locator)
    return {"sessionId": session_id,
            "status": Success if selected_ok else NoSuchElement,
            "value": {"ELEMENT": "%s" % value_of_locator if selected_ok else None}}

@get('/wd/hub/session/<session_id:int>/element/<element_id>/attribute/type')  # saw with protocol tracing
def find_element_by_name(session_id, element_id):
    session = _web_driver_engine.get_session(session_id)
    element_id = urllib.unquote_plus(element_id) #just in case it is an "escaped xpath id" by us
    elements = session.get_all_by_id(element_id)
    element_attrib_type = session.get_element_attrib_type(elements[0]) if len(elements)>0 else None
    return {"sessionId": session_id,
            "status": Success if element_attrib_type is not None else NoSuchElement,
            "value": "%s" % element_attrib_type}

@post('/wd/hub/session/<session_id:int>/element/<element_id>/value')  # https://code.google.com/p/selenium/wiki/JsonWireProtocol#/session/:sessionId/element/:id/value
def append_keys_to_element(session_id, element_id):
    session = _web_driver_engine.get_session(session_id)
    element_id = urllib.unquote_plus(element_id) #just in case it is an "escaped xpath id" by us
    keys_list = request.json and request.json.get("value", None) or None
    elements = session.get_all_by_id(element_id)
    for keys in keys_list:
        session.append_text(elements[0], keys)
    return {"sessionId": session_id,
            "status": Success if len(elements)>0 else NoSuchElement,
            "value": True}

@get('/wd/hub/session/<session_id:int>/screenshot')  #https://code.google.com/p/selenium/wiki/JsonWireProtocol#/session/:sessionId/screenshot
def take_screenshot (session_id):
    session = _web_driver_engine.get_session(session_id)
    screenshot = session.take_screenshot()
    base_64 = None
    if screenshot is not None:
        #screenshot.save("last_screenshot_returned.png", "PNG") #debug
        screenshot.load() # otherwise, lazy and no bytes in memory, broken img
        buffer_in_memory = StringIO()
        screenshot.save(buffer_in_memory, 'PNG')
        buffer_in_memory.seek(0)
        base_64 = b64encode(buffer_in_memory.getvalue())
    return {"sessionId": session_id,
            "status": Success if base_64 else NoSuchWindow,
            "value": base_64}

@delete('/wd/hub/session/<session_id:int>/window') # https://code.google.com/p/selenium/wiki/JsonWireProtocol#/session/:sessionId/window
def close_current_window(session_id):
    session = _web_driver_engine.get_session(session_id)
    closed = session.close_current_window() #FIXME: test if closed ok and return correct result
    return {"sessionId": session_id, "status": Success if closed else NoSuchWindow, "value": closed}

@post('/wd/hub/session/<session_id:int>/window') # https://code.google.com/p/selenium/wiki/JsonWireProtocol#/session/:sessionId/window
def select_window(session_id):
    session = _web_driver_engine.get_session(session_id)
    window_definition = request.json or {}
    def_value = None
    ok_focus_change = False
    if "id" in window_definition: # find element by id
        def_value = window_definition["id"]
    elif "name" in window_definition: #find by name
        def_value = window_definition["name"]
    if def_value is not None:
        ok_focus_change = session.focus_on_window(urllib.unquote_plus(def_value))
    return {"sessionId": session_id,
            "status": Success if ok_focus_change else NoSuchWindow}


@post('/wd/hub/session/<session_id:int>/element/<element_id>/clear')  # https://code.google.com/p/selenium/wiki/JsonWireProtocol#/session/:sessionId/element/:id/clear
def element_clear(session_id, element_id):
    session = _web_driver_engine.get_session(session_id)
    element_id = urllib.unquote_plus(element_id) #just in case it is an "escaped xpath id" by us
    elements = session.get_all_by_id(element_id)
    cleared = False
    if len(elements)>0:
        cleared = session.clear_element(elements[0])
    return {"sessionId": session_id,
            "status": Success if cleared else InvalidElementState,
            "value": cleared}

@get('/wd/hub/session/<session_id:int>/title')  # https://code.google.com/p/selenium/wiki/JsonWireProtocol#/session/:sessionId/title
def window_title(session_id):
    session = _web_driver_engine.get_session(session_id)
    window_title = session.get_current_window_title()
    return {"sessionId": session_id,
            "status": Success if window_title is not None else InvalidElementState,
            "value": window_title}

@get('/wd/hub/session/<session_id:int>/url')  # https://code.google.com/p/selenium/wiki/JsonWireProtocol#/session/:sessionId/url
def window_url(session_id):
    session = _web_driver_engine.get_session(session_id)
    current_window_id = session.get_current_window_id()
    return {"sessionId": session_id, "status": Success if current_window_id is not None else InvalidElementState, "value": urllib.quote_plus (current_window_id)}

@post('/wd/hub/session/<session_id:int>/element/active')  # https://code.google.com/p/selenium/wiki/JsonWireProtocol#/session/:sessionId/element/active
def get_active_element(session_id):
    session = _web_driver_engine.get_session(session_id)
    active_element_id = session.get_active_element_id()
    return {"sessionId": session_id,
            "status": Success if active_element_id is not None else InvalidElementState,
            "value": {"ELEMENT": urllib.quote_plus(active_element_id)}}
