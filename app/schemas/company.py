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

company_schema = CompanySchema()
companies_schema = CompanySchema(many=True)