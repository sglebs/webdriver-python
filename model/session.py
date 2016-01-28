__author__ = 'mqm'

import atomac
import time
import re
import pyscreeze

class Session:

    def __init__(self, required_capabilities, desired_capabilities):
        self._required_capabilities = required_capabilities
        self._desired_capabilities = desired_capabilities
        self._async_script_timeout = self.get_default_timeout()
        self._timeouts = {}
        self._bundle_id = desired_capabilities.get("bundleId", "")
        self._should_launch_app = desired_capabilities.get("shouldLaunch", True) == True
        self._should_terminate_app = desired_capabilities.get("shouldTerminate", True) == True
        if self._should_launch_app:
            atomac.launchAppByBundleId(self._bundle_id)
            time.sleep(2) #FIXME: wait until app up or timeout
        self._app = atomac.getAppRefByBundleId(self._bundle_id)
        self._current_window = None
        self._active_element = None
        self._update_current_window_to_be_the_first()
        self._cache_of_elements_by_id = {} #FIXME: need to limit the cache and also purge on new windows etc
        self._cache_of_element_ids_by_element_name = {} #FIXME: need to limit the cache and also purge on new windows etc

    def delete(self):
        if self._should_terminate_app:
            atomac.terminateAppByBundleId(self._bundle_id)

    def _set_current_window(self, window):
        self._current_window = window
        self._current_frame = None
        self._active_element = window #FIXME. By default we make the focus go to the window. No atomac API to get element with focus

    def _update_current_window_to_be_the_first(self):
        self._set_current_window(self._get_first_window())

    def _get_first_window (self):
        return self._app.findFirst (AXRole="AXWindow")

    def get_window_ids(self):
        return [self.id_of_element(window) for window in self._app.windows()]

    def get_current_window_id(self):
        return self.id_of_element(self._get_current_window())

    def _get_current_window(self):
        if len(self._app.windows()) == 0:
            self._current_window = None # FIXME: the correct approach is to hook a listener on window close and nil the inst var below
        return self._current_window

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
        if self._get_current_pane() is None:
            return []
        if self.id_of_element(self._get_current_pane()) == id_to_get:
            return [self._get_current_pane()]
        elif "/" in id_to_get or "[" in id_to_get: #xpath
            return self._locate_elements_with_xpath(id_to_get)
        else:
            first = self._get_current_pane().findFirstR(AXIdentifier=id_to_get) #findFIrst because there can be only 1 with a given ID (unique)
            if first is None:
                return []
            else:
                return [first]

    def get_all_by_id (self, id_to_get):
        cached = self._cache_of_elements_by_id.get(id_to_get, None)
        if not cached:
            cached = self._get_all_by_id(id_to_get)
            self._cache_of_elements_by_id[id_to_get] = cached
        return cached

    def _get_first_by_id (self, id_to_get):
        if self.id_of_element(self._get_current_pane()) == id_to_get:
            return [self._get_current_pane()]
        elif id_to_get.find('/'): #xpath
            all_found = self._locate_elements_with_xpath(id_to_get)
            if len(all_found) == 0:
                return None
            else:
                return all_found[0]
        else:
            return self._get_current_pane().findFirstR(AXIdentifier=id_to_get)

    def is_id_present(self, id_to_verify):
        if "/" in id_to_verify:
            return len(self._locate_elements_with_xpath(id_to_verify)) > 0
        else:
            return len(self.get_all_by_id(id_to_verify)) > 0

    def _get_all_elements_by_name (self, name_to_get):
        if name_to_get == None or name_to_get == "#" or self.id_of_element(self._get_current_pane()) == name_to_get:
            return [self._get_current_pane()]
        else:
            return self._get_current_pane().findAllR(AXDescription=name_to_get)

    def get_all_ids_for_all_by_name (self, name_to_get):
        cached_ids = self._cache_of_element_ids_by_element_name.get(name_to_get, None)
        if not cached_ids:
            elements = [element for element in self._get_all_elements_by_name(name_to_get)]
            cached_ids = [self.id_of_element(element) for element in elements]
            self._cache_of_element_ids_by_element_name[name_to_get] = cached_ids
        return cached_ids

    def _get_first_by_name (self, name_to_get):
        if name_to_get == None or name_to_get == "#" or self.id_of_element(self._get_current_pane()) == name_to_get:
            return self._get_current_pane()
        else:
            return self._get_current_pane().findFirstR(AXDescription=name_to_get)

    def is_name_present(self, name_to_verify):
        return len(self._get_all_elements_by_name(name_to_verify)) > 0

    def select_frame_by_id(self, id_to_verify):
        sheets = [sheet for sheet in self._get_current_window().sheets() if sheet.AXIdentifier == id_to_verify]
        if len(sheets) > 0:
            self._current_frame = sheets[0]
            return True
        else:
            self._current_frame = None
            return False

    def click(self, id_to_click):
        elements = self.get_all_by_id(id_to_click)
        if len(elements) == 0:
            return False
        elements[0].Press()
        self._active_element = elements[0]
        return True

    def get_element_tag_name (self, ui_element):
        return ui_element.AXRole

    def get_element_attrib_type(self, ui_element):
        return ui_element.AXRoleDescription

    def clear_element(self, ui_element):
        if ui_element.AXRole == "AXTextField":
            ui_element.AXValue = ''
        return True

    def append_text(self, ui_element, text):
        new_text = self._adjust_keys(text)
        self._active_element = ui_element
        # if ui_element.AXRole == "AXTextField" and ui_element.AXValue is not None:
        #     ui_element.AXValue = ui_element.AXValue + new_text # FIXME: find a way to sendKeys to the widget. we use a workaround of slamming its value
        #     return True
        # else:
        return ui_element.sendKeys(new_text) #FIXME: in atomac, sendKeys is global, not to the widget, even though it is an instance method :-(

    def _adjust_keys(self, keys):
        new_keys = keys.replace(u"\uE004", "\t").replace(u"\uE006", "\n") #atomac expects \t, \n to replace with MacOS values
        return new_keys

    def send_keys(self, ui_element, keys):
        new_keys = self._adjust_keys(keys)
        return ui_element.sendKeys(new_keys) #FIXME: in atomac, sendKeys is global, not to the widget, even though it is an instance method :-(

    def is_element_displayed(self, ui_element):
        if "AXEnabled" in ui_element.getAttributes():
            return ui_element.AXEnabled == "1"
        else:
            return True #FIXME: find a way in atomac

    def is_element_enabled(self, ui_element):
        if "AXEnabled" in ui_element.getAttributes():
            return True
            #return ui_element.AXEnabled == "1"
        else:
            return True #FIXME: find a way in atomac

    def _locate_elements_with_xpath (self, xpath_expression):
        parts = xpath_expression.split('/')
        current_element = self._get_current_pane()
        for part in parts:
            if current_element is None:
                break
            if part == "":
                current_element = self._app #topmost root if xpath starts with /
                continue
            search_result_like_array = re.search('(\w+)[[](\d+)[]]', part)
            search_result_like_property= re.search('(\w+)[[](\w+)=([^]]+)[]]', part)
            if search_result_like_array is not None:
                role = search_result_like_array.group(1)
                index = int(search_result_like_array.group(2))
                current_element = current_element.findAll(AXRole=role)[index-1]
            elif search_result_like_property is not None:
                role = search_result_like_property.group(1)
                prop_name = search_result_like_property.group(2)
                prop_value = search_result_like_property.group(3)
                if prop_name == "name":
                    current_element = current_element.findFirst(AXRole=role, AXDescription=prop_value)
                elif prop_name == "id":
                    current_element = current_element.findFirst(AXRole=role, AXIdentifier=prop_value)
                elif prop_name == "title":
                    current_element = current_element.findFirst(AXRole=role, AXTitle=prop_value)
                else:
                    current_element = current_element.findFirst(AXRole=part)
            else:
                current_element = current_element.findFirst(AXRole=part)
        return [current_element] if current_element is not None else []

    def id_of_element (self, element):
        if element is None:
            return None
        id = element.AXIdentifier
        if id is None:
            return str(hash(element))
        else:
            return id

    def locate_with_xpath (self, xpath_expression):
        elements = [element for element in self._locate_elements_with_xpath(xpath_expression)]
        for element in elements: #cache all IDs which we found by xpath, for speed in subsequent calls - atomac is very slow to find by id recursively
            self._cache_of_elements_by_id[self.id_of_element(element)] = [element] #FIXME: our API is sometimes based on collections
        return [self.id_of_element(element) for element in elements]

    def take_screenshot(self):
        current_pane = self._get_current_pane()
        if current_pane is None:
            return None
        rect = [current_pane.AXPosition[0], current_pane.AXPosition[1], current_pane.AXSize[0], current_pane.AXSize[1]]
        return pyscreeze.screenshot(region=rect)

    def close_current_window(self):
        current_pane = self._get_current_pane()
        if current_pane is None:
            return False
        close_button = current_pane.AXCloseButton
        if close_button is not None:
            close_button.Press()
            self._update_current_window_to_be_the_first()
        return close_button is not None

    def get_current_window_title(self):
        current_pane = self._get_current_pane()
        if current_pane is None:
            return None
        else:
            return current_pane.AXTitle

    def focus_on_window(self, window_locator):
        windows = [window for window in self._app.windows() if window.AXIdentifier == window_locator]
        if windows is None:
            return False
        else:
            self._set_current_window(windows[0])
            return True

    def get_active_element_id(self):
        return self.id_of_element(self._active_element)