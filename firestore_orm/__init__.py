"""Firestore ORM is a module that adds support for firestore
Object Relational Mapping to your application.
It requires firebase-admin 2.16.0 or higher.
It aims to simplify using Firestore collections as Objects by providing useful
defaults and extra helpers that make it easier to accomplish common tasks.
"""
__author__ = 'Benjamin Arko Afrasah'
__version__ = '1.0.0'

from model import Model
from relationship import relationship
