from flask import Flask
from pathlib import Path

from .auth import bp_auth
from .tarefas import bp_tarefas

BASE_DIR = Path(__file__).parent.parent


def create_app(Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    app.template_folder = Path.joinpath(BASE_DIR, 'resources', 'template')
    app.static_folder = Path.joinpath(BASE_DIR, 'resources', 'static')
    
    app.register_blueprint(bp_auth)
    app.register_blueprint(bp_tarefas)
    
    return app
