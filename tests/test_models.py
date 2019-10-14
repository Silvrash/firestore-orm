import pytest
import atexit
from . import Users, Settings
# import json

user_fields = {
    'first_name': 'Testy',
    'surname': 'Testa',
    'email': 'barkoafrasah@gmail.com',
    'password': 'jackass',
}


def pytest_namespace():
    return {'id': None}


class TestFireStoreOrm(object):

    def test_add_user_model(self):

        new_user: Users = Users(**user_fields)
        settings = self.add_settings({'user_id': new_user.id})
        new_user.settings_id = settings.id
        new_user.save()
        assert isinstance(new_user.id, str)
        pytest.id = new_user.id
        # self.report(
        #     'test_add_user_model', json.dumps(new_user.to_struct(), indent=1))

    def add_settings(self, kwargs):
        settings = Settings(**kwargs)
        settings.save()
        return settings

    def test_get_single_user(self):
        user = Users.query.get(pytest.id)

        assert isinstance(user, Users)
        # self.report(
        #     'test_get_single_user', json.dumps(user.to_struct(), indent=1))

    def test_fetch_user(self):
        user = Users.query.fetch(
            filters=[('is_deleted', '==', False), ('id', '==', pytest.id)], single=True)
        assert isinstance(user, Users)
        assert not user.is_deleted
        # self.report('test_fetch_user', json.dumps(user.to_struct(), indent=1))

    def test_get_multiple_users(self):
        users = Users.query.fetch(to_dict=True)

        assert isinstance(users, list)

        # self.report(
        #     'test_get_multiple_users', json.dumps(users, indent=1))

    def test_update_user(self):
        fields = {
            'first_name': 'Testaff',
            'surname': 'Testa_zzz',
        }
        user: Users = Users.query.get(pytest.id)
        user.populate(**fields)
        user.save()
        assert user.first_name != user_fields['first_name']
        assert user.surname != user_fields['surname']

        # self.report(
        #     'test_update_user', json.dumps(user.to_struct(), indent=1))

    def test_delete_user(self):
        user = Users.query.get(pytest.id)
        user.is_deleted = True
        user.save()
        assert user.is_deleted

    def test_query_filters(self):
        users = Users.query.fetch(
            filters=[('email', '==', user_fields['email'])], to_dict=True)

        assert isinstance(users, list)

        # self.report('test_query_filters', json.dumps(users, indent=1))

    def test_query_filter_single(self):
        user = Users.query.fetch(
            filters=[('email', '==', user_fields['email'])], single=True)

        assert isinstance(user, Users)
        assert user.email

        # self.report('test_query_filter_single',
        #             json.dumps(user.to_struct(), indent=1))

    def test_relationship(self):
        user = Users.query.get(pytest.id)

        assert isinstance(user, Users)
        assert isinstance(user.settings, Settings)

        # self.report('test_relationship', json.dumps(
        #     user.settings.to_struct(), indent=1))

    def test_users_add_embedded_field(self):
        pass

    def report(self, func, *args):
        atexit.register(lambda: print('Output - ', func + ':--> ', *args))
