import jsonpickle
from sirius_framework.templator import render


# Поведенческий паттерн - наблюдатель
# Объект недвижимости
class Observer:
    def update(self, subject):
        pass


class Subject:
    def __init__(self):
        self.observers = []

    def note(self):
        for item in self.observers:
            item.update(self)


class NoteByEmail(Observer):
    def update(self, subject):
        print('EMAIL:', 'зарегистрирован потенциальный покупатель', subject.buyers[-1].name)


class NoteBySms(Observer):
    def update(self, subject):
        print('SMS:', 'зарегистрирован потенциальный покупатель', subject.buyers[-1].name)


class MainSerializer:
    def __init__(self, object):
        self.obj = object

    def save(self):
        return jsonpickle.dumps(self.obj)

    @staticmethod
    def load(data):
        return jsonpickle.loads(data)


# поведенческий паттерн - Шаблонный метод
class TemplateMeta:
    template_name = 'template.html',
    # название применяемого стиля (HTML-frontcontroller for using css as string)
    css = 'style'

    def get_context_data(self):
        return {}

    def get_template(self):
        return self.template_name

    def render_template_with_context(self, request):
        template_name = self.get_template()
        context_to_render = self.get_context_data()
        constant_context = {'style': request.get(self.css, None),
                            'date': request.get('date', None),
                            'time': request.get('time', None)}
        return '200 OK', render(template_name, **constant_context, **context_to_render)

    def __call__(self, request):
       return self.render_template_with_context(request)


class ListView(TemplateMeta):
    querylst = []
    template_name = 'list.html'
    context_object_name = 'objects_list'

    def get_querylst(self):
        print(self.querylst)
        return self.querylst

    def get_context_object_name(self):
        return self.context_object_name

    def get_context_data(self):
        querylst = self.get_querylst()
        context_object_name = self.get_context_object_name()
        context = {context_object_name: querylst}
        return context


class CreateView(TemplateMeta):
    template_name = 'create.html'

    @staticmethod
    def get_request_data(request):
        return request['data']

    def create_obj(self, data):
        pass

    def __call__(self, request):
        if request['method'] == 'POST':
            # метод пост
            data = self.get_request_data(request)
            self.create_obj(data)

            return self.render_template_with_context(request)
        else:
            return super().__call__(request)


# поведенческий паттерн - Стратегия
class ConsolePrinter:
    def write(self, text):
        print(text)


class FileWriter:
    def __init__(self, file_name):
        self.file = file_name

    def write(self, text):
        with open(self.file, 'a', encoding='utf-8') as f:
            f.write(f'{text}\n')
