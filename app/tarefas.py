from flask import Blueprint, render_template
from flask_login import current_user

bp_tarefas = Blueprint('tarefas', __name__)


@bp_tarefas.route('/')
@bp_tarefas.route('/index')
def index():
    return render_template('index.html', current_user=current_user)