from flask import Blueprint

from app.db import db
from app.model import (
    Company,
    CargoType,
    Dock,
    Ship
)

cli_bp = Blueprint('db', __name__)

@cli_bp.cli.command('create')
def create_tables():
    print('Creating tables...')
    db.create_all()
    print(f"Tables created: {', '.join(db.metadata.tables.keys())}")
