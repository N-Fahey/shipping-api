from flask import Blueprint

from .company_routes import company_route_bp

routes_bp = Blueprint('routes', __name__, url_prefix='/api/v1')

routes_bp.register_blueprint(company_route_bp)