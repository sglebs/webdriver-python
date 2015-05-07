from model.web_driver_engine import WebDriverEngine
from controllers.web_driver_controller import WebDriverController

# This is a non-OO controller. It has to be included so that Bottle will activate it
import controllers.heartbeat

def setup_server (application):
    application.installed_plugins = []

    web_driver_engine = WebDriverEngine()
    web_driver_controller = WebDriverController(web_driver_engine)


def teardown_server (application):
    for plugin in application.installed_plugins:
       application.uninstall(plugin)
