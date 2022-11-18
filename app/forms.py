from flask_wtf import FlaskForm
from wtforms import (
    BooleanField, PasswordField, StringField, SubmitField
)
from wtforms.validators import (
    DataRequired, EqualTo, Email, ValidationError
)

from app.models import User


class EditProfileForm(FlaskForm):
    username = StringField('Usuário')
    email = StringField('E-mail', validators=[Email()])
    password = PasswordField('Nova Senha')
    password2 = PasswordField(
        'Repetir a Senha', validators=[EqualTo('password')]
    )
    submit = SubmitField('Atualizar')

    def __init__(self, original_username, original_email, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError(
                    'Por favor, use um nome de usuário diferente.'
                )
    
    def validate_email(self, email):
        if email.data != self.original_email:
            user = User.query.filter_by(email=self.email.data).first()
            if  user is not None:
                raise ValidationError('Por favor, use um email diferente.')


class LoginForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
    remember_me = BooleanField('Lembrar?')
    submit = SubmitField('Entrar')


class RegistrationForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
    password2 = PasswordField(
        'Repetir Senha', validators=[DataRequired(), EqualTo('password')]
    )
    submit = SubmitField('Registrar')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(
                'Por favor, use um nome de usuário diferente.'
            )

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Por favor, use um e-mail diferente.')
