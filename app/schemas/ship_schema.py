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
            'company',
            'bookings'
        )
        load_only = (
            'cargo_type_id',
            'company_id'
        )

    company = fields.Nested('CompanySchema', dump_only=True, exclude=['ships'])
    cargo_type = fields.Nested('CargoSchema', dump_only=True, only=['id', 'cargo_name'])
    bookings = fields.List(fields.Nested('BookingSchema', dump_only=True, exclude=['ship']))

    ship_name = auto_field(validate=[
        validate.Length(min=4, max=100, error='Ship name must be between {min} and {max} characters.')
    ])
    ship_length = auto_field(validate=[
        validate.Range(min=1, error='Ship length must be greater than 0.')
    ])
    registration_country = auto_field(validate=[
        validate.Length(min=4, max=50, error='Country name must be between {min} and {max} characters.')
    ])


ship_schema = ShipSchema()
ships_schema = ShipSchema(many=True)