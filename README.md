# Firestorm - A Firestore ORMA

Firestorm is a module that adds support for firestore
Object Relational Mapping to your application.
It requires firebase-admin 2.16.0 or higher.
It aims to simplify using Firestore collections as Objects by providing useful
defaults and extra helpers that make it easier to accomplish common tasks.

# Overview
Firestorm provides the following key features:

  - Object Models - create your models in the form of python Objects.
  - Queries - perform firestore queries easily.
  - Relationships - SQL foreign key concept to join documents.


## Usage

In the following paragraphs, I am going to describe how you can get and use Firestorm for your own projects.

###  Getting it

To download firestorm, either fork this github repo or simply use Pypi via pip.
```sh
$ pip install firestorm
```

### Using it

Scrapeasy was programmed with ease-of-use in mind. First, import Website and Page from Scrapeasy

```Python
from jsonmodels import fields
from firestorm import model, relationship

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

And you are ready to go!

MIT License

Copyright (c) 2019 Benjamin Arko Afrasah

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
