__author__ = 'mqm'

import atomac
import time
import re

class Session:

    def __init__(self, required_capabilities, desired_capabilities):
        self._required_capabilities = required_capabilities
        self._desired_capabilities = desired_capabilities
        self._async_script_timeout = self.get_default_timeout()
        self._timeouts = {}
        self._bundle_id = desired_capabilities.get("bundleId", "")
        self._should_launch_app = desired_capabilities.get("shouldLaunch", True) == True
        self._should_terminate_app = desired_capabilities.get("shouldTerminate", True) == True
        self._current_frame = None
        if self._should_launch_app:
            atomac.launchAppByBundleId(self._bundle_id)
        time.sleep(1) #FIXME: wait until app up or timeout
        self._app = atomac.getAppRefByBundleId(self._bundle_id)

    def delete(self):
        if self._should_terminate_app:
            atomac.terminateAppByBundleId(self._bundle_id)

    def get_window_handles(self):
        windows = self._app.windows()
        return [window.AXIdentifier for window in windows]

    def get_current_window_handle(self):
        return self.get_window_handles()[0]

    def _get_current_window(self):
        return self._app.windows()[0]

    def get_default_timeout(self):
        return 10000

    def set_async_script_timeout(self, timeout):
        self._async_script_timeout = timeout

    def set_timeout(self, timeout_type, timeout):
        self._timeouts[timeout_type]=timeout

    def open_url(self, url_to_open):
        return True

    def _get_current_pane(self):
        if self._current_frame is not None:
            return self._current_frame
        else:
            return self._get_current_window()

    def _get_all_by_id (self, id_to_get):
        if self._get_current_pane().AXIdentifier == id_to_get:
            return [self._get_current_pane()]
        elif id_to_get.find('/'): #xpath
            return self._locate_with_xpath(id_to_get)
        else:
            return self._get_current_pane().findAllR(AXIdentifier=id_to_get)

    def _get_first_by_id (self, id_to_get):
        if self._get_current_pane().AXIdentifier == id_to_get:
            return [self._get_current_pane()]
        elif id_to_get.find('/'): #xpath
            return self._locate_with_xpath(id_to_get)[0]
        else:
            return self._get_current_pane().findFirstR(AXIdentifier=id_to_get)

    def is_id_present(self, id_to_verify):
        if id_to_verify.find('/'):
            return len(self._locate_with_xpath(id_to_verify)) > 0
        else:
            return len(self._get_all_by_id(id_to_verify)) > 0

    def _get_all_by_name (self, name_to_get):
        if name_to_get == None or self._get_current_pane().AXIdentifier == name_to_get:
            return [self._get_current_pane()]
        else:
            return self._get_current_pane().findAllR(AXDescription=name_to_get)

    def _get_all_ids_for_all_by_name (self, name_to_get):
        return [widget.AXIdentifier for widget in self._get_all_by_name(name_to_get)]

    def _get_first_by_name (self, name_to_get):
        if name_to_get == None or self._get_current_pane().AXIdentifier == name_to_get:
            return self._get_current_pane()
        else:
            return self._get_current_pane().findFirstR(AXDescription=name_to_get)

    def is_name_present(self, name_to_verify):
        return len(self._get_all_by_name(name_to_verify)) > 0

    def select_frame_by_id(self, id_to_verify):
        sheets = [sheet for sheet in self._get_current_window().sheets() if sheet.AXIdentifier == id_to_verify]
        if len(sheets) > 0:
            self._current_frame = sheets[0]
            return True
        else:
            self._current_frame = None
            return False

    def click(self, id_to_click):
        elements = self._get_all_by_id(id_to_click)
        if len(elements) == 0:
            return False
        elements[0].Press()
        return True

    def get_element_tag_name (self, ui_element):
        return ui_element.AXRole

    def get_element_attrib_type(self, ui_element):
        return ui_element.AXRoleDescription

    def send_keys(self, ui_element, keys):
        return ui_element.sendKeys(keys)

    def is_element_displayed(self, ui_element):
        if "AXEnabled" in ui_element.getAttributes():
            return ui_element.AXEnabled == "1"
        else:
            return True

    def is_element_enabled(self, ui_element):
        if "AXEnabled" in ui_element.getAttributes():
            return ui_element.AXEnabled == "1"
        else:
            return True

    def _locate_with_xpath (self, xpath_expression):
        parts = xpath_expression.split('/')
        current_node = self._get_current_pane()
        for part in parts:
            search_result_like_array = re.search('(\w+)[[]?(\d+)[]]?', part)
            search_result_like_property= re.search('(\w+)[[]?(\w+)=([^]]+)[]]?', part)
            if search_result_like_array is not None:
                role = search_result_like_array.group(1)
                index = int(search_result_like_array.group(2))
                current_node = current_node.findAll(AXRole=role)[index-1]
            elif search_result_like_property is not None:
                role = search_result_like_property.group(1)
                prop_name = search_result_like_property.group(2)
                prop_value = search_result_like_property.group(3)
                if prop_name == "name":
                    current_node = current_node.findFirst(AXRole=role, AXDescription=prop_value)
                elif prop_name == "id":
                    current_node = current_node.findFirst(AXRole=role, AXIdentifier=prop_value)
                else:
                    current_node = current_node.findFirst(AXRole=part)
            else:
                current_node = current_node.findFirst(AXRole=part)
        return [current_node] if current_node is not None else []
