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
    print('Creating tables...')
    db.session.execute(text('CREATE EXTENSION IF NOT EXISTS btree_gist'))
    db.session.commit()
    db.create_all()
    print(f"Tables created: {', '.join(db.metadata.tables.keys())}")

@cli_bp.cli.command('drop')
def drop_tables():
    db.drop_all()
    db.session.execute(text('DROP EXTENSION IF EXISTS btree_gist'))
    db.session.commit()
    print('All tables dropped.')
