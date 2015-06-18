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
        if self._should_launch_app:
            atomac.launchAppByBundleId(self._bundle_id)
        self._app = atomac.getAppRefByBundleId(self._bundle_id)

    def delete (self):
        if self._should_terminate_app:
            atomac.terminateAppByBundleId(self._bundle_id)

    def get_window_handles(self):
        windows = self._app.windows()
        return [window.AXIdentifier for window in windows]

    def get_current_window_handle(self):
        return self.get_window_handles()[0]

    def get_default_timeout(self):
        return 10000

    def set_async_script_timeout(self, timeout):
        self._async_script_timeout = timeout

    def set_timeout(self, timeout_type, timeout):
        self._timeouts[timeout_type]=timeout

    def open_url(self, url_to_open):
        return True

    def is_id_present(self, id_to_verify):
        return True

    def is_name_present(self, name_to_verify):
        return True

