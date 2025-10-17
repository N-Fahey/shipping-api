from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow import fields, validate

from app.model import Company

class CompanySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Company
        load_instance = True
        fields = (
            'id',
            'company_name',
            'country',
            'email',
            'phone',
            'address',
            'ships'
        )
    
    ships = fields.List(fields.Nested('ShipSchema', dump_only=True, exclude=['company']))

    company_name = auto_field(validate=[
        validate.Length(min=3, error='Company name must be greater than {min} characters.')
    ])
    country = auto_field(validate=[
        validate.Length(min=4, error='Country name must be greater than {min} characters.')
    ])
    email = auto_field(validate=[
        validate.Email(error='Enter a valid email address.')
    ])
    phone = auto_field(validate=[
        validate.Regexp(r'/^\+?[1-9][0-9]{7,14}$/', error='Enter a valid phone number. Must include international prefix in format"+[country code]"')
    ])
    address = auto_field(validate=[
        validate.Length(min=10, error='Address must be greater than {min} characters.')
    ])

    

company_schema = CompanySchema()
companies_schema = CompanySchema(many=True)