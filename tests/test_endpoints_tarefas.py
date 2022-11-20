from flask import url_for
from flask_login import current_user, login_user, logout_user

from app.models import User, db


def test_rota_create_deve_retornar_403_quando_um_usuario_for_invalido(client):
    json = {
        'title': 'Teste de rota',
        'description': 'Testando a rota de criação',
        'type': 'lista',
        'priority': True,
    }

    response = client.post(url_for('tarefas.create'), json=json)
    
    esperado = {'error': 'Access Denied'}

    assert response.status_code == 403
    assert response.json == esperado


def test_rota_create_deve_retornar_201_quando_criar_um_recurso(client):
    u = User(username='teste', email='teste@email.com')
    db.session.add(u)
    db.session.commit()
    login_user(u)

    json = {
        'title': 'Teste de rota',
        'description': 'Testando a rota de criação',
        'type': 'lista',
        'priority': True,
    }
    response = client.post(url_for('tarefas.create'), json=json)
    
    esperado = {'description': 'Testando a rota de criação', 'id': 1, 'priority': True, 'title': 'Teste de rota', 'type': 'lista'}
    
    assert response.status_code == 201
    assert response.json == esperado


def test_rota_create_deve_retornar_400_quando_faltar_o_type_(client):
    json = {
        'title': 'Teste de rota',
        'description': 'Testando a rota de criação',
        'priority': False
    }
    response = client.post(url_for('tarefas.create'), json=json)
    
    esperado = {
        "error": {
            "type": ["Missing data for required field."]
        }
    }
    
    assert response.status_code == 400
    assert response.json == esperado


def test_rota_create_deve_retornar_400_quando_receber_um_json_incorreto(client):
    json = {
        'title': 'Teste de rota', 'type': 'lista', 'priority': True,
    }

    response = client.post(url_for('tarefas.create'), json=json)

    esperado = {'error': {'description': ['Missing data for required field.']}}

    assert response.status_code == 400
    assert response.json == esperado


def test_rota_create_deve_retornar_400_quando_receber_um_titulo_vazio(client):
    json = {
        'title': '', 'description': 'teste', 'type': 'lista', 'priority': True
    }

    response = client.post(url_for('tarefas.create'), json=json)

    esperado = {'error': {'title': ['Title is required.']}}

    assert response.status_code == 400
    assert response.json == esperado


def test_rota_create_deve_retornar_400_quando_receber_uma_descricao_vazia(client):
    json = {
        'title': 'teste', 'description': '', 'type': 'lista', 'priority': True
    }

    response = client.post(url_for('tarefas.create'), json=json)

    esperado = {'error': {'description': ['Description is required.']}}

    assert response.status_code == 400
    assert response.json == esperado


def test_rota_create_deve_retornar_400_quando_receber_um_type_vazio(client):
    json = {
        'title': 'xpto', 'description': 'todo', 'type': '', 'priority': True
    }

    response = client.post(url_for('tarefas.create'), json=json)

    esperado = {'error': {'type': ['Type is required.']}}

    assert response.status_code == 400
    assert response.json == esperado


def test_rota_create_deve_retornar_400_quando_receber_um_type_inesperado(client):
    json = {
        'title': 'xpto', 'description': 'todo', 'type': 'teste', 'priority': True
    }

    response = client.post(url_for('tarefas.create'), json=json)

    esperado = {'error': {'type': ['Type must be lista, fazer or feito.']}}

    assert response.status_code == 400
    assert response.json == esperado


def test_rota_collect_deve_retornar_200_e_uma_lista_de_jsons(client):
    response = client.get(url_for('tarefas.collect'))

    esperado = [{'description': 'Testando a rota de criação', 'id': 1, 'priority': True, 'title': 'Teste de rota', 'type': 'lista'}]

    assert response.status_code == 200
    assert response.json == esperado


def test_rota_update_deve_retornar_201_e_o_json_atualizado(client):
    response = client.put(
        url_for('tarefas.update', id=1), 
        json={'title': 'Novo Título'}
    )

    esperado = {'description': 'Testando a rota de criação','id': 1, 'priority': True, 'title': 'Novo Título', 'type': 'lista'}
    
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

    esperado = {'error': {'2': 'Not Found'}}

    assert response.status_code == 400
    assert response.json == esperado


def test_rota_uptade_deve_retornar_400_quando_receber_um_id_no_json(client):
    response = client.put(
        url_for('tarefas.update', id=2), 
        json={'id': 10}
    )

    esperado = {'error': "Dont send the ID field"}

    assert response.status_code == 400
    assert response.json == esperado


def test_rota_uptade_deve_retornar_400_quando_receber_um_type_errado(client):
    response = client.put(
        url_for('tarefas.update', id=2), 
        json={'type': 'xpto'}
    )

    esperado = {'error': "Type must be lista, fazer or feito"}

    assert response.status_code == 400
    assert response.json == esperado


