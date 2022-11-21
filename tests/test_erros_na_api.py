from flask import url_for

from app.models import db, Tarefas, User


def test_rota_api_register_deve_recusar_dados_ou_metodos_invalidos(conf_test):
    json_valido = {
        'username': 'xpto', 'email': 'xpto@email.com', 'password': '123'
    }
    json_invalido = {
        'username': 'xpto2', 'email': 'xpto2@email.com'
    }

    usuario = User(username='xpto', email='xpto@email.com')
    usuario.set_password('123')
    db.session.add(usuario)
    db.session.commit()

    response_metodo_get = conf_test.get(
        url_for('auth.api_register'), json=json_valido
    )
    response_metodo_post_password = conf_test.post(
        url_for('auth.api_register'), json=json_invalido
    )
    response_metodo_post_existente = conf_test.post(
        url_for('auth.api_register'), json=json_valido
    )

    json_esperado_password = {
        'error': {
            'password': ['Missing data for required field.']
        }
    }
    json_esperado_existente = {
        'error': {
            'email': ['Email already in use.'], 
            'username': ['Username already in use.']
        }
    }

    assert response_metodo_get.status_code == 405
    assert response_metodo_get._status == '405 METHOD NOT ALLOWED'

    assert response_metodo_post_password.status_code == 400
    assert response_metodo_post_password.json == json_esperado_password

    assert response_metodo_post_existente.status_code == 400
    assert response_metodo_post_existente.json == json_esperado_existente


def test_rota_api_get_token_deve_recusar_usuarios_ou_metodos_invalidos(conf_test):
    usuario = User(username='xpto', email='xpto@email.com')
    usuario.set_password('123')
    db.session.add(usuario)
    db.session.commit()

    json_valido = {'email': 'xpto@email.com', 'password': '123'}
    json_invalido = {'email': 'xpto@email.com', 'password': '1234'}

    response_metodo_get = conf_test.get(
        url_for('auth.api_get_token'), json=json_valido
    )
    response_metodo_post = conf_test.post(
        url_for('auth.api_get_token'), json=json_invalido
    )

    json_esperado = {'error': 'Invalid credentials'}

    assert response_metodo_get.status_code == 405
    assert response_metodo_get._status == '405 METHOD NOT ALLOWED'

    assert response_metodo_post.status_code == 400
    assert response_metodo_post.json == json_esperado


def test_rota_create_deve_recusar_dados_invalidos_ou_nao_autenticados(conf_test):
    usuario = User(username='xpto', email='xpto@email.com')
    usuario.set_password('123')
    db.session.add(usuario)
    db.session.commit()
    
    token = usuario.get_jwt_token()
    json_valido = {
        'title': 'Um titulo', 
        'description': 'Uma descrição',
        'priority': True,
        'type': 'lista'
    }
    json_type_invalido = {
        'title': 'Um titulo', 
        'description': 'Uma descrição',
        'priority': True,
        'type': 'xpto'
    }
    json_xpto_invalido = {
        'title': 'Um titulo', 
        'description': 'Uma descrição',
        'priority': True,
        'type': 'lista',
        'xpto': 'xpto'
    }
    json_title_invalido = { 
        'description': 'Uma descrição',
        'priority': True,
        'type': 'lista'
    }

    response_metodo_get = conf_test.get(
        url_for('tarefas.create'), json=json_valido, 
        headers={'Authorization': f'Bearer {token}'}
    )
    response_metodo_post_nao_autenticado = conf_test.post(
        url_for('tarefas.create'), json=json_valido
    )
    response_metodo_post_autenticado_invalido = conf_test.post(
        url_for('tarefas.create'), 
        json=json_valido, 
        headers={'Authorization': f'Bearer token'}
    )
    response_metodo_post_autenticado_invalido_bearer = conf_test.post(
        url_for('tarefas.create'), 
        json=json_valido, 
        headers={'Authorization': f'Beare {token}'}
    )
    response_metodo_post_autenticado_type = conf_test.post(
        url_for('tarefas.create'), 
        json=json_type_invalido, 
        headers={'Authorization': f'Bearer {token}'}
    )
    response_metodo_post_autenticado_xpto = conf_test.post(
        url_for('tarefas.create'), 
        json=json_xpto_invalido, 
        headers={'Authorization': f'Bearer {token}'}
    )
    response_metodo_post_autenticado_title = conf_test.post(
        url_for('tarefas.create'), 
        json=json_title_invalido, 
        headers={'Authorization': f'Bearer {token}'}
    )

    json_esperado_nao_autenticado = {'error': 'Access Denied'}
    json_esperado_autenticado_invalido = {'error': 'Invalid Token'}
    json_esperado_autenticado_type = {
        'error': {
            'type': ['Type must be lista, fazer or feito.']
        }
    }
    json_esperado_autenticado_xpto = {'error': {'xpto': ['Unknown field.']}}
    json_esperado_autenticado_title = {
        'error': {
            'title': ['Missing data for required field.']
        }
    }

    assert response_metodo_get.status_code == 405
    assert response_metodo_get._status == '405 METHOD NOT ALLOWED'

    assert response_metodo_post_nao_autenticado.status_code == 403
    assert response_metodo_post_nao_autenticado.json == json_esperado_nao_autenticado

    assert response_metodo_post_autenticado_invalido.status_code == 403
    assert response_metodo_post_autenticado_invalido.json == json_esperado_autenticado_invalido

    assert response_metodo_post_autenticado_invalido_bearer.status_code == 401
    assert response_metodo_post_autenticado_invalido_bearer.json == json_esperado_autenticado_invalido

    assert response_metodo_post_autenticado_type.status_code == 400
    assert response_metodo_post_autenticado_type.json == json_esperado_autenticado_type

    assert response_metodo_post_autenticado_xpto.status_code == 400
    assert response_metodo_post_autenticado_xpto.json == json_esperado_autenticado_xpto

    assert response_metodo_post_autenticado_title.status_code == 400
    assert response_metodo_post_autenticado_title.json == json_esperado_autenticado_title


