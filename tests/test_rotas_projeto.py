from flask import url_for


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
