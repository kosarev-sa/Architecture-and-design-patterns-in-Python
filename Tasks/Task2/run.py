from sirius_framework.main import SiriusFramework
from urls import routes, fronts
from wsgiref.simple_server import make_server

app = SiriusFramework(routes, fronts)

HOST = '127.0.0.1'
PORT = 8080

with make_server('', 8080, app) as httpd:
    print("sirius_framework running...", f"http://{HOST}:{PORT}")
    httpd.serve_forever()
