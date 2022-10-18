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
