from datetime import datetime, timedelta

from flask import Blueprint, request, jsonify
from sqlalchemy import select

from app.schemas import booking_schema, bookings_schema
from app.model import Booking
from app.db import db
from app.errors import PathParamError, BodyError

booking_route_bp = Blueprint('booking_routes', __name__, url_prefix='/booking')

@booking_route_bp.route('/CreateBooking', methods=('POST',))
def create_booking():
    '''Create a new booking. One of booking_duration or booking_end must be supplied

    Body data (JSON):
        booking_start (datetime): The date / time of the start of the booking. FORMAT: (YYYY-MM-DD HH:MM)
        OPTIONAL: booking_duration (int): The duration (in hours) of the booking
        OPTIONAL: booking_end (datetime): The date / time of the end of the booking. FORMAT: (YYYY-MM-DD HH:MM)
        booking_status (str): The current status of the booking, from [PENDING, CONFIRMED]
        ship_id (int): ID of the ship this booking is for
        dock_id (int): ID of the dock this booking is for
    '''

    data = request.get_json()
    
    #Process start/end datetime
    start_str = data.pop('booking_start', None)
    end_str = data.pop('booking_end', None)
    duration = data.pop('booking_duration', None)


    if end_str and duration:
        raise BodyError('Conflicting information supplied. Only one of booking_duration, booking_end can be supplied.')

    start_datetime = datetime.strptime(start_str, r'%Y-%m-%d %H:%M')
    end_datetime = start_datetime + timedelta(hours=duration) if duration \
        else datetime.strptime(end_str, r'%Y-%m-%d %H:%M')

    data['booking_start'] = start_datetime
    data['booking_end'] = end_datetime

    #TODO: Controller/schema level validation of overlapping bookings

    #Load new booking
    new_booking = booking_schema.load(data, session=db.session)

    db.session.add(new_booking)
    db.session.commit()
    
    result = booking_schema.dump(new_booking)
    return jsonify(result), 201