from sqlalchemy import types, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db import db

class Ship(db.Model):
    """
    Ships model representing a ship.

    Fields:
        id: Primary key, unique identifier for the ship
        ship_name: Name of the ship
        registration_country: Country where the ship is registered
        cargo_type_id: ID of the cargo type this ship is configured for (FK to cargo_types)
        company_id: ID of the company this ship is registered to (FK to companies)
    """

    __tablename__ = 'ships'
    id: Mapped[int] = mapped_column(types.Integer, primary_key=True)
    ship_name: Mapped[str] = mapped_column(types.String(100))
    ship_length: Mapped[int] = mapped_column(types.Integer)
    registration_country: Mapped[str] = mapped_column(types.String(50))
    cargo_type_id: Mapped[int] = mapped_column(ForeignKey('cargo_types.id'))
    company_id: Mapped[int] = mapped_column(ForeignKey('companies.id'))
