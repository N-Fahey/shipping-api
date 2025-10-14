from flask import Blueprint, request, jsonify
from sqlalchemy import select

from app.schemas import company_schema, companies_schema
from app.model import Company
from app.db import db

company_route_bp = Blueprint('company_routes', __name__, url_prefix='/company')


@company_route_bp.route('/create_company', methods=['POST'])
def add_company():
    '''Create a new shipping company
    
    Body data (JSON):
        Company_name(str): Name of the company
        Country(str): Home country of the company
        Email(str): Contact email address
        Phone(str): Contact phone number
        Address(str): Company street address
    '''
    
    data = request.get_json()
    new_company = company_schema.load(data, session=db.session)
    
    db.session.add(new_company)
    db.session.commit()
    
    result = company_schema.dump(new_company)
    return jsonify(result), 201

@company_route_bp.route('/<int:company_id>')
def get_company(company_id:int):
    '''Get a single company

    Path Params:
        company_id (int): ID of the company to retrieve
    '''
    company = db.session.get(Company, company_id)

    if not company:
        return {'message':f'No company with id {company_id}.'}, 404
    
    result = company_schema.dump(company)
    return jsonify(result), 200

@company_route_bp.route('/get_all_companies')
def get_all_companies():
    '''Get all companies

    '''
    stmt = select(Company)

    #TODO: Add any query parameters

    companies = db.session.scalars(stmt)

    result = companies_schema.dump(companies)
    return jsonify(result), 200