from flask import jsonify, request, url_for
from functools import wraps
from flask_login import current_user, login_user

from app.models import User


def jwt_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        scheme = 'http'
        try:
            if 'https' in request.environ.get('HTTP_REFERER'):
                scheme = 'https'
        except:
            pass

        if request.environ.get('HTTP_REFERER') != url_for('tarefas.dashboard', _scheme=scheme, _external=True):
            token = request.headers.get('Authorization')

            if not token:
                return jsonify({'error': 'Access Denied'}), 403
            
            if not "Bearer" in token:
                return jsonify({'error': 'Invalid Token'}), 401

            try:
                token_pure = token.replace('Bearer ', '')
                login_user(User.verify_jwt_token(token_pure))
            except:
                return jsonify({'error': 'Invalid Token'}), 403
        
        return f(*args, **kwargs)
    return wrapper
