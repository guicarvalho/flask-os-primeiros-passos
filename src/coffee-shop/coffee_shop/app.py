from datetime import datetime
from functools import wraps
from http import HTTPStatus

from flask import Flask, abort, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
from werkzeug.exceptions import HTTPException, default_exceptions


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://root:root@database:5432/coffee_shop'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['JWT_SECRET_KEY'] = 'my-secret-key'
app.config['JWT_HEADER_TYPE'] = 'JWT'
db = SQLAlchemy(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)


def error_handler(error):
    code = error.code
    description = error.description
    return jsonify(error=description, code=code)


for exc in default_exceptions:
    app.register_error_handler(exc, error_handler)


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


@app.errorhandler(Exception)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


def requires_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if not any([role in roles for role in get_current_user_role()]):
                return error_response()
            return f(*args, **kwargs)
        return wrapped
    return wrapper


def get_current_user_role():
    return ['admin'] if get_jwt_identity() == 'test' else ['visitant']


def error_response():
    return jsonify({'msg': "You've got no permission to access this resource."}), HTTPStatus.FORBIDDEN


class User(db.Model):

    __tablename__ = 'user'

    uuid = db.Column(UUID, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(20), nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'User (uuid: {self.uuid}, name: {self.name}, email: {self.email}, active: {self.active})'


class Product(db.Model):

    __tablename__ = 'product'

    uuid = db.Column(UUID, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    value = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'Product (uuid: {self.uuid}, name: {self.name}, stock: {self.stock}, value: {self.value})'


class Sale(db.Model):

    __tablename__ = 'sale'

    uuid = db.Column(UUID, primary_key=True)
    value = db.Column(db.Numeric(10, 2), nullable=False)
    user_uuid = db.Column(UUID, db.ForeignKey('user.uuid'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'Sale (uuid: {self.uuid}, value: {self.value}, user_uuid: {self.user_uuid})'


class ProductSale(db.Model):

    __tablename__ = 'product_sale'

    uuid = db.Column(UUID, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    value = db.Column(db.Numeric(10, 2), nullable=False)
    product_uuid = db.Column(UUID, db.ForeignKey('product.uuid'), nullable=False)
    sale_uuid = db.Column(UUID, db.ForeignKey('sale.uuid'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'uuid: {self.uuid}, quantity: {self.quantity}, value: {self.value}, product_uuid: {self.product_uuid}, ' \
                 'sale_uuid: {sale.uuid}'


@app.route('/health')
def health():
    return jsonify({'status': 'Ok'})


@app.route('/login', methods=['POST'])
def login():
    data = request.json

    if 'username' not in data or 'password' not in data:
        return jsonify({'msg': 'username and password are required!'})

    if data['username'] not in ['test', 'test1'] or data['password'] != 'test':
        return jsonify({'msg': 'Bad username or password!'})

    access_token = create_access_token(identity=data['username'])
    return jsonify(access_token=access_token), HTTPStatus.OK


@app.route('/api/v1/coffees', methods=['POST'])
@jwt_required
@requires_roles('admin')
def create_coffee():
    print(request.json)
    print(get_jwt_identity())
    return jsonify({'msg': 'Coffee created with success!'})


@app.route('/error/<int:error>')
def raise_error(error):
    abort(error)


@app.route('/error2/')
def raise_error2():
    raise InvalidUsage('Esse cliente já existe!', HTTPStatus.CONFLICT)

