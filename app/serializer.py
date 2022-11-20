from marshmallow import fields, validates, ValidationError, post_dump,  post_load
from flask_marshmallow import Marshmallow

from .models import Tarefas, User

ma = Marshmallow()

def config(app):
    ma.init_app(app)


class TarefaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Tarefas
        load_instance = True

    title = fields.Str(required=True)
    description = fields.Str(required=True)
    type = fields.Str(required=True)
    priority = fields.Bool(required=True)
    user_id = fields.Int(required=True)

    @validates('id')
    def validate_id(self, value):
        raise ValidationError('Dont send the ID field.')

    @validates('title')
    def validate_title(self, value):
        value = value.strip()
        if not value or value is None:
            raise ValidationError('Title is required.')

    @validates('description')
    def validate_description(self, value):
        value = value.strip()
        if not value or value is None:
            raise ValidationError('Description is required.')

    @validates('type')
    def validate_type(self, value):
        if not value or value is None:
            raise ValidationError('Type is required.')
        elif value not in ['lista', 'fazer', 'feito']:
            raise ValidationError('Type must be lista, fazer or feito.')

    @post_dump
    def show_user(self, data, **kwargs):
        return {
            'id': data['id'],
            'title': data['title'],
            'description': data['description'],
            'type': data['type'],
            'priority': data['priority'],
        }


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True

    email = fields.Str(required=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True)

    @validates('email')
    def validate_email(self, email):
        user = User.query.filter_by(email=email).first()
        if user:
            raise ValidationError('Email already in use.')

    @validates('username')
    def validate_username(self, username):
        user = User.query.filter_by(username=username).first()
        if user:
            raise ValidationError('Username already in use.')

    @post_load
    def make_user(self, data, **kwargs):
        user = User(username=data.username, email=data.email)
        user.set_password(kwargs['partial'])
        return user

    @post_dump
    def show_user(self, data, **kwargs):
        return {
            'email': data['email'],
            'username': data['username']
        }
