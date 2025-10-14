from flask import Blueprint, request, jsonify

from app.schemas import company_schema
from app.db import db

company_route_bp = Blueprint('company_routes', __name__, url_prefix='/company')


@company_route_bp.route('/create_company', methods=['POST'])
def add_company():
    '''Create a new shipping company
    Expects:
        Company_name: Name of the company
        Country: Home country of the company
        Email: Contact email address
        Phone: Contact phone number
        Address: Company street address
    '''
    
    data = request.get_json()
    new_company = company_schema.load(data, session=db.session)
    
    db.session.add(new_company)
    db.session.commit()
    
    result = company_schema.dump(new_company)
    return jsonify(result), 201