from http import HTTPStatus

from flask import abort, current_app, jsonify, request, Blueprint
from flask_jwt_extended import jwt_required
from werkzeug.exceptions import default_exceptions

from .auth import create_token, get_identity, requires_roles


root = Blueprint('root', __name__)


def error_handler(error):
    code = error.code
    description = error.description
    return jsonify(error=description, code=code)


for exc in default_exceptions:
    root.register_error_handler(exc, error_handler)


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        super(InvalidUsage, self).__init__()

        self.message = message

        if status_code is not None:
            self.status_code = status_code

        self.payload = payload

    def to_dict(self):
        resp = dict(self.payload or ())
        resp['message'] = self.message
        return resp


@root.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@root.route('/health')
def health():
    current_app.logger.info('blabla')
    return jsonify({'status': 'Ok'})


@root.route('/login', methods=['POST'])
def login():
    data = request.json

    if 'username' not in data or 'password' not in data:
        return jsonify({'msg': 'username and password are required!'})

    if data['username'] not in ['test', 'test1'] or data['password'] != 'test':
        return jsonify({'msg': 'Bad username or password!'})

    access_token = create_token(data['username'])
    return jsonify(access_token=access_token), HTTPStatus.OK


@root.route('/api/v1/coffees', methods=['POST'])
@jwt_required
@requires_roles('admin')
def create_coffee():
    print(request.json)
    print(get_identity())
    return jsonify({'msg': 'Coffee created with success!'})


@root.route('/error/<int:error>/')
def raise_error(error):
    abort(error)


@root.route('/error2/')
def raise_error2():
    raise InvalidUsage('Esse cliente já existe!', HTTPStatus.CONFLICT)
