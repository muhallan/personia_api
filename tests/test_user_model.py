import unittest
import uuid
from helpers.validate import validate_uuid
from tests.base_test import BaseTestCase, db
from models.user import User


class TestUserModel(BaseTestCase):

    def test_encode_auth_token(self):
        user = User(
            user_id=uuid.uuid4().hex,
            username='test_user',
            password='test_password',
            name='test_name'
        )
        db.session.add(user)
        db.session.commit()
        auth_token = user.generate_token(user.user_id)
        self.assertTrue(isinstance(auth_token, bytes))

    def test_decode_auth_token(self):
        user = User(
            user_id=uuid.uuid4().hex,
            username='test_user',
            password='test_password',
            name='test_name'
        )
        db.session.add(user)
        db.session.commit()
        auth_token = user.generate_token(user.user_id)
        self.assertTrue(isinstance(auth_token, bytes))
        self.assertTrue(validate_uuid(User.decode_token(auth_token.decode("utf-8"))))

    def test_password_is_valid(self):
        user = User(
            user_id=uuid.uuid4().hex,
            username='test_user',
            password='test_password',
            name='test_name'
        )
        db.session.add(user)
        db.session.commit()
        self.assertTrue(user.is_password_valid("test_password"))


if __name__ == '__main__':
    unittest.main()
