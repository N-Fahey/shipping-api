from flask import Blueprint
from sqlalchemy import text

from app.db import db
from app.model import (
    Booking,
    Company,
    CargoType,
    Dock,
    DockCargo,
    Ship
)

cli_bp = Blueprint('db', __name__)

@cli_bp.cli.command('create')
def create_tables():
    '''Command to create all tables defined in the model
    Also installs btree_gist extension as required by bookings exclude constraints
    '''
    print('Creating tables...')
    db.session.execute(text('CREATE EXTENSION IF NOT EXISTS btree_gist'))
    db.session.commit()
    db.create_all()
    print(f"Tables created: {', '.join(db.metadata.tables.keys())}")

@cli_bp.cli.command('drop')
def drop_tables():
    '''Command to drop all tables defined in the model
    Cleans up btree_gist extension
    '''
    db.drop_all()
    db.session.execute(text('DROP EXTENSION IF EXISTS btree_gist'))
    db.session.commit()
    print('All tables dropped.')

@cli_bp.cli.command('truncate')
def truncate_tables():
    '''Command to truncate all tables defined in the model
    '''
    table_names_str = ', '.join(db.metadata.tables.keys())
    db.session.execute(text(f'TRUNCATE TABLE {table_names_str}'))
    db.session.commit()

    print(f'Truncated tables: {table_names_str}')

@cli_bp.cli.command('seed')
def seed_data():
    '''Command to seed test data into the database
    Test data can be removed with flask db truncate
    '''
    cargo_types = [
        CargoType(cargo_name='Container'),
        CargoType(cargo_name='Fuel'),
        CargoType(cargo_name='Grain'),
        CargoType(cargo_name='Vehicles'),
        CargoType(cargo_name='Passengers')
    ]

    companies = [
        Company(company_name='Shipping Co', country='Australia', email='contact@shipping.co', phone='+61(02)12345678', address='123 Ship St, Melbourne 3000 VIC Australia'),
        Company(company_name='American Ferry Lines', country='USA', email='email@ferries.com', phone='+1(555)123-4567', address='66 Ferry Way, Atlanta, Georgia USA'),
        Company(company_name='Swedish Flour Distributors', country='Sweden', email='hej@fish.net', phone='+46 111 111 111', address='44 Floury Drive, Stockholm Sweden')
    ]

    db.session.add_all(cargo_types+companies)
    db.session.commit()

    docks = [
        Dock(dock_code='C01', dock_length=250),
        Dock(dock_code='C02', dock_length=200),
        Dock(dock_code='FG01', dock_length=280),
        Dock(dock_code='VP01', dock_length=310),
        Dock(dock_code='V01', dock_length=200)
    ]

    ships = [
        Ship(ship_name='SS ContainerShip', ship_length=210, registration_country='New Zealand', cargo_type_id=cargo_types[0].id, company_id=companies[0].id),
        Ship(ship_name='Got Fuel?', ship_length=240, registration_country='Cayman Islands', cargo_type_id=cargo_types[1].id, company_id=companies[0].id),
        Ship(ship_name='Ferry Odd Parents', ship_length=160, registration_country='USA', cargo_type_id=cargo_types[4].id, company_id=companies[1].id),
        Ship(ship_name='Pride Of Sweden', ship_length=260, registration_country='Norway', cargo_type_id=cargo_types[2].id, company_id=companies[2].id),
        Ship(ship_name='I Love Cars', ship_length=300, registration_country='China', cargo_type_id=cargo_types[3].id, company_id=companies[0].id),
        Ship(ship_name='Mud Island Cruises', ship_length=100, registration_country='Australia', cargo_type_id=cargo_types[4].id, company_id=companies[1].id)
    ]

    db.session.add_all(docks+ships)
    db.session.commit()

    dock_cargo = [
        DockCargo(cargo_type_id=cargo_types[0].id, dock_id=docks[0].id),
        DockCargo(cargo_type_id=cargo_types[0].id, dock_id=docks[1].id),
        DockCargo(cargo_type_id=cargo_types[1].id, dock_id=docks[2].id),
        DockCargo(cargo_type_id=cargo_types[2].id, dock_id=docks[2].id),
        DockCargo(cargo_type_id=cargo_types[3].id, dock_id=docks[3].id),
        DockCargo(cargo_type_id=cargo_types[4].id, dock_id=docks[3].id),
        DockCargo(cargo_type_id=cargo_types[3].id, dock_id=docks[4].id)
    ]

    db.session.add_all(dock_cargo)
    db.session.commit()

    # bookings = [
    #     Booking()
    # ]

    # db.session.add_all(bookings)
    # db.session.commit()

    print('Seed data inserted')