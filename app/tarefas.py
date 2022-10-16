from flask import Blueprint, render_template

bp_tarefas = Blueprint('tarefas', __name__)


@bp_tarefas.route('/')
@bp_tarefas.route('/index')
def index():
    return render_template('index.html')