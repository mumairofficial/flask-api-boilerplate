import jwt
from datetime import datetime, timedelta

from .. import db, flask_bcrypt
from app.main.model.blacklist import BlacklistToken
from os import path

from Cryptodome.PublicKey import RSA

# from ..config import key
from app.main.config import basedir

JWT_ALGORITHM = "RS256"

key_path = path.join(basedir, 'rsa_private.pem')

key = open(key_path, "rb").read()
# key = RSA.import_key(encoded_key)

# key = "ALLAH"


class User(db.Model):
    """User Model for storing user related details"""
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True)
    password_hash = db.Column(db.String(100))
    admin = db.Column(db.Boolean, nullable=False, default=False)
    registration_date = db.Column(db.DateTime, nullable=False)

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = flask_bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return flask_bcrypt.check_password_hash(self.password_hash, password)

    @staticmethod
    def encode_auth_token(user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(days=1, seconds=5),
                'iat': datetime.utcnow(),
                'sub': user_id
            }

            return jwt.encode(
                payload,
                key,
                algorithm=JWT_ALGORITHM
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decode Auth Token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, key, algorithms=[JWT_ALGORITHM])
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)

            if is_blacklisted_token:
                return 'Token is expired. Please log in again.'

            return payload['sub']

        except jwt.ExpiredSignature:
            return 'Signature expired. Please log in again'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please login again'

    def __repr__(self):
        return "<User '{}'>".format(self.username)
