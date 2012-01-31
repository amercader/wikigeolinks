"""The base Controller API

Provides the BaseController class for subclassing.
"""
from pylons.controllers import WSGIController
from pylons.templating import render_mako as render
from pylons import response

from wikigeolinks.model.meta import Session

class BaseController(WSGIController):

    def __call__(self, environ, start_response):
        """Invoke the Controller"""
        # WSGIController.__call__ dispatches to the Controller method
        # the request is routed to. This routing information is
        # available in environ['pylons.routes_dict']
        try:
            return WSGIController.__call__(self, environ, start_response)
        finally:
            Session.remove()

    def __after__(self, action, **params):

        # Set CORS headers
        response.headers['Access-Control-Allow-Origin'] = "*"
        response.headers['Access-Control-Allow-Methods'] = "POST, PUT, GET, DELETE"
        response.headers['Access-Control-Allow-Headers'] = "X-CKAN-API-KEY, Content-Type"
