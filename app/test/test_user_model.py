import unittest
from datetime import datetime

from app.main import db
from app.main.model.user import User
from app.test.base import BaseTestCase


class TestUserModel(BaseTestCase):

    def test_encode_auth_token(self):
        user = User(
            email='test@test.com',
            password='HelloWorld',
            registration_date=datetime.utcnow()
        )

        db.session.add(user)
        db.session.commit()
        auth_token = user.encode_auth_token(user.public_id)
        self.assertTrue(isinstance(auth_token, bytes))

    def test_decode_auth_token(self):
        user = User(
            email='test@test.com',
            password="HelloWorld",
            registration_date=datetime.utcnow()
        )

        db.session.add(user)
        db.session.commit()
        auth_token = user.encode_auth_token(user.public_id)

        self.assertTrue(isinstance(auth_token, bytes))
        self.assertTrue(User.decode_auth_token(auth_token.decode('utf-8')) == user.public_id)


if __name__ == '__main__':
    unittest.main()
