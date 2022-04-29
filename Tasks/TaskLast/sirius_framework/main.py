import os
import quopri
import json

from sirius_framework.requests import PostRequests, GetRequests
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

        request = {}
        method = environ['REQUEST_METHOD']
        request['method'] = method

        if method == 'POST':
            data = PostRequests().get_request_params(environ)
            request['data'] = data
            new_content = SiriusFramework.decode_post(data)
            print(f'Принят POST-запрос: {new_content}')
            # Принят POST - запрос: {'name': 'Сергей', 'phone': '89009990909', 'email': 'test@mail.ru',
            # 'location': 'nn', 'member': 'no', 'title_msg': 'Хочу квартиру', 'msg': 'Интересует хата на Ленина 52'}
            content = []
            try:
                with open(os.path.join(os.path.dirname(__file__), 'fixtures', 'db.json'), "r", encoding='UTF-8') as f:
                    content = json.load(f)
            except:
                pass
            with open(os.path.join(os.path.dirname(__file__), 'fixtures', 'db.json'), "w", encoding='UTF-8') as f:
                    content.append(new_content)
                    json.dump(content, f)

        if method == 'GET':
            # "GET /?id=1&object=5 HTTP/1.1" 200 12578
            request_params = GetRequests().get_request_params(environ)
            request['request_params'] = request_params
            print(f'Приняты параметры GET-запроса: {request_params}')
        print(request)
        # {'method': 'GET', 'request_params': {'id': '1', 'object': '5'}}

        # {'method': 'POST', 'data': {'name': '%D0%A1%D0%B5%D1%80%D0%B3%D0%B5%D0%B9', 'phone': '89009990909',
        # 'email': 'test%40mail.ru', 'location': 'nn', 'member': 'no',
        # 'title_msg': '%D0%A5%D0%BE%D1%87%D1%83+%D0%BA%D0%B2%D0%B0%D1%80%D1%82%D0%B8%D1%80%D1%83',
        # 'msg': '%D0%98%D0%BD%D1%82%D0%B5%D1%80%D0%B5%D1%81%D1%83%D0%B5%D1%82+%D1%85%D0%B0%D1%82%D0%B0+%D0%BD%D0%B0+%D0%9B%D0%B5%D0%BD%D0%B8%D0%BD%D0%B0+52'}}

        if path in self.routes_dct:
            view = self.routes_dct[path]
        else:
            view = PageNotFound404()

        for front in self.fronts_lst:
            front(request)
        # запуск контроллера с передачей объекта request
        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]

    @staticmethod
    def decode_post(old_data) -> dict:
        new_data = {}
        for key, value in old_data.items():
            b_val = bytes(value.replace('%', '=').replace("+", " "), 'UTF-8')
            val_decode_str = quopri.decodestring(b_val).decode('UTF-8')
            new_data[key] = val_decode_str
        return new_data
