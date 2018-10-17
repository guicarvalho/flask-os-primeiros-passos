class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'my-secrete-flask'
    JWT_HEADER_TYPE = 'JWT'


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://root:root@database:5432/coffee_shop'
    SQLALCHEMY_ECHO = True
    JWT_SECRET_KEY = 'my-secret-key'


class TestingConfig(DevelopmentConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
