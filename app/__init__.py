from flask import Flask
from flask_babel import Babel
from flask_migrate import Migrate
from logging.handlers import SMTPHandler
from pathlib import Path
from flasgger import Swagger, LazyJSONEncoder
import logging

from .auth import bp_auth
from .tarefas import bp_tarefas
from .errors import bp_errors
from .models import config as config_db
from .serializer import config as config_ma
from .flasgger import template, swagger_config


migrate = Migrate()
babel = Babel()

def create_app(Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    babel.init_app(app)

    config_db(app)
    config_ma(app)
    migrate.init_app(app, app.db)

    app.template_folder = Path.joinpath(Path.cwd(), 'resources', 'template')
    app.static_folder = Path.joinpath(Path.cwd(), 'resources', 'static')

    app.register_blueprint(bp_auth)
    app.register_blueprint(bp_tarefas)
    app.register_blueprint(bp_errors)

    app.json_encoder = LazyJSONEncoder
    Swagger(app, template=template, config=swagger_config)

    if not app.debug and not app.testing:
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr=app.config['MAIL_DEFAULT_SENDER'],
                toaddrs=app.config['ADMINS'], subject='Alerta de Erro!',
                credentials=auth, secure=secure
            )
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)
    
    return app
