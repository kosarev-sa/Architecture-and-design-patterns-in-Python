from sirius_framework.templator import render


class PageNotFound404:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


class Index:
    def __call__(self, request):
        return '200 OK', render('index.html',
                                style=request.get('style1', None),
                                date=request.get('date', None),
                                time=request.get('time', None)
                                )


class Salers:
    def __call__(self, request):
        return '200 OK', render('salers.html',
                                style=request.get('style1', None),
                                date=request.get('date', None),
                                time=request.get('time', None)
                                )


class Realty:
    def __call__(self, request):
        return '200 OK', render('realty.html',
                                style=request.get('style1', None),
                                date=request.get('date', None),
                                time=request.get('time', None)
                                )
