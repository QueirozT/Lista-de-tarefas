from decouple import config

class ProdConf(object):
    DEBUG = False
    BABEL_DEFAULT_LOCALE ='pt_BR'
    SECRET_KEY = config('SECRET_KEY', default="você-nunca-vai-adivinhar")
    SQLALCHEMY_DATABASE_URI = config('DATABASE_URI', default='sqlite:///')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConf(object):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SECRET_KEY = "você-nunca-vai-adivinhar"
    SQLALCHEMY_DATABASE_URI = "sqlite:///"
    SQLALCHEMY_TRACK_MODIFICATIONS = False