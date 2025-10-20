from sqlalchemy import types, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import db

class Company(db.Model):
    """
    Company model representing a shipping company.

    Fields:
        id: Primary key, unique identifier for the company
        company_name: Name of the company
        country: Country where the company is located
        email: Contact email
        phone: Contact phone number
        address: Company address
    """

    __tablename__ = 'companies'
    __table_args__ = (
        UniqueConstraint('company_name', 'country', name='companies_unique_company_name_country'),
    )
    id: Mapped[int] = mapped_column(types.Integer, primary_key=True)
    company_name: Mapped[str] = mapped_column(types.String(100))
    country: Mapped[str] = mapped_column(types.String(50))
    email: Mapped[str] = mapped_column(types.String(150), unique=True)
    phone: Mapped[str] = mapped_column(types.String(20))
    address: Mapped[str] = mapped_column(types.Text)

    ships: Mapped[list['Ship']] = relationship(back_populates='company')