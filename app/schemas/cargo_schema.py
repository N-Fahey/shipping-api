from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow import fields, validate

from app.model import CargoType

class CargoSchema(SQLAlchemyAutoSchema):
    """Schema to define load & dump validation rules for the Cargo model

    Fields:
        cargo_name (str): Name of the cargo type
        docks (list[Dock]) dump only: List of nested DockSchemas that accept this cargo type
    """
    class Meta:
        model = CargoType
        load_instance = True
        fields = (
            'id',
            'cargo_name',
            'docks'
        )

    cargo_name = auto_field(validate=[
        validate.Length(min=3, max=50, error='Cargo name must be between {min} and {max} characters.')
    ])
    
    docks = fields.List(fields.Nested('DockSchema', exclude=['cargo_types']))


cargo_schema = CargoSchema()
cargos_schema = CargoSchema(many=True)