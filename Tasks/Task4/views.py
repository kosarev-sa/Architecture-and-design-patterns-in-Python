from sirius_framework.templator import render
from patterns.сreational_patterns import Engine, Logger

site = Engine()
logger = Logger('main')


class PageNotFound404:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


class Index:
    def __call__(self, request):
        return '200 OK', render('index.html', style=request.get('style1', None),
                                date=request.get('date', None),
                                time=request.get('time', None),
                                )


class Salers:
    def __call__(self, request):
        return '200 OK', render('salers.html', style=request.get('style1', None),
                                date=request.get('date', None),
                                time=request.get('time', None),
                                )


class Realty:
    def __call__(self, request):
        return '200 OK', render('realty.html', style=request.get('style1', None),
                                date=request.get('date', None),
                                time=request.get('time', None),
                                )


# контроллер - менеджер объектов
class ObjManager:
    def __call__(self, request):
        return '200 OK', render('obj_manager.html', objects_list=site.categories,
                                style=request.get('style1', None),
                                date=request.get('date', None),
                                time=request.get('time', None),
                                )


# контроллер - список объектов
class ObjectsList:
    def __call__(self, request):
        logger.log('Список курсов')
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
class CreateObject:
    category_id = -1

    def __call__(self, request):
        if request['method'] == 'POST':
            # метод пост
            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            category = None
            if self.category_id != -1:
                category = site.find_category_by_id(int(self.category_id))

                object = site.create_object('Квартира', name, category)
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
class CreateCategory:
    def __call__(self, request):

        if request['method'] == 'POST':
            # метод пост
            print(request)
            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            category_id = data.get('category_id')

            category = None
            if category_id:
                category = site.find_category_by_id(int(category_id))

            new_category = site.create_category(name, category)

            site.categories.append(new_category)

            return '200 OK', render('obj_manager.html', style=request.get('style1', None),
                                    date=request.get('date', None),
                                    time=request.get('time', None),
                                    objects_list=site.categories,
                                    )
        else:
            categories = site.categories
            return '200 OK', render('create_category.html', style=request.get('style1', None),
                                    date=request.get('date', None),
                                    time=request.get('time', None),
                                    categories=categories,
                                    )


# контроллер - список категорий
class CategoryList:
    def __call__(self, request):
        logger.log('Список категорий')
        return '200 OK', render('category_list.html', style=request.get('style1', None),
                                date=request.get('date', None),
                                time=request.get('time', None),
                                objects_list=site.categories,
                                )


# контроллер - копировать объект
class CopyObject:
    def __call__(self, request):
        request_params = request['request_params']

        try:
            name = request_params['name']
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
