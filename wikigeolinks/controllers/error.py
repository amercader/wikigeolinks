from httplib import responses as error_names
import cgi
from pylons import response

from wikigeolinks.lib.base import BaseController


class ErrorController(BaseController):
    def document(self):
        """Render the error document"""
        request = self._py_object.request
        resp = request.environ.get('pylons.original_response')

        code=cgi.escape(request.GET.get('code', str(resp.status_int)))
        message = error_names.get(int(code),'')

        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return '{"error":"%s","code":%s}' % (message,code)

