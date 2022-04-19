import copy
import quopri


# абстрактный пользователь
class User:
    pass


# продавец
class Saler(User):
    pass


# покупатель
class Buyer(User):
    pass


# порождающий паттерн Абстрактная фабрика - фабрика пользователей
class UserFactory:
    types = {
        'sale': Saler,
        'buy': Buyer
    }

    # порождающий паттерн Фабричный метод
    @classmethod
    def create(cls, type_):
        return cls.types[type_]()


# порождающий паттерн Прототип - Объект
class ObjectPrototype:
    # прототип объектов недвижимости

    def clone(self):
        return copy.deepcopy(self)


class Object(ObjectPrototype):
    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.objects.append(self)


# Квартира
class Apartment(Object):
    pass


# Комната
class Room(Object):
    pass


# Дом
class House(Object):
    pass


# Категория заявки (продажа/покупка)
class Category:
    # реестр
    auto_id = 0

    def __init__(self, name, category):
        self.id = Category.auto_id
        Category.auto_id += 1
        self.name = name
        self.category = category
        self.subcategories = []
        if category:
            self.category.subcategories.append(self)
        self.objects = []

    def objects_count(self):
        result = len(self.objects)
        if self.category:
            result += self.category.objects_count()
        return result


# порождающий паттерн Абстрактная фабрика - фабрика объектов
class ObjectsFactory:
    types = {
        'Квартира': Apartment,
        'Комната': Room,
        'Дом': House
    }

    # порождающий паттерн Фабричный метод
    @classmethod
    def create(cls, type_, name, category):
        return cls.types[type_](name, category)


# Основной интерфейс проекта
class Engine:
    def __init__(self):
        self.salers = []
        self.buyers = []
        self.objects = []
        self.categories = []
        self.subcategories = []

    @staticmethod
    def create_user(type_):
        return UserFactory.create(type_)

    @staticmethod
    def create_category(name, category=None):
        return Category(name, category)

    def find_category_by_id(self, id):
        for item in self.categories:
            print('item', item.id)
            if item.id == id:
                return item
        raise Exception(f'Нет категории с id = {id}')

    @staticmethod
    def create_object(type_, name, category):
        return ObjectsFactory.create(type_, name, category)

    def get_object(self, name):
        for item in self.objects:
            if item.name == name:
                return item
        return None

    @staticmethod
    def decode_value(val):
        val_b = bytes(val.replace('%', '=').replace("+", " "), 'UTF-8')
        val_decode_str = quopri.decodestring(val_b)
        return val_decode_str.decode('UTF-8')


# порождающий паттерн Синглтон
class SingletonByName(type):

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class Logger(metaclass=SingletonByName):

    def __init__(self, name):
        self.name = name

    @staticmethod
    def log(text):
        print('log-->', text)
