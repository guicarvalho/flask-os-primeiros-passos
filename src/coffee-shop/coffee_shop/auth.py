from functools import wraps
from http import HTTPStatus

from flask import jsonify
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity


jwt = JWTManager()


def get_current_user_role():
    return ['admin'] if get_jwt_identity() == 'test' else ['visitant']


def error_response():
    return jsonify({'msg': "You've got no permission to access this resource."}), HTTPStatus.FORBIDDEN


def requires_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if not any([role in roles for role in get_current_user_role()]):
                return error_response()
            return f(*args, **kwargs)
        return wrapped
    return wrapper


def create_token(username):
    return create_access_token(identity=username)


def get_identity():
    return get_jwt_identity()

