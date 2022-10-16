from crypt import methods
from flask import Blueprint, render_template

bp_auth = Blueprint('auth', __name__, url_prefix='/auth')


@bp_auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


@bp_auth.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')


@bp_auth.route('/profile', methods=['GET', 'POST'])
def profile():
    return render_template('perfil.html')