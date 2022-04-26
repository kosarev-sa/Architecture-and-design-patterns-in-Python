from time import time


class AppRouteClassDec:
    def __init__(self, routes, url):
        self.routes = routes
        self.url = url

    def __call__(self, cls):
        '''Декоратор'''
        self.routes[self.url] = cls()


class DebugTimeDec:
    def __init__(self, cls_name):
        self.name = cls_name

    def __call__(self, cls):
        '''Декоратор'''
        def time_wrap(method):
            '''
            wrapper оборачивает каждый метод декорируемого класса
            '''
            def timed(*args, **kwargs):
                time_start = time()
                result = method(*args, **kwargs)
                time_end = time()
                delta = time_end - time_start
                print(f'DEBUG: Class_{self.name}, время выполняемого метода {delta:2.2f} ms')
                return result
            return timed
        return time_wrap(cls)
