from flask import Blueprint, request, jsonify
from sqlalchemy import select

from app.schemas import company_schema, companies_schema
from app.model import Company
from app.db import db
from app.errors import PathParamError

company_route_bp = Blueprint('company_routes', __name__, url_prefix='/company')


@company_route_bp.route('/CreateCompany', methods=('POST',))
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
        raise PathParamError(f'No company with id {company_id}')
    
    result = company_schema.dump(company)
    return jsonify(result), 200

@company_route_bp.route('/GetAllCompanies')
def get_all_companies():
    '''Get all companies

    '''
    stmt = select(Company)

    #TODO: Add any query parameters

    companies = db.session.scalars(stmt)

    result = companies_schema.dump(companies)
    return jsonify(result), 200

@company_route_bp.route('/UpdateCompany/<int:company_id>', methods=('PUT','PATCH'))
def update_company(company_id:int):
    '''Update details of a single company
    Path Params:
        company_id (int): ID of the company to update
    Body (All optional):
        Company_name(str): Name of the company
        Country(str): Home country of the company
        Email(str): Contact email address
        Phone(str): Contact phone number
        Address(str): Company street address
    '''

    company = db.session.get(Company, company_id)

    if not company:
        raise PathParamError(f'No company with id {company_id}')
    
    data = request.get_json()
    
    company = company_schema.load(data, instance=company, session=db.session, partial=True)
    db.session.commit()

    result = company_schema.dump(company)
    return jsonify(result), 200

@company_route_bp.route('/DeleteCompany/<int:company_id>', methods=('DELETE',))
def delete_company(company_id:int):
    '''Delete a single company
    Path Params:
        company_id (int): ID of the company to delete
    '''
    
    company = db.session.get(Company, company_id)
    
    if not company:
        raise PathParamError(f'No company with id {company_id}')
    
    #TODO: Validation re. ships - in schema?

    db.session.delete(company)
    db.session.commit()

    return jsonify({'message': f'Company "{company.company_name}" deleted.'}), 200