__author__ = 'mqm'

class Session:

    def __init__(self, required_capabilities, desired_capabilities):
        self._required_capabilities = required_capabilities
        self._desired_capabilities = desired_capabilities

    def get_current_window_handle(self):
        return 1