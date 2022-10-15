from decouple import config

class ProdConf(object):
    DEBUG = False
    SECRET_KEY = config('SECRET_KEY', default="você-nunca-vai-adivinhar")


class TestConf(object):
    TESTING = True
    SECRET_KEY = "você-nunca-vai-adivinhar"