def test_rota_collect_deve_recusar_usuarios_nao_autenticados(conf_test):
    token_invalido = 'token'

    response_nao_autenticado = conf_test.get(
        url_for('tarefas.collect'),
        headers={'Authorization': f'Bearer {token_invalido}'}
    )
    response_nao_autenticado_bearer = conf_test.get(
        url_for('tarefas.collect'),
        headers={'Authorization': f'Beare {token_invalido}'}
    )

    json_esperado_nao_autenticado = {'error': 'Invalid Token'}

    assert response_nao_autenticado.status_code == 403
    assert response_nao_autenticado.json == json_esperado_nao_autenticado

    assert response_nao_autenticado_bearer.status_code == 401
    assert response_nao_autenticado_bearer.json == json_esperado_nao_autenticado
    

def test_roda_update_deve_recusar_usuarios_ou_dados_invalidos(conf_test):
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
    json_valido = {
        'title': 'Um titulo', 
        'description': 'Uma descrição',
        'priority': True,
        'type': 'lista'
    }
    json_invalido_type = {
        'title': 'Um titulo', 
        'description': 'Uma descrição',
        'priority': True,
        'type': 'xpto'
    }
    json_invalido_xpto = {
        'title': 'Um titulo', 
        'description': 'Uma descrição',
        'priority': True,
        'type': 'lista',
        'xpto': 'xpto'
    }
    json_invalido_id = {
        'title': 'Um titulo', 
        'description': 'Uma descrição',
        'priority': True,
        'type': 'lista',
        'id': 2
    }

    response_metodo_get = conf_test.get(
        url_for('tarefas.update', id=1), json=json_valido, 
        headers={'Authorization': f'Bearer {token}'}
    )
    response_metodo_put_invalido_token = conf_test.put(
        url_for('tarefas.update', id=1), json=json_valido, 
        headers={'Authorization': f'Bearer token'}
    )
    response_metodo_put_invalido_type = conf_test.put(
        url_for('tarefas.update', id=1), json=json_invalido_type, 
        headers={'Authorization': f'Bearer {token}'}
    )
    response_metodo_put_invalido_xpto = conf_test.put(
        url_for('tarefas.update', id=1), json=json_invalido_xpto, 
        headers={'Authorization': f'Bearer {token}'}
    )
    response_metodo_put_invalido_id = conf_test.put(
        url_for('tarefas.update', id=1), json=json_invalido_id, 
        headers={'Authorization': f'Bearer {token}'}
    )

    json_esperado_token = {'error': 'Invalid Token'}
    json_esperado_type = {'error': 'Type must be lista, fazer or feito'}
    json_esperado_xpto = {'error': json_invalido_xpto}
    json_esperado_id = {'error': 'Dont send the ID field'}

    assert response_metodo_get.status_code == 405
    assert response_metodo_get._status == '405 METHOD NOT ALLOWED'

    assert response_metodo_put_invalido_token.status_code == 403
    assert response_metodo_put_invalido_token.json == json_esperado_token

    assert response_metodo_put_invalido_type.status_code == 400
    assert response_metodo_put_invalido_type.json == json_esperado_type

    assert response_metodo_put_invalido_xpto.status_code == 400
    assert response_metodo_put_invalido_xpto.json == json_esperado_xpto

    assert response_metodo_put_invalido_id.status_code == 400
    assert response_metodo_put_invalido_id.json == json_esperado_id


def test_roda_delete_deve_recusar_usuarios_ou_dados_invalidos(conf_test):
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

    response_metodo_get = conf_test.get(
        url_for('tarefas.delete', id=1), 
        headers={'Authorization': f'Bearer {token}'}
    )
    response_metodo_delete_invalido_token = conf_test.delete(
        url_for('tarefas.delete', id=1), 
        headers={'Authorization': f'Bearer token'}
    )
    response_metodo_delete_invalido_bearer = conf_test.delete(
        url_for('tarefas.delete', id=1), 
        headers={'Authorization': f'Beare {token}'}
    )
    response_metodo_delete_invalido_id = conf_test.delete(
        url_for('tarefas.delete', id=2), 
        headers={'Authorization': f'Bearer {token}'}
    )

    json_esperado_token = {'error': 'Invalid Token'}
    json_esperado_id = {'error': {'2': 'Not Found'}}
    
    assert response_metodo_get.status_code == 405
    assert response_metodo_get._status == '405 METHOD NOT ALLOWED'

    assert response_metodo_delete_invalido_token.status_code == 403
    assert response_metodo_delete_invalido_token.json == json_esperado_token

    assert response_metodo_delete_invalido_bearer.status_code == 401
    assert response_metodo_delete_invalido_bearer.json == json_esperado_token

    assert response_metodo_delete_invalido_id.status_code == 400
    assert response_metodo_delete_invalido_id.json == json_esperado_id
