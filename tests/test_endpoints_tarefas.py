from flask import url_for
from flask_login import current_user, login_user, logout_user

from app.models import User, db


def test_rota_create_deve_retornar_302_quando_um_usuario_for_invalido(client):
    json = {
        'title': 'Teste de rota',
        'description': 'Testando a rota de criação',
        'type': 'list',
        'priority': True,
    }
    response = client.post(url_for('tarefas.create'), json=json)

    assert response.status_code == 302
    assert response.json == None


def test_rota_create_deve_retornar_201_quando_criar_um_recurso(client):
    u = User(username='teste', email='teste@email.com')
    db.session.add(u)
    db.session.commit()
    login_user(u)

    json = {
        'title': 'Teste de rota',
        'description': 'Testando a rota de criação',
        'type': 'list',
        'priority': True,
    }
    response = client.post(url_for('tarefas.create'), json=json)
    
    esperado = {'description': 'Testando a rota de criação', 'id': 1, 'priority': True, 'title': 'Teste de rota', 'type': 'list', 'user_id': 1}
    
    assert response.status_code == 201
    assert response.json == esperado


def test_rota_create_deve_retornar_400_quando_receber_um_json_incorreto(client):
    json = {
        'title': 'Teste de rota', 'type': 'list', 'priority': True,
    }

    response = client.post(url_for('tarefas.create'), json=json)

    esperado = {'error': {'description': ['Missing data for required field.']}}

    assert response.status_code == 400
    assert response.json == esperado


def test_rota_collect_deve_retornar_200_e_uma_lista_de_jsons(client):
    response = client.get(url_for('tarefas.collect'))

    esperado = [{'description': 'Testando a rota de criação', 'id': 1, 'priority': True, 'title': 'Teste de rota', 'type': 'list', 'user_id': 1}]

    assert response.status_code == 200
    assert response.json == esperado


def test_rota_update_deve_retornar_201_e_o_json_atualizado(client):
    response = client.put(
        url_for('tarefas.update', id=1), 
        json={'title': 'Novo Título'}
    )

    esperado = {'description': 'Testando a rota de criação','id': 1, 'priority': True, 'title': 'Novo Título', 'type': 'list', 'user_id': 1}

    assert response.status_code == 201
    assert response.json == esperado


def test_rota_update_deve_retornar_400_quando_receber_um_dado_invalido(client):
    response = client.put(
        url_for('tarefas.update', id=1), 
        json={'xpto': 'bla'}
    )

    esperado = {'error': {'xpto': 'bla'}}

    assert response.status_code == 400
    assert response.json == esperado


def test_rota_uptade_deve_retornar_400_quando_receber_um_id_invalido(client):
    response = client.put(
        url_for('tarefas.update', id=2), 
        json={'title': 'xpto'}
    )

    esperado = {'error': {'id': 2}}

    assert response.status_code == 400
    assert response.json == esperado


def test_rota_delete_deve_retornar_204_quando_deletar_um_recurso(client):
    response = client.delete(url_for('tarefas.delete', id=1))

    assert response.status_code == 204
    assert response.json == None


def test_rota_delete_deve_retornar_400_quando_não_encontrar_um_recurso(client):
    response = client.delete(url_for('tarefas.delete', id=0))

    esperado = {'error': {'id': 0}}

    assert response.status_code == 400
    assert response.json == esperado


def test_rota_delete_deve_retornar_204_e_remover_o_recurso_correto(client):
    json = {'title': 'Teste de rota', 'description': 'Testando a rota de criação', 'type': 'list', 'priority': True}

    client.post(url_for('tarefas.create'), json=json)
    client.post(url_for('tarefas.create'), json=json)
    tarefas_user1_antes = client.get(url_for('tarefas.collect'))
    
    logout_user()
    u = User(username='teste2', email='teste2@email.com')
    db.session.add(u)
    db.session.commit()
    login_user(u)

    client.post(url_for('tarefas.create'), json=json)
    client.post(url_for('tarefas.create'), json=json)

    tarefas_user2_antes = client.get(url_for('tarefas.collect'))

    response = client.delete(url_for('tarefas.delete', id=3))

    tarefas_user2_depois = client.get(url_for('tarefas.collect'))

    logout_user()
    login_user(User.query.filter_by(username='teste').first())
    tarefas_user1_depois = client.get(url_for('tarefas.collect'))

    assert response.status_code == 204
    assert response.json == None
    assert tarefas_user2_antes.json != tarefas_user2_depois.json
    assert tarefas_user1_antes.json == tarefas_user1_depois.json
