from flask import (
    Blueprint, current_app, jsonify, render_template, request
)
from flask_login import current_user, login_required
from flask_marshmallow import exceptions

from app.authenticate import jwt_required
from app.serializer import TarefaSchema

bp_tarefas = Blueprint('tarefas', __name__)


@bp_tarefas.route('/')
@bp_tarefas.route('/index')
def index():
    return render_template('index.html')


@bp_tarefas.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', title='Minhas Tarefas')


@bp_tarefas.route('/create', methods=['POST'])
@jwt_required
def create():
    ts = TarefaSchema()
    request.json.update(user_id=current_user.id)
    try:
        tarefa = ts.load(request.json)
    except exceptions.ValidationError as e:
        return jsonify({'error': e.messages_dict}), 400
    else:
        current_app.db.session.add(tarefa)
        current_app.db.session.commit()
        return ts.jsonify(tarefa), 201


@bp_tarefas.route('/collect', methods=['GET'])
@jwt_required
def collect():
    ts = TarefaSchema(many=True)
    tarefas = current_user.tarefas.all()
    return ts.jsonify(tarefas), 200


@bp_tarefas.route('/update/<int:id>', methods=['PUT'])
@jwt_required
def update(id):
    ts = TarefaSchema()
    tarefa = current_user.tarefas.filter_by(id=id)
    try:
        if not tarefa.first():
            raise KeyError
        tarefa.update(request.json)
    except KeyError as e:
        return jsonify({'error': {'id': id}}), 400
    except:
        return jsonify({'error': request.json}), 400
    else:
        current_app.db.session.commit()
        return ts.jsonify(tarefa.first()), 201


@bp_tarefas.route('/delete/<int:id>', methods=['DELETE'])
@jwt_required
def delete(id):
    tarefa = current_user.tarefas.filter_by(id=id).delete()
    if tarefa:
        current_app.db.session.commit()
        return '', 204
    else:
        return jsonify({'error': {'id': id}}), 400
