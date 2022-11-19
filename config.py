from decouple import config

class ProdConf(object):
    DEBUG = False
    BABEL_DEFAULT_LOCALE ='pt_BR'
    SECRET_KEY = config('SECRET_KEY', default="você-nunca-vai-adivinhar")
    SQLALCHEMY_DATABASE_URI = config('DATABASE_URI', default='sqlite:///')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = config('MAIL_SERVER', default='localhost')
    MAIL_PORT = config('MAIL_PORT', cast=int, default='8025')
    MAIL_USE_TLS = config('MAIL_USE_TLS', cast=bool, default=False)
    MAIL_USERNAME = config('MAIL_USERNAME', default=None)
    MAIL_PASSWORD = config('MAIL_PASSWORD', default=None)
    MAIL_DEFAULT_SENDER = config(
        'MAIL_DEFAULT_SENDER', 
        default='contato@queirozt.webredirect.org'
    )
    ADMINS = config(
        'ADMINS', 
        cast=lambda v: [s.strip() for s in v.split(',')], 
        default="email@exemplo.com,"
    )


class TestConf(object):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SECRET_KEY = "você-nunca-vai-adivinhar"
    SQLALCHEMY_DATABASE_URI = "sqlite:///"
    SQLALCHEMY_TRACK_MODIFICATIONS = False