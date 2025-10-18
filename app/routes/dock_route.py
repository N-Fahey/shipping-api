from flask import Blueprint, request, jsonify
from sqlalchemy import select

from app.schemas import dock_schema, docks_schema
from app.model import Dock, DockCargo
from app.db import db
from app.errors import PathParamError, BodyError

dock_route_bp = Blueprint('dock_routes', __name__, url_prefix='/dock')

