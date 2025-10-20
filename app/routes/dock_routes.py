from flask import Blueprint, request, jsonify
from sqlalchemy import select, delete

from app.schemas import dock_schema, docks_schema, dock_cargos_schema
from app.model import Dock, DockCargo
from app.db import db
from app.errors import PathParamError, BodyError

dock_route_bp = Blueprint('dock_routes', __name__, url_prefix='/dock')

@dock_route_bp.route('/CreateDock', methods=('POST',))
def add_dock():
    '''Create a new dock

    Body data (JSON):
        Dock_code (str): Unique identifying code for the dock
        Dock_length (int): Dock length (in meters) - the maximum size of dock the dock can accomodate
        Cargo_types (array[int]): Array of cargo_type IDs that the dock can receive
    ''' 
    data = request.get_json()

    dock_data_keys = ('dock_code', 'dock_length')
    dock_data = {key: data.get(key) for key in dock_data_keys if data.get(key)}

    if not dock_data:
        raise BodyError(f'None or incomplete attributes to update. Expected: dock_code, dock_length')

    new_dock = dock_schema.load(dock_data, session=db.session)
    db.session.add(new_dock)
    db.session.commit()

    cargo_type_ids = data.get('cargo_types')

    if cargo_type_ids:
        #Add the junction table entries for each cargo_type
        cargos_data = [
            {'cargo_type_id': cargo_type, 'dock_id': new_dock.id} for cargo_type in cargo_type_ids
        ]
        
        dock_cargos = dock_cargos_schema.load(cargos_data, session=db.session, many=True)
        db.session.add_all(dock_cargos)
        db.session.commit()
    
    result = dock_schema.dump(new_dock)
    return jsonify(result), 201

@dock_route_bp.route('/<int:dock_id>')
def get_dock(dock_id:int):
    '''Get details of a single dock

    Path Params:
        dock_id (int): ID of the dock to retrieve
    '''
    dock = db.session.get(Dock, dock_id)

    if not dock:
        raise PathParamError(f'No dock with id {dock_id}')
    
    result = dock_schema.dump(dock)
    return jsonify(result), 200

@dock_route_bp.route('/GetAllDocks')
def get_all_docks():
    '''Get all docks

    '''
    stmt = select(Dock)

    #TODO: Add any query parameters

    docks = db.session.scalars(stmt)

    result = docks_schema.dump(docks)
    return jsonify(result), 200

@dock_route_bp.route('/UpdateLength/<int:dock_id>', methods=('PUT','PATCH'))
def update_dock_length(dock_id:int):
    '''Update length of a single dock
    Path Params:
        dock_id (int): ID of the dock to update
    Body:
        dock_length (int): Length of the dock (in metres) - the maximum dock length it can accomodate
    '''

    dock = db.session.get(Dock, dock_id)

    if not dock:
        raise PathParamError(f'No dock with id {dock_id}')
    
    data = request.get_json()
    
    #Only allow updates to specified items
    allowed_updates = ('dock_length',)
    data = {key: data.get(key) for key in allowed_updates if data.get(key)}

    dock = dock_schema.load(data, instance=dock, session=db.session, partial=True)
    db.session.commit()

    result = dock_schema.dump(dock)
    return jsonify(result), 200

@dock_route_bp.route('/UpdateCargo/<int:dock_id>', methods=('PUT','PATCH'))
def update_dock_cargo(dock_id:int):
    '''Update cargo types of a single dock
    Path Params:
        dock_id (int): ID of the dock to update
    Body:
        cargo_types (array[int]): Array of cargo_type IDs that the dock can receive
    '''
    dock = db.session.get(Dock, dock_id)

    if not dock:
        raise PathParamError(f'No dock with id {dock_id}')
    
    data = request.get_json()
    
    #Only allow updates to specified items
    allowed_updates = ('cargo_types',)
    data = {key: data.get(key) for key in allowed_updates if data.get(key)}

    current_types = sorted([cargo.id for cargo in dock.cargo_types])
    update_types = sorted(data['cargo_types'])

    if current_types == update_types:
        raise BodyError(f'Cargo types unchanged.')
    
    #Delete current dock_cargo records
    stmt = delete(DockCargo).where(DockCargo.dock_id == dock.id)
    db.session.execute(stmt)

    #Create new records
    cargos_data = [
        {'cargo_type_id': cargo_type, 'dock_id': dock.id} for cargo_type in update_types
    ]
    new_dock_cargos = dock_cargos_schema.load(cargos_data, session=db.session, many=True)
    db.session.add_all(new_dock_cargos)
    db.session.commit()

    result = dock_schema.dump(dock)
    return jsonify(result), 200

@dock_route_bp.route('/DeleteDock/<int:dock_id>', methods=('DELETE',))
def delete_dock(dock_id:int):
    '''Delete a single dock. Also deletes matching dock_cargo records
    Path Params:
        dock_id (int): ID of the dock to delete
    '''
    
    dock = db.session.get(Dock, dock_id)
    
    if not dock:
        raise PathParamError(f'No dock with id {dock_id}')

    #Deletion removes records from junction table automatically
    db.session.delete(dock)
    db.session.commit()

    return jsonify({'message': f'Dock "{dock.dock_code}" deleted.'}), 200