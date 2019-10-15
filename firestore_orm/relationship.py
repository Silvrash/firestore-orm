__author__ = 'Benjamin Arko Afrasah'

import firebase_admin
from firebase_admin import firestore
from firebase_admin import storage

from firestore_orm.base import FirestoreORM
from firestore_orm.model import Model


def relationship(model, foreign_model, key, uselist=False):
    # type: (Model, Model, str, bool) -> Model
    """Used to define a relationship between a models

    Arguments:
        model {Model} -- current model
        foreign_model{Model} -- related model
        key {str} -- foreign key binding current model to the foreign model
        uselist {bool} -- set to false for a single related item, true for multiple

    Returns:
        [Model] -- related model
    """
    id = model.to_struct().get(key)
    query = FirestoreORM(
        db=firestore.client(),
        bucket=storage.bucket(name=firebase_admin.get_app().options.get('storageBucket')),
    )
    return query.get(id=id, model=foreign_model) if not uselist else query.fetch(foreign_model,
                                                                                 filters=[('id', '==', id)])
