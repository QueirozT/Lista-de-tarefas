from flask import Flask
from flask_babel import Babel
from flask_migrate import Migrate
from pathlib import Path

from .auth import bp_auth
from .tarefas import bp_tarefas
from .errors import bp_errors
from .models import config as config_db
from .serializer import config as config_ma


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
    
    return app
