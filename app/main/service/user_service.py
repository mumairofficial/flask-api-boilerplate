import uuid
from datetime import datetime

from app.main import db
from app.main.model.user import User


def save_new_user(data):
    user = User.query.filter_by(email=data['email'], username=data['username']).first()

    if not user:
        new_user = User(
            public_id=str(uuid.uuid4()),
            email=data['email'],
            username=data['username'],
            password=data['password'],
            registration_date=datetime.utcnow()
        )

        save_changes(new_user)
        # response_object = {
        #     'status': 'success',
        #     'message': 'Successfully registered'
        # }
        return generate_token(new_user), 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'User already exists. Please log in'
        }
        return response_object, 409


def generate_token(user):
    try:
        auth_token = user.encode_auth_token(user.public_id)
        response_object = {
            'status': 'success',
            'message': 'Successfully registered',
            'authorization': auth_token.decode()
        }
        return response_object, 201
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again'
        }
        return response_object, 401


def get_all_users():
    return User.query.all()


def get_a_user(public_id):
    return User.query.filter_by(public_id=public_id).first()


def save_changes(data):
    db.session.add(data)
    db.session.commit()
