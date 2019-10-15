from jsonmodels.fields import StringField

__author__ = 'Benjamin Arko Afrasah'

import uuid
from functools import partial

import firebase_admin
from firebase_admin import firestore
from firebase_admin import storage
from jsonmodels import fields
from jsonmodels.models import Base, JsonmodelMeta

from .base import FirestoreORM


class ModelMeta(JsonmodelMeta):

    def __new__(mcs, name, bases, local):
        new_class = type.__new__(mcs, name, bases, local)
        query = FirestoreORM(
            db=firestore.client(),
            bucket=storage.bucket(
                name=firebase_admin.get_app().options.get('storageBucket')),
        )
        partials = ['get', 'fetch']
        for attr in dir(query):
            if callable(getattr(query, attr)) and attr in partials:
                func = getattr(query, attr)
                func = partial(func, model=new_class)
                setattr(query, attr, func)

        new_class.query = query
        return new_class


class Model(Base):
    __metaclass__ = ModelMeta
    """Firestore Models all inherit from jsonmodels.models.Base.\n
    This is exposed as `from firestore_orm import model`.

    Arguments:
        Base {:class:`jsonmodels.models.Base`} -- To create models you need to create class that inherits from :class:`jsonmodels.models.Base`.\n
        For more details, refer to https://jsonmodels.readthedocs.io/en/latest/usage.html.\n
        __tablename__ {str} -- Collection name of model in firestore
    Keyword Arguments:
        metaclass {:class:`firestore_orm.models.ModelMeta`} --  (default: {ModelMeta})

    Example:

    .. code-block:: python

        from jsonmodels import fields
        from firestorm import model, utils

        class Pet(model.Model):
            __tablename__ = 'pet'

            name = fields.StringField(required=True)

        class Person(model.Model):
            __tablename__ = 'person'

            name = fields.StringField(required=True)
            surname = fields.StringField(nullable=False)
            age = fields.FloatField()
            pet_id = fields.StringField(required=True)

            def __init__(self, **kwargs):
                super(Person, self).__init__(**kwargs)
                self.pet = utils.relationship(self, Pet, 'pet_id')

    Usage:

    After that you can use it as normal object.\n
    You can pass kwargs in constructor or :meth:`jsonmodels.models.PreBase.populate` method.

    .. code-block:: python

        >>> pet = Pet(name='Katty')
        >>> pet.id
        '26b353d6-f5a1-4a38-b61a-b9371de5b92f'
        >>> pet.save()  # save to firestore
        >>> person = Person(name='Chuck', pet_id=pet.id)
        >>> person.name
        'Chuck'
        >>> person.surname
        None
        >>> person.populate(surname='Norris', age=20)
        >>> person.surname
        'Norris'
        >>> person.name
        'Chuck'
        >>> person.id
        '1286f8ae-710f-4fb7-a804-31fbed525390'
        >>> person.save()   # save to firestore
        >>> Person.query.fetch()
        [Person(created_at=datetime.datetime(2019, 3, 24, 13, 57, 21, 761746), name='Chuck', surname='Norris', age=20, pet_id='26b353d6-f5a1-4a38-b61a-b9371de5b92f', id='1286f8ae-710f-4fb7-a804-31fbed525390')]
        >>> Person.query.get('1286f8ae-710f-4fb7-a804-31fbed525390')
        Person(created_at=datetime.datetime(2019, 3, 24, 13, 57, 21, 761746), name='Chuck', surname='Norris', age=20, pet_id='26b353d6-f5a1-4a38-b61a-b9371de5b92f', id='1286f8ae-710f-4fb7-a804-31fbed525390')
        >>> person = Person.query.get('1286f8ae-710f-4fb7-a804-31fbed525390')
        >>> person.pet
        'Pet(created_at=datetime.datetime(2019, 3, 24, 13, 57, 21, 761746), name='Katty', id='26b353d6-f5a1-4a38-b61a-b9371de5b92f')'

    Filter
    --------

    You can filter the results of a query using the following functions

    .. code-block:: python

        >>> Person.query.fetch(filters=[('name', '==', 'Chuck'), ('age', '<=', 20)])
        [Person(created_at=datetime.datetime(2019, 3, 24, 13, 57, 21, 761746), name='Chuck', surname='Norris', age=20, pet_id='26b353d6-f5a1-4a38-b61a-b9371de5b92f', id='1286f8ae-710f-4fb7-a804-31fbed525390')]

    Order by
    ---------

    You can also order the results of a query
    .. code-block:: python

        >>> Person.query.fetch(order_by={"population": 'DESCENDING'})  # orders query by DESCENDING order: set to `ASCENDING` for ascending order
    """

    hidden_fields = ['password', 'is_deleted']
    show_relationships = []

    __tablename__ = None
    id = fields.StringField()  # type: StringField
    created_at = fields.DateTimeField()

    def __init__(self, *args, **kwargs):
        super(Model, self).__init__(*args, **kwargs)
        self.id = uuid.uuid4().__str__() if not self.id else self.id

    def save(self):
        # type: () -> bool
        """Save model instance to firestore
        """

        return self.query.commit(self.id, self)

    @classmethod
    def __call__(cls, *args, **kw):
        constructor = getattr(cls, "__new__")
        instance = constructor(
            cls) if constructor is object.__new__ else constructor(cls, *args, **kw)
        instance.__init__(cls, *args, **kw)
        return instance

    def to_dict(self, show=None, hide=None):
        # type: (list, list) -> dict
        """ Return a dictionary representation of this model.
        """
        if hide is None:
            hide = []
        if show is None:
            show = []
        hidden = []

        if hasattr(self, 'hidden_fields'):
            hidden = self.hidden_fields
            hidden.extend(hide)

        resp = {}
        for _, name, field in self.iterate_with_name():
            value = field.__get__(self)
            if name not in show and name in hidden:
                continue

            if value is None:
                resp[name] = None
                continue
            value = field.to_struct(value)
            resp[name] = value

        # jsonify relationships
        for key in self.show_relationships:
            val = getattr(self, key)  # type: Model
            if not val or not isinstance(val, Base):
                continue
            resp[key] = val.to_dict()
        return resp

    def delete(self):
        return self.query.delete(self)
