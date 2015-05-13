from bottle import default_app, app, run
import server_setup
import os

DEFAULT_PORT = "4444"
port = os.environ.get("PORT", DEFAULT_PORT)

# -------------------- SETUP / MAIN ------------------------

# This is needed for uwsgi or gunicorn. uwsgi will do introspection and will find my app
application = default_app()
app().catchall = False # dumps full stack trace
server_setup.setup_server(application)
run(application, host='0.0.0.0', port=port)