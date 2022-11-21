from flask import url_for

from app.models import db, Tarefas, User


def test_rota_api_register_deve_retornar_201_e_registrar_um_novo_usuario(conf_test):
    json = {
        'username': 'xpto', 'email': 'xpto@email.com', 'password': '123'
    }

    response = conf_test.post(
        url_for('auth.api_register'), json=json
    )

    json_esperado = {'email': 'xpto@email.com', 'username': 'xpto'}

    assert response.status_code == 201
    assert response.json == json_esperado


def test_rota_api_get_token_deve_retornar_um_token_valido_quando_autenticar(conf_test):
    usuario = User(username='xpto', email='xpto@email.com')
    usuario.set_password('123')
    db.session.add(usuario)
    db.session.commit()

    json = {'email': 'xpto@email.com', 'password': '123'}

    response = conf_test.post(url_for('auth.api_get_token'), json=json)

    assert response.status_code == 200
    assert User.verify_jwt_token(response.json.get('token'))


def test_rota_create_deve_criar_uma_nova_tarefa_quando_receber_dados_validos(conf_test):
    usuario = User(username='xpto', email='xpto@email.com')
    usuario.set_password('123')
    db.session.add(usuario)
    db.session.commit()
    
    token = usuario.get_jwt_token()
    json = {
        'title': 'Um titulo', 
        'description': 'Uma descrição',
        'priority': True,
        'type': 'lista'
    }

    response = conf_test.post(
        url_for('tarefas.create'),
        json=json, 
        headers={'Authorization': f'Bearer {token}'}
    )

    esperado = {
        'id': 1, 
        'title': 'Um titulo', 
        'description': 'Uma descrição', 
        'priority': True, 
        'type': 'lista'
    }

    assert response.status_code == 201
    assert response.json == esperado


def test_rota_collect_deve_retornar_todas_as_tarefas_do_usuario_autenticado(conf_test):
    usuario = User(username='xpto', email='xpto@email.com')
    usuario.set_password('123')
    
    tarefa = Tarefas(
        title='Um titulo',
        description='Uma descrição',
        type='lista',
        priority=False,
        user_id=1
    )
    
    db.session.add_all([usuario, tarefa])
    db.session.commit()
    
    token = usuario.get_jwt_token()

    response = conf_test.get(
        url_for('tarefas.collect'),
        headers={'Authorization': f'Bearer {token}'}
    )

    esperado = [
        {
            'id': 1, 
            'title': 'Um titulo', 
            'description': 'Uma descrição', 
            'priority': False, 
            'type': 'lista'
        }
    ]

    assert response.status_code == 200
    assert response.json == esperado


def test_rota_update_deve_atializar_uma_tarefa_quando_receber_dados_validos(conf_test):
    usuario = User(username='xpto', email='xpto@email.com')
    usuario.set_password('123')
    
    tarefa = Tarefas(
        title='Um titulo',
        description='Uma descrição',
        type='lista',
        priority=False,
        user_id=1
    )
    
    db.session.add_all([usuario, tarefa])
    db.session.commit()
    
    token = usuario.get_jwt_token()
    json = {
        'title': 'Um titulo', 
        'description': 'Uma descrição',
        'priority': False, 
        'type': 'fazer'
    }

    response = conf_test.put(
        url_for('tarefas.update', id=1),
        json=json,
        headers={'Authorization': f'Bearer {token}'}
    )

    esperado = {
        'id': 1, 
        'title': 'Um titulo', 
        'description': 'Uma descrição', 
        'priority': False, 
        'type': 'fazer'
    }

    assert response.status_code == 201
    assert response.json == esperado


def test_rota_delete_deve_remover_uma_tarefa_quando_receber_dados_validos(conf_test):
    usuario = User(username='xpto', email='xpto@email.com')
    usuario.set_password('123')
    
    tarefa = Tarefas(
        title='Um titulo',
        description='Uma descrição',
        type='lista',
        priority=False,
        user_id=1
    )
    
    db.session.add_all([usuario, tarefa])
    db.session.commit()
    
    token = usuario.get_jwt_token()
    
    response = conf_test.delete(
        url_for('tarefas.delete', id=1),
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == 204
    assert response.json == None
