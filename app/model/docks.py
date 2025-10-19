from sqlalchemy import types
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
    #TODO: Add Check constraints - dock_length, dock_code(min)

    id: Mapped[int] = mapped_column(types.Integer, primary_key=True)
    dock_code: Mapped[str] = mapped_column(types.String(10), unique=True)
    dock_length: Mapped[int] = mapped_column(types.Integer)

    cargo_types: Mapped[list['CargoType']] = relationship(
        secondary="dock_cargo",
        back_populates="docks"
    )