from session import Session
__author__ = 'mqm'


class WebDriverEngine:

    _sessions = {}

    def get_sessions(self):
        return self._sessions

    def create_new_session(self, required_capabilities, desired_capabilities):
        new_session = Session(required_capabilities, desired_capabilities)
        return new_session