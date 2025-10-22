from sqlalchemy import types, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import db

class CargoType(db.Model):
    """
    CargoType model representing a cargo type.

    Fields:
        id: Primary key, unique identifier for the cargo type
        cargo_name: The name of the cargo type
    """

    __tablename__ = 'cargo_types'
    __table_args__ = (
        CheckConstraint("length(cargo_name) > 2", name="check_cargo_name_length"),
    )    
    id: Mapped[int] = mapped_column(types.Integer, primary_key=True)
    cargo_name: Mapped[str] = mapped_column(types.String(50), unique=True)

    docks: Mapped[list['Dock']] = relationship(secondary="dock_cargo", back_populates="cargo_types")