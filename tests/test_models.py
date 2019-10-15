# Copyright 2019 Benjamin Arko Afrasah
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest

from testdata.models import Users


class TestModel(unittest.TestCase):

    def test_cud(self):
        user = self.create()
        self.update(user)
        self.delete(user.id)

    @staticmethod
    def create():
        # Mock the API response
        # channel = ChannelStub(responses=[expected_response])
        # patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        # with patch as create_channel:
        #     create_channel.return_value = channel
        #     client = firestore_client.FirestoreClient()
        user = Users(first_name='Chuck', surname='Norris')
        assert user.save(), 'Could not save user'
        return user

    @staticmethod
    def update(user):
        # type: (Users) -> Users

        new_first_name = 'Chukky'
        user.populate(first_name=new_first_name)

        assert user.first_name == new_first_name, 'Failed to update property'
        assert user.save(), 'Failed to update model'

        user = Users.query.get(user.id)
        assert user.first_name == new_first_name, 'Property does not match updated value'
        return user

    @staticmethod
    def delete(user_id):
        # type: (str) -> None

        user = Users.query.get(user_id)
        assert user.delete(), 'Failed to delete'
