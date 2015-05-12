__author__ = 'mqm'

class Session:

    def __init__(self, required_capabilities, desired_capabilities):
        self._required_capabilities = required_capabilities
        self._desired_capabilities = desired_capabilities
        self._async_script_timeout = self.get_default_timeout()
        self._timeouts = {}

    def get_current_window_handle(self):
        return 1

    def get_default_timeout(self):
        return 10000

    def set_async_script_timeout(self, timeout):
        self._async_script_timeout = timeout

    def set_timeout(self, timeout_type, timeout):
        self._timeouts[timeout_type]=timeout