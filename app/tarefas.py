from flasgger import swag_from
from flask import (
    Blueprint, current_app, jsonify, render_template, request
)
from flask_login import current_user, login_required
from flask_marshmallow import exceptions

from app.authenticate import jwt_required
from app.flasgger import specs_create, specs_collect, specs_update, specs_delete
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
@swag_from(specs_create)
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
@swag_from(specs_collect)
def collect():
    ts = TarefaSchema(many=True)
    tarefas = current_user.tarefas.all()
    return ts.jsonify(tarefas), 200


@bp_tarefas.route('/update/<int:id>', methods=['PUT'])
@jwt_required
@swag_from(specs_update)
def update(id):
    ts = TarefaSchema()
    tarefa = current_user.tarefas.filter_by(id=id)
    try:
        if request.json.get('type'):
            if request.json.get('type') not in ['lista', 'fazer', 'feito']:
                raise exceptions.ValidationError({
                    'error': 'Type must be lista, fazer or feito'
                })
        if 'id' in request.json.keys() or 'user_id' in request.json.keys():
            raise exceptions.ValidationError({
                "error": "Dont send the ID field"
            })
        if not tarefa.first():
            raise exceptions.ValidationError({
                "error": {id: "Not Found"}
            })
        tarefa.update(request.json)
    except exceptions.ValidationError as e:
        return jsonify(e.messages_dict), 400
    except:
        return jsonify({'error': request.json}), 400
    else:
        current_app.db.session.commit()
        return ts.jsonify(tarefa.first()), 201


@bp_tarefas.route('/delete/<int:id>', methods=['DELETE'])
@jwt_required
@swag_from(specs_delete)
def delete(id):
    tarefa = current_user.tarefas.filter_by(id=id).delete()
    if tarefa:
        current_app.db.session.commit()
        return '', 204
    else:
        return jsonify({'error': {id: "Not Found"}}), 400
