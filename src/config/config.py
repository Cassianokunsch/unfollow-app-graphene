import os


class BaseConfig(object):
    DEBUG = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    HOST = 'localhost'
    ENV = "development"


class ProductionConfig(BaseConfig):
    HOST = '0.0.0.0'
