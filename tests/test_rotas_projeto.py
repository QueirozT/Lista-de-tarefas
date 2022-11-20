from flask import url_for

from app.models import User


def test_rota_register_deve_retornar_302_quando_criar_uma_nova_conta(client):
    data = {
        'username': 'Pessoa',
        'email': 'pessoa@email.com',
        'password': 'senha',
        'password2': 'senha'
    }

    response = client.post(url_for('auth.register'), data=data)

    assert response.status_code == 302
    response.request.path == url_for('auth.register')


def test_rota_login_deve_retornar_302_quando_os_dados_forem_corretos(client):
    data = {
        'email': 'pessoa@email.com',
        'password': 'senha'
    }

    response = client.post(url_for('auth.login'), data=data)

    assert response.status_code == 302
    response.request.path == url_for('auth.login')


def test_rota_profile_deve_retornar_302_quando_os_dados_forem_validos(client):
    data = {
        'username': 'teste',
        'email': 'teste@email.com',
    }

    response = client.post(url_for('auth.profile'), data=data)

    assert response.status_code == 302
    response.request.path == url_for('auth.profile')


def test_rota_logout_deve_retornar_302_quando_sair_de_uma_sessao(client):
    response = client.get(url_for('auth.logout'))

    assert response.status_code == 302
    response.request.path == url_for('auth.logout')


def test_rota_register_deve_retornar_200_quando_os_dados_forem_invalidos(client):
    data = {
        'username': 'Pessoa',
        'email': 'pessoa@email.com',
        'password': 'senha',
        'password2': 'diferente'
    }

    response = client.post(url_for('auth.register'), data=data)

    assert response.status_code == 200
    assert response.request.path == url_for('auth.register')


def test_rota_login_deve_retornar_302_quando_os_dados_forem_invalidos(client):
    data = {
        'email': 'pessoa@email.com',
        'password': 'outra'
    }

    response = client.post(url_for('auth.login'), data=data)

    assert response.status_code == 302
    assert response.request.path == url_for('auth.login')


def test_rota_dashboard_deve_retornar_302_quando_nao_estiver_autenticado(client):
    response = client.get(url_for('tarefas.dashboard'))

    assert response.status_code == 302
    response.request.path == url_for('tarefas.dashboard')


def test_rota_dashboard_deve_retornar_200_quando_estiver_autenticado(client):
    client.post(url_for('auth.login'), data={
        'email': 'teste@email.com', 'password': 'senha'
    })    

    response = client.get(url_for('tarefas.dashboard'))

    assert response.status_code == 200
    response.request.path == url_for('tarefas.dashboard')


def test_rota_index_deve_retornar_200_quando_acessada(client):
    response = client.get(url_for('tarefas.index'))

    assert response.status_code == 200


def test_rota_api_get_token_deve_retornar_200_e_o_token_quando_dados_forem_validos(client):
    json = {'email': 'teste@email.com', 'password': 'senha'}

    response = client.post(url_for('auth.api_get_token'), json=json)

    user = User.verify_jwt_token(response.json['token'])

    assert response.status_code == 200
    assert user.email == 'teste@email.com'


def test_rota_api_register_deve_aceitar_json_para_registrar_usuarios(client):
    json = {'username': 'xpto', 'email': 'xpto@email.com', 'password': '123'}

    response = client.post(url_for('auth.api_register'), json=json)

    esperado = {'email': 'xpto@email.com', 'username': 'xpto'}

    assert response.status_code == 201
    assert response.json == esperado


def test_rota_register_deve_retornar_400_quando_receber_dados_incorretos(client):
    json = {'username': 'xpto2', 'email': 'xpto2@email.com'}

    response = client.post(url_for('auth.api_register'), json=json)

    esperado = {'error': {'password': ['Missing data for required field.']}}

    assert response.status_code == 400
    assert response.json == esperado


def test_rota_api_register_deve_retornar_400_quando_os_dados_ja_existirem(client):
    json = {'username': 'xpto', 'email': 'xpto@email.com', 'password': '123'}

    response = client.post(url_for('auth.api_register'), json=json)

    esperado = {'error': {'email': ['Email already in use.'], 'username': ['Username already in use.']}}
    
    assert response.status_code == 400
    assert response.json == esperado


def test_rota_api_get_token_deve_retornar_400_quando_dados_forem_invalidos(client):
    json = {'email': 'xpto@email.com', 'password': '000'}

    response = client.post(url_for('auth.api_get_token'), json=json)

    esperado = {
        "error": "Usuário ou senha inválidos"
    }
    
    assert response.status_code == 400
    assert response.json == esperado
