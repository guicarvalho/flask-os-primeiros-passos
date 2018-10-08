from logging.config import dictConfig

from flask import Flask

from .auth import jwt
from .models import db, migrate


dictConfig({
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s: %(message)s'
        }
    },
    'handlers': {
        'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        }
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['wsgi']
    }
})


def create_app(enviroment='Development'):
    app = Flask(__name__)
    app.config.from_object(f'coffee_shop.config.{enviroment}Config')

    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    from .views import root
    app.register_blueprint(root)

    return app

