from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow import fields, validate

from app.model import Dock

class DockSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Dock
        load_instance = True
        fields = (
            'id',
            'dock_code',
            'dock_length',
            'cargo_types'
        )
    
    cargo_types = fields.List(fields.Nested('CargoSchema', dump_only=True, exclude=['docks']))

    dock_code = auto_field(validate=[
        validate.Length(min=2, max=10, error='Dock name must be between {min} and {max} characters.'),
        validate.Regexp(r'^[a-zA-Z0-9]+$', error='Dock code must be alphanumeric and numbers only ([a-z], [A-Z], [0-9])')
    ])

    dock_length = auto_field(validate=[
        validate.Length(min=1, error='Dock length must be greater than 0.')
    ])

    #TODO: validation re. cargo types


dock_schema = DockSchema()
docks_schema = DockSchema(many=True)