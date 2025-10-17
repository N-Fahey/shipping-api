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
            'company_id'
        )

    #TODO: Implement relationships - cargo, company
    #ships = fields.List(fields.Nested('ShipSchema', exclude=['company']))

ship_schema = ShipSchema()
ships_schema = ShipSchema(many=True)