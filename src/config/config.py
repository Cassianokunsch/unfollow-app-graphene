import os


class BaseConfig(object):
    DEBUG = False
    PORT = os.environ.get('PORT', "5000")


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    HOST = 'localhost'
    ENV = "development"


class ProductionConfig(BaseConfig):
    HOST = '0.0.0.0'
