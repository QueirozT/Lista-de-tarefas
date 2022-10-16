from flask import (
    Blueprint, redirect, render_template, request, url_for
)
from flask_login import current_user

bp_auth = Blueprint('auth', __name__, url_prefix='/auth')


@bp_auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html', current_user=current_user)


@bp_auth.route('/logout')
def logout():
    return redirect(url_for('auth.login'))


@bp_auth.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html', current_user=current_user)


@bp_auth.route('/profile', methods=['GET', 'POST'])
def profile():
    return render_template('perfil.html', current_user=current_user)