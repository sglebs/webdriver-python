from model.web_driver import WebDriverEngine
import rest.web_driver

# This is a non-OO controller. It has to be included so that Bottle will activate it
import rest.heartbeat

def setup_server (application):
    application.installed_plugins = []
    rest.web_driver._web_driver_engine = WebDriverEngine() # inject the engine. on-OO / bottle


def teardown_server (application):
    for plugin in application.installed_plugins:
       application.uninstall(plugin)
