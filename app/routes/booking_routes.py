from datetime import datetime, timedelta

from flask import Blueprint, request, jsonify
from sqlalchemy import select

from app.schemas import booking_schema, bookings_schema
from app.model import Booking
from app.db import db
from app.errors import PathParamError, BodyError, QueryParamError

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

    #TODO: Controller/schema level validation of overlapping bookings - using get route

    #Load new booking
    new_booking = booking_schema.load(data, session=db.session)

    db.session.add(new_booking)
    db.session.commit()
    
    result = booking_schema.dump(new_booking)
    return jsonify(result), 201

@booking_route_bp.route('/<int:booking_id>')
def get_booking(booking_id:int):
    '''Get a single booking

    Path Params:
        booking_id (int): ID of the booking to retrieve
    '''
    booking = db.session.get(Booking, booking_id)

    if not booking:
        raise PathParamError(f'No booking with id {booking_id}')
    
    result = booking_schema.dump(booking)
    return jsonify(result), 200

@booking_route_bp.route('/GetAllBookings')
def get_all_bookings():
    '''Get all bookings
    Query Params (All optional):
        from_time (datetime): Retrieve matching bookings at or after provided time, in format YYYY-MM-DD HH:MM
        to_time (datetime): Retrieve matching bookings before or to provided time, in format YYYY-MM-DD HH:MM
        status (str): Retrieve matching bookings with specified booking status
        dock_id (int): Retrieve bookings for specified dock
        ship_id (int): Retrieve bookings for specified ship

    '''

    q_from_time = request.args.get('from_time')
    q_to_time = request.args.get('to_time')
    status = request.args.get('status')
    dock_id = request.args.get('dock_id', type=int)
    ship_id = request.args.get('ship_id', type=int)

    try:
        from_time = datetime.strptime(q_from_time, r'%Y-%m-%d %H:%M') if q_from_time else None
        to_time = datetime.strptime(q_to_time, r'%Y-%m-%d %H:%M') if q_to_time else None
    except ValueError:
        raise QueryParamError('Invalid input supplied. from_time and to_time must match format: YYYY-MM-DD HH:MM')

    stmt = select(Booking)
    # Handle from/to time
    if from_time and to_time:
        stmt = stmt.where(
            (Booking.booking_start < to_time) & (Booking.booking_end > from_time)
        )
    else:
        if from_time:
            stmt = stmt.where(Booking.booking_end > from_time)
        if to_time:
            stmt = stmt.where(Booking.booking_start < to_time)
    
    if status:
        stmt = stmt.where(Booking.booking_status == status.upper())
    if dock_id:
        stmt = stmt.where(Booking.dock_id == dock_id)
    if ship_id:
        stmt = stmt.where(Booking.ship_id == ship_id)

    bookings = db.session.scalars(stmt)

    result = bookings_schema.dump(bookings)
    return jsonify(result), 200

@booking_route_bp.route('/UpdateBooking/<int:booking_id>', methods=('PUT','PATCH'))
def update_booking(booking_id:int):
    '''Update details of a single booking
    Path Params:
        booking_id (int): ID of the booking to update
    Body (All optional):
        booking_start (datetime): Update booking start time, using format YYYY-MM-DD HH:MM
        booking_end (datetime): Update booking end time, using format YYYY-MM-DD HH:MM
        booking_status (int): Contact phone number
    '''

    booking = db.session.get(Booking, booking_id)

    if not booking:
        raise PathParamError(f'No ship with id {booking_id}')
    
    data = request.get_json()

    #Only allow updates to specified items
    allowed_updates = ('booking_start', 'booking_end', 'booking_status')
    data = {key: data.get(key) for key in allowed_updates if data.get(key)}
    
    if not data:
        raise BodyError(f'No valid attributes to update. Allowed attributes: {", ".join(allowed_updates)}')

    booking = booking_schema.load(data, instance=booking, session=db.session, partial=True)
    db.session.commit()

    result = booking_schema.dump(booking)
    return jsonify(result), 200

@booking_route_bp.route('/DeleteBooking/<int:booking_id>', methods=('DELETE',))
def delete_company(booking_id:int):
    '''Delete a single booking
    Path Params:
        booking_id (int): ID of the booking to delete
    '''
    
    booking = db.session.get(Booking, booking_id)
    
    if not booking:
        raise PathParamError(f'No booking with id {booking_id}')

    db.session.delete(booking)
    db.session.commit()

    return jsonify({'message': f'Booking with ID {booking_id} deleted.'}), 200