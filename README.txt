Normal Py-files startup 

because with:
(from wsgiref.simple_server import make_server)
...with make_server('', 8080, application) as httpd:
        httpd.serve_forever()

