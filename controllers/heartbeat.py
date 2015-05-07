from bottle import route
import datetime

# Having a ping is useful for New Relic and for benchmarking heavy loads,
# just the "byte serving" part (time to hit the stack and back)

@route('/ping')
def ping():
    return {"time": datetime.datetime.utcnow().isoformat()}

