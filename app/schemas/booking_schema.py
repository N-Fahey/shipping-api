from datetime import datetime, timedelta

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow import fields, validate, validates_schema, ValidationError, post_dump

from app.model import Booking

class BookingSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Booking
        load_instance = True
        include_fk = True
        fields = (
            'id',
            'booking_start',
            'booking_duration',
            'booking_end',
            'booking_status',
            'ship_id',
            'dock_id',
            'ship',
            'dock'
        )
        load_only = (
            'ship_id',
            'dock_id'
        )
    
    #Define booking_duration field
    booking_duration = fields.Integer(load_only=True)
    #Explicitly define booking_status field to avoid TypeError when deserialising, as Marshmallow automatically assigns as type Enum
    booking_status = fields.String(validate=validate.OneOf([status for status in Booking.booking_status.type.enums]))

    ship = fields.Nested('ShipSchema')
    dock = fields.Nested('DockSchema', exclude=['bookings'])
    
    @validates_schema
    def validate_dates(self, data, **kwargs):
        today = datetime.now().date()
        booking_start = data.get('booking_start')
        booking_end = data.get('booking_end')

        if not isinstance(booking_start, datetime) or not isinstance(booking_end, datetime):
            raise ValidationError('Booking start & end fields must be Python datetime objects supplied in format: YYYY-MM-DD HH:MM')

        if booking_start.date() < today:
            raise ValidationError('Booking start date cannot be earlier than today.')

        if booking_end <= booking_start:
            raise ValidationError('Booking end cannot be earlier than booking start.')

        if booking_end > booking_start + timedelta(hours=12):
            raise ValidationError('Maximum booking duration is 12 hours.') 
    
    @post_dump
    def serialise_status(self, data, **kwargs):
        '''Hook to post_dump to correctly serialise status enum field, rather than string representation of the Enum

        Remind me to just use constrained VARCHAR next time
        '''
        data['booking_status'] = data['booking_status'].split('.')[1]

        return data


booking_schema = BookingSchema()
bookings_schema = BookingSchema(many=True)