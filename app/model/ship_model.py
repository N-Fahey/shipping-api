from sqlalchemy import types, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import db

class Ship(db.Model):
    """
    Ships model representing a ship.

    Fields:
        id: Primary key, unique identifier for the ship
        ship_name: Name of the ship
        ship_length: Length (in metres) of the ship
        registration_country: Country where the ship is registered
        cargo_type_id: ID of the cargo type this ship is configured for (FK to cargo_types)
        company_id: ID of the company this ship is registered to (FK to companies)
    """

    __tablename__ = 'ships'
    __table_args__ = (
        UniqueConstraint('ship_name', 'company_id', name='ships_unique_ship_name_company_id'),
    )

    id: Mapped[int] = mapped_column(types.Integer, primary_key=True)
    ship_name: Mapped[str] = mapped_column(types.String(100))
    ship_length: Mapped[int] = mapped_column(types.Integer)
    registration_country: Mapped[str] = mapped_column(types.String(50))
    cargo_type_id: Mapped[int] = mapped_column(ForeignKey('cargo_types.id'))
    company_id: Mapped[int] = mapped_column(ForeignKey('companies.id'))

    cargo_type: Mapped['CargoType'] = relationship()
    company: Mapped['Company'] = relationship(back_populates='ships')
    bookings: Mapped[list['Booking']] = relationship(back_populates='ship')