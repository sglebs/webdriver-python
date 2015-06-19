__author__ = 'mqm'

import atomac

class Session:

    def __init__(self, required_capabilities, desired_capabilities):
        self._required_capabilities = required_capabilities
        self._desired_capabilities = desired_capabilities
        self._async_script_timeout = self.get_default_timeout()
        self._timeouts = {}
        self._bundle_id = desired_capabilities.get("bundleId", "")
        self._should_launch_app = desired_capabilities.get("shouldLaunch", True)
        self._should_terminate_app = desired_capabilities.get("shouldTerminate", True)
        self._current_frame = None
        if self._should_launch_app:
            atomac.launchAppByBundleId(self._bundle_id)
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

    def _get_by_id (self, id_to_get):
        return [child for child in self._get_current_pane().AXChildren if child.AXIdentifier == id_to_get]

    def is_id_present(self, id_to_verify):
        return len(self._get_by_id(id_to_verify)) > 0

    def _get_by_name (self, name_to_get):
        # we test if the AXTitle attribute does exist first, or attempting to read it may cause an exception. That is why we short-cut with "and"
        return [child for child in self._get_current_pane().AXChildren if "AXTitle" in child.getAttributes() and child._getAttribute("AXTitle") == name_to_get]

    def is_name_present(self, name_to_verify):
        return len(self._get_by_name(name_to_verify)) > 0

    def select_frame_by_id(self, id_to_verify):
        sheets = [sheet for sheet in self._get_current_window().sheets() if sheet.AXIdentifier == id_to_verify]
        if len(sheets) > 0:
            self._current_frame = sheets[0]
            return True
        else:
            self._current_frame = None
            return False

    def click(self, id_to_click):
        elements = self._get_by_id(id_to_click)
        if len(elements) == 0:
            return False
        elements[0].Press()
        return True
