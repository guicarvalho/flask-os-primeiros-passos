from http import HTTPStatus

import marshmallow
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from .core.exceptions import InvalidUsage


db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
ma = Marshmallow()


def create_app(enviroment='Development'):
    app = Flask(__name__)
    app.config.from_object(f'coffee_shop.config.{enviroment}Config')

    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)

    from .auth.views import auth_bp
    from .product.views import product_bp
    from .sale.views import sale_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(sale_bp)

    @app.errorhandler(marshmallow.ValidationError)
    def handle_validation_error(error):
        return jsonify(error.messages), HTTPStatus.BAD_REQUEST

    @app.errorhandler(IntegrityError)
    @app.errorhandler(NoResultFound)
    def handle_no_result_found(error):
        return jsonify(message=error.args[0]), HTTPStatus.CONFLICT

    @app.errorhandler(InvalidUsage)
    def handle_invalid_usage_error(error):
        return jsonify(error.message), error.status_code

    return app
