from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow import fields, validate

from app.model import CargoType

class CargoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = CargoType
        load_instance = True
        fields = (
            'id',
            'cargo_name',
            'ships'
        )

    cargo_name = auto_field(validate=[
        validate.Length(min=3, max=50, error='Cargo name must be between {min} and {max} characters.')
    ])
    
    ships = fields.List(fields.Nested('ShipSchema', exclude=['cargo']))


cargo_schema = CargoSchema()
cargos_schema = CargoSchema(many=True)