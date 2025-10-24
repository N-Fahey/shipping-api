from flask import Blueprint

from .company_routes import company_route_bp
from .cargo_routes import cargo_route_bp
from .ship_routes import ship_route_bp
from .dock_routes import dock_route_bp
from .booking_routes import booking_route_bp

routes_bp = Blueprint('routes', __name__, url_prefix='/api/v1')

routes_bp.register_blueprint(company_route_bp)
routes_bp.register_blueprint(cargo_route_bp)
routes_bp.register_blueprint(ship_route_bp)
routes_bp.register_blueprint(dock_route_bp)
routes_bp.register_blueprint(booking_route_bp)