from jsonmodels import fields
from jsonmodels.models import Base
import six
from app import init_firebase


init_firebase()


from firestorm import model, utils  # noqa


class Location(Base):
    longitude = fields.FloatField(required=True)
    latitude = fields.FloatField(required=True)
    name = fields.StringField(required=True)


class BaseModel(model.Model):
    is_deleted = fields.BoolField(default=False)


class ErrandCategory(BaseModel):
    """Errand category model class"""

    __tablename__ = 'test_errand_category'

    name = fields.StringField(required=True)


class Settings(BaseModel):
    """Settings model class"""

    __tablename__ = 'test_settings'

    user_id = fields.StringField(required=True)
    mode_of_transport = fields.ListField(
        items_types=six.string_types, nullable=True)
    preferred_errands = fields.ListField([ErrandCategory], nullable=True)
    payment_methods = fields.ListField(
        items_types=six.string_types, nullable=True)
    location = fields.EmbeddedField(Location, nullable=True)


class Users(BaseModel):
    """User's model class"""

    __tablename__ = 'test_users'

    first_name = fields.StringField(required=True)
    surname = fields.StringField(required=True)
    email = fields.StringField(required=True)
    password = fields.StringField(required=True)
    phone = fields.StringField(nullable=True)
    image_url = fields.StringField(nullable=True)
    settings_id = fields.StringField()
    location = fields.EmbeddedField(Location, nullable=True)

    def __init__(self, **kwargs):
        super(Users, self).__init__(**kwargs)
        self.settings = utils.relationship(
            self, Settings, 'settings_id')
