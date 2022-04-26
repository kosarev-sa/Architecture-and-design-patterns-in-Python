from sirius_framework.templator import render
from patterns.сreational_patterns import Engine, Logger
from patterns.structural_patterns import AppRouteClassDec, DebugTimeDec
from patterns.behavioral_patterns import NoteByEmail, NoteBySms, ListView, CreateView, MainSerializer

site = Engine()
logger = Logger('main')

email_note = NoteByEmail()
sms_note = NoteBySms()

routes = {}


class PageNotFound404:
    @DebugTimeDec(cls_name='PageNotFound404')
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


@AppRouteClassDec(routes=routes, url='/')
class Index:
    @DebugTimeDec(cls_name='Index')
    def __call__(self, request):
        return '200 OK', render('index.html', style=request.get('style1', None),
                                date=request.get('date', None),
                                time=request.get('time', None),
                                )


@AppRouteClassDec(routes=routes, url='/salers/')
class Salers:
    @DebugTimeDec(cls_name='Salers')
    def __call__(self, request):
        return '200 OK', render('salers.html', style=request.get('style1', None),
                                date=request.get('date', None),
                                time=request.get('time', None),
                                )


@AppRouteClassDec(routes=routes, url='/realty/')
class Realty:
    @DebugTimeDec(cls_name='Realty')
    def __call__(self, request):
        return '200 OK', render('realty.html', style=request.get('style1', None),
                                date=request.get('date', None),
                                time=request.get('time', None),
                                )


# контроллер - менеджер объектов
@AppRouteClassDec(routes=routes, url='/obj-manager/')
class ObjManager:
    @DebugTimeDec(cls_name='ObjManager')
    def __call__(self, request):
        return '200 OK', render('obj_manager.html', categories_list=site.categories,
                                style=request.get('style1', None),
                                date=request.get('date', None),
                                time=request.get('time', None),
                                )


# контроллер - список объектов
@AppRouteClassDec(routes=routes, url='/objects-list/')
class ObjectsList:
    @DebugTimeDec(cls_name='ObjectsList')
    def __call__(self, request):
        logger.log('Список объектов')
        try:
            category = site.find_category_by_id(int(request['request_params']['id']))
            return '200 OK', render('objects_list.html', style=request.get('style1', None),
                                    date=request.get('date', None),
                                    time=request.get('time', None),
                                    objects_list=category.objects,
                                    name=category.name,
                                    id=category.id,
                                    )
        except KeyError:
            return '200 OK', 'No objects have been added yet'


# контроллер - создать объект
@AppRouteClassDec(routes=routes, url='/create-object/')
class CreateObject:
    category_id = -1

    @DebugTimeDec(cls_name='CreateObject')
    def __call__(self, request):
        if request['method'] == 'POST':
            # метод пост
            print(request)
            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            category = None

            if self.category_id != -1:
                category = site.find_category_by_id(int(self.category_id))
                object = site.create_object('Квартира', name, category)

                # добавляем наблюдателей
                object.observers.append(email_note)
                object.observers.append(sms_note)

                site.objects.append(object)
            return '200 OK', render('objects_list.html', style=request.get('style1', None),
                                    date=request.get('date', None),
                                    time=request.get('time', None),
                                    objects_list=category.objects,
                                    name=category.name,
                                    id=category.id,
                                    )

        else:
            try:
                self.category_id = int(request['request_params']['id'])
                category = site.find_category_by_id(int(self.category_id))
                return '200 OK', render('create_object.html', style=request.get('style1', None),
                                        date=request.get('date', None),
                                        time=request.get('time', None),
                                        name=category.name,
                                        id=category.id,
                                        )
            except KeyError:
                return '200 OK', 'No categories have been added yet'


# контроллер - создать категорию
@AppRouteClassDec(routes=routes, url='/create-category/')
class CreateCategory:
    category_id = None
    @DebugTimeDec(cls_name='CreateCategory')
    def __call__(self, request):
        if 'request_params' in request and 'id' in request['request_params']:
           self.category_id = int(request['request_params']['id'])
        if request['method'] == 'POST':
            # метод пост
            print(request)
            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            # category_id = data.get('category_id')
            category = None
            if self.category_id:
                category = site.find_category_by_id(int(self.category_id))
            print("***", category)
            new_category = site.create_category(name, category)

            site.categories.append(new_category)

            return '200 OK', render('obj_manager.html', style=request.get('style1', None),
                                    date=request.get('date', None),
                                    time=request.get('time', None),
                                    categories_list=site.categories,
                                    )
        else:
            categories = site.categories
            return '200 OK', render('create_category.html', style=request.get('style1', None),
                                    date=request.get('date', None),
                                    time=request.get('time', None),
                                    categories=categories,
                                    )


# контроллер - список категорий
@AppRouteClassDec(routes=routes, url='/category-list/')
class CategoryList:
    @DebugTimeDec(cls_name='CategoryList')
    def __call__(self, request):
        logger.log('Список категорий')
        category = site.find_category_by_id(int(request['request_params']['id']))
        return '200 OK', render('category_list.html', style=request.get('style1', None),
                                date=request.get('date', None),
                                time=request.get('time', None),
                                categories_list=site.categories,
                                id=category.id
                                )


# контроллер - копировать объект
@AppRouteClassDec(routes=routes, url='/copy-object/')
class CopyObject:
    @DebugTimeDec(cls_name='CopyObject')
    def __call__(self, request):
        request_params = request['request_params']
        try:

            name = request_params['name']
            name = site.decode_value(name)

            old_object = site.get_object(name)
            if old_object:
                new_name = f'copy_{name}'
                new_object = old_object.clone()
                new_object.name = new_name
                site.objects.append(new_object)
            return '200 OK', render('objects_list.html', style=request.get('style1', None),
                                    date=request.get('date', None),
                                    time=request.get('time', None),
                                    objects_list=site.objects,
                                    )
        except KeyError:
            return '200 OK', 'No objects have been added yet'


@AppRouteClassDec(routes=routes, url='/buyer-list/')
class BuyerListView(ListView):
    querylst = site.buyers
    template_name = 'buyer_list.html'
    css = 'style1'


@AppRouteClassDec(routes=routes, url='/create-buyer/')
class BuyerCreateView(CreateView):
    template_name = 'create_buyer.html'
    css = 'style1'

    def create_obj(self, data: dict):
        name = data['name']
        name = site.decode_value(name)
        new_buyer = site.create_user('buyer', name)
        site.buyers.append(new_buyer)


@AppRouteClassDec(routes=routes, url='/add-buyer/')
class AddBuyerByObjectCreateView(CreateView):
    template_name = 'add_buyer.html'
    css = 'style1'

    def get_context_data(self):
        context = super().get_context_data()
        context['objects'] = site.objects
        context['buyers'] = site.buyers
        return context

    def create_obj(self, data: dict):
        object_name = data['object_name']
        object_name = site.decode_value(object_name)
        object = site.get_object(object_name)
        buyer_name = data['buyer_name']
        buyer_name = site.decode_value(buyer_name)
        buyer = site.get_buyer(buyer_name)
        object.add_buyer(buyer)


@AppRouteClassDec(routes=routes, url='/api/')
class ObjectApi:
    @DebugTimeDec(cls_name='ObjectApi')
    def __call__(self, request):
        return '200 OK',   MainSerializer(site.objects).save()
