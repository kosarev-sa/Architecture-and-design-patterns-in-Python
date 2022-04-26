import quopri
from views import PageNotFound404


class SiriusFramework:
    """Класс SiriusFramework - основа фреймворка"""
    def __init__(self, routes, fronts):
        self.routes_dct = routes
        self.fronts_lst = fronts

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']
        if not path.endswith('/'):
            path = f'{path}/'
        if path in self.routes_dct:
            view = self.routes_dct[path]
        else:
            view = PageNotFound404()
        request = {}
        for front in self.fronts_lst:
            front(request)
        # запуск контроллера с передачей объекта request
        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]

    @staticmethod
    def decode_value(old_data):
        new_data = {}
        for key, value in old_data.items():
            b_val = bytes(value.replace('%', '=').replace("+", " "), 'UTF-8')
            val_decode_str = quopri.decodestring(b_val).decode('UTF-8')
            new_data[key] = val_decode_str
        return new_data
