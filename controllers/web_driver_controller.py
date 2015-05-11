from utils.bottlehelpers import route, Routeable

__author__ = 'mqm'


class WebDriverController (Routeable):

    def __init__(self, web_driver_engine):
        super(WebDriverController, self).__init__()
        self._web_driver_engine = web_driver_engine

    @route('/wd/hub/status', method='GET')
    def get_server_status(self):
        return {"build": {"version": 1.0, "time": "2015-05-07T12:21:30.208824"}, "os": {"name": "linux"}}

    @route('/wd/hub/sessions', method='GET')
    def get_active_sessions(self):
        result = self._web_driver_engine.get_sessions()
        return result