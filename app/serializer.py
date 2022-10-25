from marshmallow import fields, validates, ValidationError
from flask_marshmallow import Marshmallow

from .models import Tarefas

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
        if not value or value is None:
            raise ValidationError('Title is required.')

    @validates('description')
    def validate_description(self, value):
        if not value or value is None:
            raise ValidationError('Description is required.')

    @validates('type')
    def validate_type(self, value):
        if not value or value is None:
            raise ValidationError('Type is required.')
        elif value not in ['lista', 'fazer', 'feito']:
            raise ValidationError('Type must be lista, fazer or feito.')
