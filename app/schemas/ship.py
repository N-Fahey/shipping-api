from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow import fields, validate

from app.model import Ship

class ShipSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Ship
        load_instance = True
        include_fk = True
        fields = (
            'id',
            'ship_name',
            'ship_length',
            'registration_country',
            'cargo_type_id',
            'company_id',
            'cargo_type',
            'company'
        )
        load_only = (
            'cargo_type_id',
            'company_id'
        )

    company = fields.Nested('CompanySchema', exclude=['ships'])
    cargo_type = fields.Nested('CargoSchema')

ship_schema = ShipSchema()
ships_schema = ShipSchema(many=True)