from datetime import date, datetime
from views import Index, Realty, Salers, ObjManager, ObjectsList, CreateObject, CreateCategory, CategoryList, CopyObject


def style_front(request):
    """HTML-frontcontroller for using css as string"""
    with open('static/styles1.css') as f:
        css1 = f.read()
    with open('static/styles2.css') as f:
        css2 = f.read()
    request['style1'] = css1
    request['style2'] = css2


def secret_front(request):
    """Front controller"""
    request['date'] = date.today()
    request['time'] = datetime.today().strftime("%H:%M")


def other_front(request):
    """Front controller"""
    request['key'] = 'key'


fronts = [style_front, secret_front, other_front]
