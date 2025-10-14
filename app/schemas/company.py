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
            'address'
        )

    #TODO: Implement relationship
    #ships = fields.List(fields.Nested('ShipSchema', exclude=['company']))

company_schema = CompanySchema()
companies_schema = CompanySchema(many=True)