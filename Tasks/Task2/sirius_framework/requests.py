class GetRequests:
    """Class for params parsing of GET requests"""
    @staticmethod
    def get_dct(data: str) -> dict:
        result = {}
        if data:
            pairs = data.split('&')
            for pair in pairs:
                key, val = pair.split('=')
                result[key] = val
        return result

    @staticmethod
    def get_request_params(environ):
        # получаем параметры запроса, затем превращаем параметры в словарь
        query_string = environ['QUERY_STRING']
        request_params = GetRequests.get_dct(query_string)
        return request_params


class PostRequests:
    """Class for params parsing of POST requests"""
    @staticmethod
    def get_dct(data: str) -> dict:
        result = {}
        if data:
            pairs = data.split('&')
            for pair in pairs:
                key, val = pair.split('=')
                result[key] = val
        return result

    @staticmethod
    def get_wsgi_input_data(environ) -> bytes:
        str_content_length = environ.get('CONTENT_LENGTH')
        int_content_length = int(str_content_length) if str_content_length else 0
        print(int_content_length) # 329
        # Считываем данные, если они есть
        # print(f"{type(env['wsgi.input'])}") -> <class '_io.BufferedReader'>
        inputed_data = environ['wsgi.input'].read(int_content_length) if int_content_length > 0 else b''
        return inputed_data

    def parse_b_input_data(self, data: bytes) -> dict:
        result = {}
        if data:
            data_str = data.decode(encoding='utf-8')
            print(f'Декодированная строка: {data_str}')
            # Декодированная строка: name = % D0 % A1 % D0 % B5 % D1 % 80 % D0 % B3 % D0 % B5 % D0 % B9 & phone = 890099
            # 90909 & email = test % 40 mail.ru & location = nn & member = no & title_msg = % D0 % A5 % D0 % BE % D1 % 8
            # 7 % D1 % 83 + % D0 % BA % D0 % B2 % D0 % B0 % D1 % 80 % D1 % 82 % D0 % B8 % D1 % 80 % D1 % 83 & msg = % D0
            # % 98 % D0 % BD % D1 % 82 % D0 % B5 % D1 % 80 % D0 % B5 % D1 % 81 % D1 % 83 % D0 % B5 % D1 % 82 + % D1 % 85
            # % D0 % B0 % D1 % 82 % D0 % B0 + % D0 % BD % D0 % B0 + % D0 % 9 B % D0 % B5 % D0 % BD % D0 % B8 % D0 % BD %
            # D0 % B0 + 52
            result = self.get_dct(data_str)
        return result

    def get_request_params(self, environ):
        data = self.get_wsgi_input_data(environ)
        data = self.parse_b_input_data(data)
        return data

# 'method': 'POST', 'data':
# {'name': '%D0%A1%D0%B5%D1%80%D0%B3%D0%B5%D0%B9', 'phone': '89009990909', 'email': 'test%40mail.ru', 'location': 'nn',
# 'member': 'no', 'title_msg': '%D0%A5%D0%BE%D1%87%D1%83+%D0%BA%D0%B2%D0%B0%D1%80%D1%82%D0%B8%D1%80%D1%83',
# 'msg': '%D0%98%D0%BD%D1%82%D0%B5%D1%80%D0%B5%D1%81%D1%83%D0%B5%D1%82+%D1%85%D0%B0%D1%82%D0%B0+%D0%BD%D0%B0+%D0%9B%D0%B5%D0%BD%D0%B8%D0%BD%D0%B0+52'}
