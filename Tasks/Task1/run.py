from sirius_framework.main import SiriusFramework
from urls import routes, fronts
from wsgiref.simple_server import make_server

app = SiriusFramework(routes, fronts)

with make_server('', 8080, app) as httpd:
    print("sirius_framework running... Port 8080")
    httpd.serve_forever()
