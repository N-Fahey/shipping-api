from datetime import datetime, timedelta

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow import fields, validate, validates_schema, ValidationError, post_dump

from app.model import Booking

class BookingSchema(SQLAlchemyAutoSchema):
    """Schema to define load & dump validation rules for the Booking model

    Fields:
        booking_start (datetime): Start date & time of the booking
        booking_duration (int) Optional, load only: Duration (in hours) of the booking
        booking_end (datetime): End date & time of the booking
        booking_status (str): Status of the booking. Enum defined by StatusEnum in Booking model 
        ship_id (int) load only: ID of the ship this booking is for
        dock_id (int) load only: ID of the dock this booking is for
        ship (Ship) dump only: Nested ShipSchema of the ship with matching ship_id
        dock (Dock) dump only: Nested DockSchema of the dock with matching dock_id
    """
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

    ship = fields.Nested('ShipSchema', exclude=['bookings'])
    dock = fields.Nested('DockSchema', exclude=['bookings'])
    
    @validates_schema
    def validate_dates(self, data, **kwargs):
        """Validator function to check for any invalid dates supplied
        """
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
    def serialise_fields(self, data, **kwargs):
        '''Hook to post_dump to correctly serialise status enum field, rather than string representation of the Enum

        Remind me to just use constrained VARCHAR next time
        '''
        status = data.get('booking_status')
        start_str = data.get('booking_start')
        end_str = data.get('booking_end')

        if status:
            data['booking_status'] = status.split('.')[1]
        
        if start_str:
            data['booking_start'] = datetime.strptime(start_str, r'%Y-%m-%dT%H:%M:%S%z').strftime(r'%Y-%m-%d %H:%M')
        if end_str:
            data['booking_end'] = datetime.strptime(end_str, r'%Y-%m-%dT%H:%M:%S%z').strftime(r'%Y-%m-%d %H:%M')

        return data


booking_schema = BookingSchema()
bookings_schema = BookingSchema(many=True)