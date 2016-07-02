import sys
if sys.platform == 'darwin':
    from model.mac_session import Session
if sys.platform == 'win32':
    from model.win_session import Session

import time

__author__ = 'mqm'


class WebDriverEngine:

    def __init__(self):
        self._sessions = {}

    def get_sessions(self):
        return self._sessions

    def get_session(self, session_id):
        return self._sessions.get(session_id, None)

    def delete_session(self, session_id):
        session = self._sessions.get (session_id, None)
        if session is not None:
            session.delete()
            del self._sessions[session_id]

    def create_new_session(self, required_capabilities, desired_capabilities):
        new_session = Session(required_capabilities, desired_capabilities)
        session_id = (int) (time.time()*1000)
        self._sessions[session_id] = new_session
        self._sessions[session_id] = new_session
        return [session_id, new_session]