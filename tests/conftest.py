from config import TestConf
from pytest import fixture

from app import create_app


@fixture(scope='function')
def conf_test():
    app = create_app(TestConf)
    
    app.test_request_context().push()
    app.db.create_all()

    yield app.test_client()

    app.db.drop_all()
