from flask import url_for
from flask_login import login_user

from app.models import User


def test_rota_index_deve_retornar_200_quando_acessada(conf_test):
    response_visitante = conf_test.get(url_for('tarefas.index'))

    usuario = User(
        username='Um Usuario De Teste', email='teste@email.com'
    )
    login_user(usuario)
    response_autenticado = conf_test.get(url_for('tarefas.index'))

    assert response_visitante.status_code == 200
    assert b'Visitante' in response_visitante.data
    assert b'/login' in response_visitante.data
    assert b'/dashboard' not in response_visitante.data

    assert response_autenticado.status_code == 200
    assert b'Um Usuario De Teste' in response_autenticado.data
    assert b'/dashboard' in response_autenticado.data
    assert b'/login' not in response_autenticado.data


def test_rota_login_deve_retornar_200_ou_quando_ja_autenticada_302(conf_test):
    response_visitante = conf_test.get(url_for('auth.login'))

    usuario = User(
        username='Um Usuario De Teste', email='teste@email.com'
    )
    login_user(usuario)
    response_autenticado = conf_test.get(url_for('auth.login'))

    assert response_visitante.status_code == 200
    assert b'<h1>Login</h1>' in response_visitante.data
    assert b'You should be redirected automatically to the target URL:' not in response_visitante.data

    assert response_autenticado.status_code == 302
    assert b'You should be redirected automatically to the target URL:' in response_autenticado.data
    assert b'<h1>Login</h1>' not in response_autenticado.data


def test_rota_register_deve_retornar_200_ou_quando_ja_autenticado_302(conf_test):
    response_visitante = conf_test.get(url_for('auth.register'))

    usuario = User(
        username='Um Usuario De Teste', email='teste@email.com'
    )
    login_user(usuario)
    response_autenticado = conf_test.get(url_for('auth.register'))

    assert response_visitante.status_code == 200
    assert b'<h1>Registrar</h1>' in response_visitante.data
    assert b'You should be redirected automatically to the target URL:' not in response_visitante.data

    assert response_autenticado.status_code == 302
    assert b'You should be redirected automatically to the target URL:' in response_autenticado.data
    assert b'<h1>Registrar</h1>' not in response_autenticado.data


def test_rota_dashboard_deve_retornar_202_ou_quando_nao_autenticado_302(conf_test):
    response_visitante = conf_test.get(url_for('tarefas.dashboard'))

    usuario = User(
        username='Um Usuario De Teste', email='teste@email.com'
    )
    login_user(usuario)
    response_autenticado = conf_test.get(url_for('tarefas.dashboard'))

    assert response_autenticado.status_code == 200
    assert b'<legend>Lista de Tarefas</legend>' in response_autenticado.data
    assert b'You should be redirected automatically to the target URL:' not in response_autenticado.data

    assert response_visitante.status_code == 302
    assert b'You should be redirected automatically to the target URL:' in response_visitante.data
    assert b'<legend>Lista de Tarefas</legend>' not in response_visitante.data


def test_rota_profile_deve_retornar_200_ou_quando_nao_autenticado_302(conf_test):
    response_visitante = conf_test.get(url_for('auth.profile'))

    usuario = User(
        username='Um Usuario De Teste', email='teste@email.com'
    )
    login_user(usuario)
    response_autenticado = conf_test.get(url_for('auth.profile'))

    assert response_autenticado.status_code == 200
    assert b'<h1>Editar Perfil</h1>' in response_autenticado.data
    assert b'You should be redirected automatically to the target URL:' not in response_autenticado.data

    assert response_visitante.status_code == 302
    assert b'You should be redirected automatically to the target URL:' in response_visitante.data
    assert b'<h1>Editar Perfil</h1>' not in response_visitante.data


def test_rota_apispec_deve_retornar_a_documentacao_da_api_do_projeto(conf_test):
    response = conf_test.get(url_for('flasgger.apispec'))

    assert response.status_code == 200
    assert response.json.get('info').get('title') == "API - Lista de Tarefas"
    assert '/auth/api/register' in response.json.get('paths')
    assert '/auth/api/get-token' in response.json.get('paths')
    assert '/create' in response.json.get('paths')
    assert '/collect' in response.json.get('paths')
    assert '/update/{id}' in response.json.get('paths')
    assert '/delete/{id}' in response.json.get('paths')
