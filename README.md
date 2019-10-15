# A Firestore ORM

Firestore ORM is a module that adds support for firestore
Object Relational Mapping to your application.
It requires firebase-admin 2.16.0 or higher.
It aims to simplify using Firestore collections as Objects by providing useful
defaults and extra helpers that make it easier to accomplish common tasks.

# Overview
Firestore ORM provides the following key features:

  - Object Models - create your models in the form of python Objects.
  - Queries - perform firestore queries easily.
  - Relationships - SQL foreign key concept to join documents.


## Usage

In the following paragraphs, I am going to describe how you can get and use Firestore ORM for your own projects.

###  Getting it

To download Firestore ORM, either fork this github repo or simply use Pypi via pip.
```sh
$ pip install firestore_orm
```

### Creating Models

Scrapeasy was programmed with ease-of-use in mind. First, import Website and Page from Scrapeasy

```Python
from jsonmodels import fields
from firestore_orm import model, relationship

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
        self.pet = relationship(self, Pet, 'pet_id')
```

### Operations

```Python

pet = Pet(name='Katty')
pet.id # >>> '26b353d6-f5a1-4a38-b61a-b9371de5b92f'

pet.save()  # save to firestore

person = Person(name='Chuck', pet_id=pet.id)
person.name # >>> 'Chuck'
person.surname # >>> None

person.populate(surname='Norris', age=20)
person.surname # >>> 'Norris'
person.name # >>> 'Chuck'
person.id # >>> '1286f8ae-710f-4fb7-a804-31fbed525390'

person.save()   # save to firestore

Person.query.fetch() 
# >>> [Person(created_at=datetime.datetime(2019, 3, 24, 13, 57, 21, 761746), name='Chuck', surname='Norris', age=20, pet_id='26b353d6-f5a1-4a38-b61a-b9371de5b92f', id='1286f8ae-710f-4fb7-a804-31fbed525390')]

Person.query.get('1286f8ae-710f-4fb7-a804-31fbed525390') 
# >>> Person(created_at=datetime.datetime(2019, 3, 24, 13, 57, 21, 761746), name='Chuck', surname='Norris', age=20, pet_id='26b353d6-f5a1-4a38-b61a-b9371de5b92f', id='1286f8ae-710f-4fb7-a804-31fbed525390')

person = Person.query.get('1286f8ae-710f-4fb7-a804-31fbed525390')
person.pet
# >>> 'Pet(created_at=datetime.datetime(2019, 3, 24, 13, 57, 21, 761746), name='Katty', id='26b353d6-f5a1-4a38-b61a-b9371de5b92f')'
```
# Filter
You can filter the results of a query using the following functions

```python

Person.query.fetch(filters=[('name', '==', 'Chuck'), ('age', '<=', 20)])
# >>> [Person(created_at=datetime.datetime(2019, 3, 24, 13, 57, 21, 761746), name='Chuck', surname='Norris', age=20, pet_id='26b353d6-f5a1-4a38-b61a-b9371de5b92f', id='1286f8ae-710f-4fb7-a804-31fbed525390')]
```
# Order by
You can also order the results of a query

```python
Person.query.fetch(order_by={"population": 'DESCENDING'})  # orders query by DESCENDING order: set to `ASCENDING` for ascending order
``` 

And you are ready to go!

Copyright (c) 2019 Benjamin Arko Afrasah

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.


