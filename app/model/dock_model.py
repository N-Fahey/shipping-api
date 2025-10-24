from sqlalchemy import types, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import db

class Dock(db.Model):
    """
    Docks model representing a dock.

    Fields:
        id: Primary key, unique identifier for the dock
        dock_code: Unique identifying code for the dock
        dock_length: Size of the dock in metres, also maximum length of ship using the dock
    """

    __tablename__ = 'docks'
    __table_args__ = (
        CheckConstraint('dock_length > 0', name='check_dock_length'),
        CheckConstraint('length(dock_code) > 1', name='check_dock_code_length'),
        CheckConstraint("regexp_like(dock_code, '^[a-zA-Z0-9]+$')", name='check_dock_code_regex')
    )
    id: Mapped[int] = mapped_column(types.Integer, primary_key=True)
    dock_code: Mapped[str] = mapped_column(types.String(10), unique=True)
    dock_length: Mapped[int] = mapped_column(types.Integer)

    cargo_types: Mapped[list['CargoType']] = relationship(secondary="dock_cargo", back_populates="docks")
    bookings: Mapped[list['Booking']] = relationship(back_populates='dock')