def test_rota_delete_deve_retornar_204_quando_deletar_um_recurso(client):
    response = client.delete(url_for('tarefas.delete', id=1))

    assert response.status_code == 204
    assert response.json == None


def test_rota_delete_deve_retornar_400_quando_não_encontrar_um_recurso(client):
    response = client.delete(url_for('tarefas.delete', id=0))

    esperado = {'error': {'0': 'Not Found'}}
    
    assert response.status_code == 400
    assert response.json == esperado


def test_rota_delete_deve_retornar_204_e_remover_o_recurso_correto(client):
    json = {'title': 'Teste de rota', 'description': 'Testando a rota de criação', 'type': 'lista', 'priority': True}

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


def test_rota_create_deve_retornar_201_caso_o_token_seja_valido(client):
    logout_user()
    token = User.query.filter_by(username='teste').first().get_jwt_token()
    
    json = {
        'title': 'Teste', 
        'description': 'Testando a rota de criação', 
        'type': 'lista', 
        'priority': True
    }
    
    response = client.post(url_for('tarefas.create'), json=json, headers={'Authorization': f'Bearer {token}'})

    esperado = {'description': 'Testando a rota de criação','id': 5, 'priority': True, 'title': 'Teste', 'type': 'lista'}

    assert response.status_code == 201
    assert response.json == esperado


def test_rota_create_deve_retornar_403_caso_o_token_seja_invalido(client):
    logout_user()
    token = 'token inválido'
    
    json = {
        'title': 'Teste', 
        'description': 'Testando a rota de criação', 
        'type': 'lista', 
        'priority': True
    }

    response = client.post(url_for('tarefas.create'), json=json, headers={'Authorization': f'Bearer {token}'})
    response2 = client.post(url_for('tarefas.create'), json=json, headers={'Authorization': token})

    esperado = {'error': 'Invalid Token'}

    assert response.status_code == 403
    assert response.json == esperado

    assert response2.status_code == 401
    assert response2.json == esperado


def test_collect_deve_retornar_200_caso_o_token_seja_valido(client):
    logout_user()
    token = User.query.filter_by(username='teste').first().get_jwt_token()
    
    response = client.get(url_for('tarefas.collect'), headers={'Authorization': f'Bearer {token}'})

    esperado = [
        {'description': 'Testando a rota de criação', 'id': 1, 'priority': True, 'title': 'Teste de rota', 'type': 'lista'},
        {'description': 'Testando a rota de criação', 'id': 2, 'priority': True, 'title': 'Teste de rota', 'type': 'lista'},
        {'description': 'Testando a rota de criação', 'id': 5, 'priority': True, 'title': 'Teste', 'type': 'lista'}
    ]

    assert response.status_code == 200
    assert response.json == esperado


def test_collect_deve_retornar_401_e_um_erro_caso_o_token_seja_invalido(client):
    logout_user()
    token = User.query.filter_by(username='teste').first().get_jwt_token()
    
    response = client.get(url_for('tarefas.collect'), headers={'Authorization': token})

    esperado = {'error': 'Invalid Token'}

    assert response.status_code == 401
    assert response.json == esperado


def test_update_deve_retornar_201_quando_o_token_e_os_dados_forem_validos(client):
    logout_user()
    token = User.query.filter_by(username='teste').first().get_jwt_token()
    
    json = {'description': 'Testando a rota update'}

    response = client.put(
        url_for('tarefas.update', id=1), 
        json=json, 
        headers={'Authorization': f'Bearer {token}'}
    )

    esperado = {'description': 'Testando a rota update', 'id': 1, 'priority': True, 'title': 'Teste de rota', 'type': 'lista'}

    assert response.status_code == 201
    assert response.json == esperado


def test_update_deve_retornar_403_caso_nao_seja_passado_um_token(client):
    logout_user()
    json = {'description': 'Testando a rota update'}

    response = client.put(url_for('tarefas.update', id=1), json=json)

    esperado =  {'error': 'Access Denied'}

    assert response.status_code == 403
    assert response.json == esperado


def test_rota_delete_deve_retornar_204_caso_o_token_seja_valido(client):
    logout_user()

    token = User.query.filter_by(username='teste').first().get_jwt_token()

    response = client.delete(
        url_for('tarefas.delete', id=1), 
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == 204


def test_rota_delete_deve_retornar_403_caso_o_token_seja_invalido(client):
    logout_user()

    token = 'Token invalido'

    response = client.delete(
        url_for('tarefas.delete', id=1), 
        headers={'Authorization': f'Bearer {token}'}
    )

    esperado = {'error': 'Invalid Token'}

    assert response.status_code == 403
    assert response.json == esperado
