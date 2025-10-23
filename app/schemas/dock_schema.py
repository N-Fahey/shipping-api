from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow import fields, validate

from app.model import Dock, DockCargo

class DockSchema(SQLAlchemyAutoSchema):
    """Schema to define load & dump validation rules for the Dock model

    Fields:
        dock_code (str): Identifying alphanumeric code for the dock
        dock_length (int): Length of the dock (in metres)
        cargo_types (list[CargoType]) dump only: List of nested CargoSchemas of cargo types this dock accepts
        bookings (list[Booking]) dump only: List of nested BookingSchemas made for this dock
    """
    class Meta:
        model = Dock
        load_instance = True
        fields = (
            'id',
            'dock_code',
            'dock_length',
            'cargo_types',
            'bookings'
        )
    
    cargo_types = fields.List(fields.Nested('CargoSchema', exclude=['docks']), dump_only=True)

    dock_code = auto_field(validate=[
        validate.Length(min=2, max=10, error='Dock name must be between {min} and {max} characters.'),
        validate.Regexp(r'^[a-zA-Z0-9]+$', error='Dock code must be alphanumeric and numbers only ([a-z], [A-Z], [0-9])')
    ])

    dock_length = auto_field(validate=[
        validate.Range(min=1, error='Dock length must be greater than 0.')
    ])

    bookings = fields.List(fields.Nested('BookingSchema', exclude=['dock']))
    #TODO: validation re. cargo types

class DockCargoSchema(SQLAlchemyAutoSchema):
    """Schema to define load & dump validation rules for the DockCargo model

    Fields:
        cargo_type_id (int): ID of the cargo type represented by this relationship
        dock_id (int): ID of the dock represented by this relationship
    """
    class Meta:
        model = DockCargo
        load_instance = True
        include_fk = True
        fields = (
            'id',
            'cargo_type_id',
            'dock_id'
        )

dock_schema = DockSchema()
docks_schema = DockSchema(many=True)

dock_cargos_schema = DockCargoSchema(many=True)