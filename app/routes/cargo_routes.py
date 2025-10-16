from flask import Blueprint, request, jsonify
from sqlalchemy import select

from app.schemas import cargo_schema, cargos_schema
from app.model import CargoType
from app.db import db
from app.errors import PathParamError

cargo_route_bp = Blueprint('cargo_routes', __name__, url_prefix='/cargo')

@cargo_route_bp.route('/CreateCargo', methods=('POST',))
def add_cargo():
    '''Create a new cargo type

    Body data (JSON):
        cargo_name(str): Name of the cargo type
    '''
    
    data = request.get_json()
    new_cargo = cargo_schema.load(data, session=db.session)

    db.session.add(new_cargo)
    db.session.commit()
    
    result = cargo_schema.dump(new_cargo)
    return jsonify(result), 201

@cargo_route_bp.route('/GetCargoTypes')
def get_all_cargos():
    '''Get all cargo types

    '''
    stmt = select(CargoType)

    #TODO: Add any query parameters

    companies = db.session.scalars(stmt)

    result = cargos_schema.dump(companies)
    return jsonify(result), 200

@cargo_route_bp.route('/DeleteCargo/<int:cargo_id>', methods=('DELETE',))
def delete_cargo(cargo_id:int):
    '''Delete a single cargo type
    Path Params:
        cargo_id (int): ID of the cargo type to delete
    '''
    
    cargo = db.session.get(CargoType, cargo_id)
    
    if not cargo:
        raise PathParamError(f'No cargo type with id {cargo_id}')
    
    #TODO: Validation re. ships - in schema?

    #TODO: Finish route once ships done