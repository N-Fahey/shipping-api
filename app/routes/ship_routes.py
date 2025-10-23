from flask import Blueprint, request, jsonify
from sqlalchemy import select

from app.schemas import ship_schema, ships_schema
from app.model import Ship, Booking
from app.db import db
from app.errors import PathParamError, BodyError

ship_route_bp = Blueprint('ship_routes', __name__, url_prefix='/ship')

@ship_route_bp.route('/CreateShip', methods=('POST',))
def add_ship():
    '''Create a new ship

    Body data (JSON):
        Ship_name(str): Name of the ship
        Registration_country(str): The ship's country of registration
        Cargo_type_id (int): ID for the ships configured cargo type
        Ship_id(int): ID for the ships owning ship
    ''' 
    
    data = request.get_json()
    new_ship = ship_schema.load(data, session=db.session)
    
    db.session.add(new_ship)
    db.session.commit()
    
    result = ship_schema.dump(new_ship)
    return jsonify(result), 201

@ship_route_bp.route('/<int:ship_id>')
def get_ship(ship_id:int):
    '''Get a single ship

    Path Params:
        ship_id (int): ID of the ship to retrieve
    '''
    ship = db.session.get(Ship, ship_id)

    if not ship:
        raise PathParamError(f'No ship with id {ship_id}')
    
    result = ship_schema.dump(ship)
    return jsonify(result), 200

@ship_route_bp.route('/GetAllShips')
def get_all_ships():
    '''Get all ships

    '''
    stmt = select(Ship)

    #TODO: Add  query parameters: per ship ID, per cargo type, min/max length?

    ships = db.session.scalars(stmt)

    result = ships_schema.dump(ships)
    return jsonify(result), 200

@ship_route_bp.route('/UpdateShip/<int:ship_id>', methods=('PUT','PATCH'))
def update_ship(ship_id:int):
    '''Update details of a single ship
    Path Params:
        ship_id (int): ID of the ship to update
    Body (All optional):
        Registration_country (str): The ship's country of registration
        Cargo_type_id (int): Contact phone number
        Company_id (int): The ship's owning company
    '''

    ship = db.session.get(Ship, ship_id)

    if not ship:
        raise PathParamError(f'No ship with id {ship_id}')
    
    data = request.get_json()

    #Only allow updates to specified items
    allowed_updates = ('registration_country', 'cargo_type_id', 'company_id')
    data = {key: data.get(key) for key in allowed_updates if data.get(key)}
    
    if not data:
        raise BodyError(f'No valid attributes to update. Allowed attributes: {", ".join(allowed_updates)}')

    ship = ship_schema.load(data, instance=ship, session=db.session, partial=True)
    db.session.commit()

    result = ship_schema.dump(ship)
    return jsonify(result), 200

@ship_route_bp.route('/DeleteShip/<int:ship_id>', methods=('DELETE',))
def delete_ship(ship_id:int):
    '''Delete a single ship
    Path Params:
        ship_id (int): ID of the ship to delete
    '''
    
    ship = db.session.get(Ship, ship_id)
    
    if not ship:
        raise PathParamError(f'No ship with id {ship_id}')
    
    #Check if ship exists in any bookings
    stmt = select(Booking).where(Booking.ship_id == ship.id)

    existing_bookings = db.session.scalars(stmt).all()
    if existing_bookings:
        raise PathParamError(f'Unable to delete ship with id {ship_id}. Remove existing bookings for this ship first.')

    db.session.delete(ship)
    db.session.commit()

    return jsonify({'message': f'Ship "{ship.ship_name}" deleted.'}), 200