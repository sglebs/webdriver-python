from session import Session
import datetime

__author__ = 'mqm'


class WebDriverEngine:

    def __init__(self):
        self._sessions = {}

    def get_sessions(self):
        return self._sessions

    def get_session(self, session_id):
        return self._sessions.get(session_id, None)

    def create_new_session(self, required_capabilities, desired_capabilities):
        new_session = Session(required_capabilities, desired_capabilities)
        session_id = datetime.datetime.utcnow().isoformat()
        self._sessions[session_id] = new_session
        self._sessions[session_id] = new_session
        return [session_id, new_session]