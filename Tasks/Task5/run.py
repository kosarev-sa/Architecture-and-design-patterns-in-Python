from wsgiref.simple_server import make_server

from sirius_framework.main import SiriusFramework
from urls import fronts
from views import routes


# class SiriusFrameworkDebugVersion(SiriusFramework):
#     def __init__(self, routes, fronts):
#         super().__init__(routes, fronts)
#         self.app = SiriusFramework(routes, fronts)
#
#     def __call__(self, environ, start_response):
#         print('SiriusFramework - Debug Version: ', environ)
#         return self.app(environ, start_response)


class FakeApp:
    def __call__(self, environ, start_response):
        start_response('200 OK', [('Content-Type', 'text/html')])
        return [b'Hello from Fake!']


# app = SiriusFramework(routes, fronts)
# app = SiriusFrameworkDebugVersion(routes, fronts)
app = FakeApp()

HOST = '127.0.0.1'
PORT = 8080

with make_server('', 8080, app) as httpd:
    print("sirius_framework running...", f"http://{HOST}:{PORT}")
    httpd.serve_forever()
