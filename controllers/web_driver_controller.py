from utils.bottlehelpers import route, Routeable

__author__ = 'mqm'

class WebDriverController (Routeable):

    def __init__ (self, web_driver_engine):
        super(WebDriverController, self).__init__()
        self._web_driver_engine = web_driver_engine

    @route('/sessions', method='GET')
    def get_active_sessions (self):
        result = self._web_driver_engine.get_sessions()
        return result