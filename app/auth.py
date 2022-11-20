from flasgger import swag_from
from flask import (
    Blueprint, current_app, flash, redirect, 
    render_template, request, url_for, jsonify
)
from flask_login import current_user, login_required, login_user, logout_user
from flask_marshmallow import exceptions
from werkzeug.urls import url_parse

from app.models import User
from app.flasgger import specs_get_token, specs_register
from app.forms import (
    LoginForm, RegistrationForm, EditProfileForm
)
from app.serializer import UserSchema


bp_auth = Blueprint('auth', __name__, url_prefix='/auth')


@bp_auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('tarefas.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user is None or not user.check_password(form.password.data):
            flash('Email ou senha inválidos')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)

        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('tarefas.index')
        
        return redirect(next_page)

    return render_template('login.html', title='Entrar', form=form)


@bp_auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('tarefas.index'))


@bp_auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('tarefas.index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data.strip(), email=form.email.data)
        user.set_password(form.password.data)
        current_app.db.session.add(user)
        current_app.db.session.commit()
        flash('Parabéns! Você se registrou com sucesso!')
        return redirect(url_for('auth.login'))

    return render_template('register.html', title='Registro', form=form)


@bp_auth.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = EditProfileForm(current_user.username, current_user.email)
    if form.validate_on_submit():
        current_user.username = form.username.data.strip()
        current_user.email = form.email.data
        if form.password.data:
            current_user.set_password(form.password.data)
        current_app.db.session.commit()
        flash('Suas alterações foram salvas!')
        return redirect(url_for('auth.profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    return render_template('perfil.html', title='Editar Perfil', form=form)


@bp_auth.route('/api/register', methods=['POST'])
@swag_from(specs_register)
def api_register():
    if request.is_json:
        us = UserSchema()
        try:
            user = us.load(
                request.json, 
                partial=request.json.get('password')
            )
        except exceptions.ValidationError as e:
            return jsonify({'error': e.messages_dict}), 400
        else:
            current_app.db.session.add(user)
            current_app.db.session.commit()
            return us.jsonify(user), 201


@bp_auth.route('/api/get-token', methods=["POST"])
@swag_from(specs_get_token)
def api_get_token():
    if current_user.is_authenticated:
        logout_user()
    
    email = request.json['email']
    password = request.json['password']
    user = User.query.filter_by(email=email).first()
    if user is None or not user.check_password(password):
        return jsonify({'error': 'Usuário ou senha inválidos'}), 400
    
    return jsonify({'token': user.get_jwt_token()}), 200
