import copy
import quopri
import sqlite3

from patterns.architectural_system_pattern_unit_of_work import DomainObject
from patterns.behavioral_patterns import ConsolePrinter, Subject


# абстрактный пользователь
class User:
    def __init__(self, name):
        self.name = name


# продавец
class Saler(User):
    pass


# покупатель
class Buyer(User, DomainObject):
    def __init__(self, name):
        self.objects = []
        super().__init__(name)


# порождающий паттерн Абстрактная фабрика - фабрика пользователей
class UserFactory:
    types = {
        'saler': Saler,
        'buyer': Buyer
    }

    # порождающий паттерн Фабричный метод
    @classmethod
    def create(cls, type_, name):
        return cls.types[type_](name)


# порождающий паттерн Прототип - Объект
class ObjectPrototype:
    # прототип объектов недвижимости

    def clone(self):
        return copy.deepcopy(self)


class Object(ObjectPrototype, Subject):
    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.objects.append(self)
        self.buyers = []
        super().__init__()

    def __getitem__(self, item):
        return self.buyers[item]

    def add_buyer(self, buyer: Buyer):
        self.buyers.append(buyer)
        buyer.objects.append(self)
        self.note()


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
class Category(DomainObject):
    # реестр
    auto_id = 0

    def __init__(self, name, category):
        self.id = Category.auto_id
        Category.auto_id += 1
        self.name = name
        self.category = category
        self.objects = []

    def objects_count(self):
        if self.objects == None:
            self.objects = []
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

    @staticmethod
    def create_user(type_, name):
        return UserFactory.create(type_, name)

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

    def get_buyer(self, name) -> Buyer:
        for item in self.buyers:
            if item.name == name:
                return item

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
    '''Логгер с возможносттью применять стратегию (в случае добавления стратегии логирования)'''

    def __init__(self, name, writer=ConsolePrinter()):
        self.name = name
        self.writer = writer

    def log(self, text):
        text = f'log---> {text}'
        self.writer.write(text)


class BuyerMapper:

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = 'buyer'

    def all(self):
        statement = f'SELECT * from {self.tablename}'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id, name, objects = item
            buyer = Buyer(name)
            buyer.id = id
            buyer.objects = objects
            result.append(buyer)
        return result

    def find_by_id(self, id):
        statement = f"SELECT id, name FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            return Buyer(*result)
        else:
            raise RecordNotFoundException(f'record with id={id} not found')

    def insert(self, obj):
        statement = f"INSERT INTO {self.tablename} (name, objects) VALUES (?, ?)"
        self.cursor.execute(statement, (obj.name, None,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, obj):
        statement = f"UPDATE {self.tablename} SET objects=? WHERE name=?"
        self.cursor.execute(statement, (obj.objects[-1].name, obj.name))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, obj):
        statement = f"DELETE FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


class CategoryMapper:

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = 'category'

    def all(self):
        statement = f'SELECT * from {self.tablename}'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id, name, parent_category, objects = item
            category = Category(name, parent_category)
            category.id = id
            category.category = parent_category
            category.objects = objects
            result.append(category)
        return result

    def find_by_id(self, id):
        statement = f"SELECT name, category FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            return Category(*result)
        else:
            raise RecordNotFoundException(f'record with id={id} not found')

    def insert(self, obj):
        statement = f"INSERT INTO {self.tablename} (name, category, objects) VALUES (?, ?, ?)"
        self.cursor.execute(statement, (obj.name, obj.category, None,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, obj):
        statement = f"UPDATE {self.tablename} SET name=?, category=?, objects=? WHERE id=?"
        objects = ''
        for object in obj.objects:
            objects += f'{object.name} '
        self.cursor.execute(statement, (obj.name, obj.category, objects, obj.name))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, obj):
        statement = f"DELETE FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


connection = sqlite3.connect('patterns.sqlite')


# архитектурный системный паттерн - Data Mapper
class MapperRegistry:
    mappers = {
        'buyer': BuyerMapper,
        'category': CategoryMapper,
        #'object': ObjectMapper
    }

    @staticmethod
    def get_mapper(obj):
        if isinstance(obj, Buyer):
            return BuyerMapper(connection)
        if isinstance(obj, Category):
            return CategoryMapper(connection)
        # if isinstance(obj, Object):
            #return ObjectMapper(connection)

    @staticmethod
    def get_current_mapper(name):
        return MapperRegistry.mappers[name](connection)


class DbCommitException(Exception):
    def __init__(self, message):
        super().__init__(f'Db commit error: {message}')


class DbUpdateException(Exception):
    def __init__(self, message):
        super().__init__(f'Db update error: {message}')


class DbDeleteException(Exception):
    def __init__(self, message):
        super().__init__(f'Db delete error: {message}')

class RecordNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(f'Record not found: {message}')
