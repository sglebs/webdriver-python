from model.web_driver import WebDriverEngine
from rest.web_driver import WebDriverController

# This is a non-OO controller. It has to be included so that Bottle will activate it
import rest.heartbeat

def setup_server (application):
    application.installed_plugins = []

    web_driver_engine = WebDriverEngine()
    web_driver_controller = WebDriverController(web_driver_engine)


def teardown_server (application):
    for plugin in application.installed_plugins:
       application.uninstall(plugin)
