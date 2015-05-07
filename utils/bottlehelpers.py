#from bottle import get, put, post, delete
from json import dumps

import bottle

__author__ = 'mqm'


def jsonabort(status, error=None, msg=None):
    error = error if error else {}
    error.update({'error': status})
    if msg:
        error.update({"message": msg})
    raise bottle.HTTPResponse(body=dumps(error), status=200,
        Content_Type="application/json; charset=UTF-8")


GET, POST, PUT, DELETE, ROUTE = range(5)

GET_STR, POST_STR, PUT_STR, DELETE_STR, ROUTE_STR = ('get', 'post', 'put', 'delete' ,'route')

METHOD_LIST = (GET_STR, POST_STR, PUT_STR, DELETE_STR, ROUTE_STR)

METHODS = {GET: GET_STR,
           POST: POST_STR,
           PUT: PUT_STR,
           DELETE: DELETE_STR,
           ROUTE: ROUTE_STR}

def makelist(data): # This is just to handy
    if isinstance(data, (tuple, list, set, dict)): return list(data)
    elif data: return [data]
    else: return []

def httpmethod(meth, route, **options):
    def decorator(f):
        #f.get = route (meth=GET)
        #f.post = route (meth=POST), etc
        setattr(f, METHODS[meth], route)
        if getattr (f, "options", None) is None:
            f.options = dict()
        for key , value in options.iteritems():
            values = f.options.get(key,None)
            values = makelist(values)
            values.append(value)
            f.options[key] = values
        return f

    return decorator


def methodget(route, **options):
    return httpmethod(GET, route, **options)


get = methodget


def methodpost(route, **options):
    return httpmethod(POST, route, **options)


post = methodpost


def methodput(route, **options):
    return httpmethod(PUT, route, **options)


put = methodput


def methoddelete(route, **options):
    return httpmethod(DELETE, route, **options)


delete = methoddelete


def methodroute(route, **options):
    return httpmethod(ROUTE, route, **options)


route = methodroute


http_attr = lambda x: [item for item in dir(x) if item in METHOD_LIST]


def is_attr_ok(attr):
    return attr and callable(attr)


def get_http_method(attr):
    cur_meth = http_attr(attr)
    cur_meth = cur_meth[0] if cur_meth else None
    return cur_meth


def decorate_method(decorated, cur_meth):
    bottle_meth = getattr(bottle, cur_meth)
    bottle_options = getattr(decorated, 'options')
    route = getattr(decorated, cur_meth)
    bottle_meth(route, **bottle_options)(decorated)


def get_object_methods(o):
    return [kw for kw in dir(o) if not kw.startswith('_')]


def add_routes(app_class):
    '''
    adds routes to a class
    by looking for METHOD_LIST attributes on methods
    (yes, python allows methods with attributes as first-class citizens)
    i.e. will search for get, put, post, delete attributes on each function
    this attribute holds the ROUTE (/api/doit/123)
    the function must have an OPTIONS attribute, as well (actually, a kwargs)
    '''
    for kw in get_object_methods(app_class):
        attr = getattr(app_class, kw)
        if is_attr_ok(attr):
            cur_meth = get_http_method(attr)
            if cur_meth:
                decorate_method(attr, cur_meth)


def clear_routes():
    while bottle.default_app:
        bottle.default_app.pop() #get rid of previous configs
    bottle.default_app.push()


#def get_params(request):
#    return loads([item for item in request.forms][0])

class Routeable(object):
    '''
    allows routes as method classes
    will "route" the methods just after object instantiation (__new__)
    '''

    def __new__(cls, *args, **kwargs):
        obj = object.__new__(cls, *args, **kwargs)
        add_routes(obj)
        return obj

