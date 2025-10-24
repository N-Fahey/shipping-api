from sqlalchemy import types, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db import db

class DockCargo(db.Model):
    """
    DockCargo model representing accepted cargo types for docks.

    Fields:
        id: Primary key, unique identifier for the dock/cargo relationship
        cargo_type_id: ID of the cargo type this dock is configured for (FK to cargo_types)
        dock_id: ID of the dock this relationship is for (FK to docks)
    """

    __tablename__ = 'dock_cargo'
    __table_args__ = (
        UniqueConstraint('cargo_type_id', 'dock_id', name='dock_cargo_unique_cargo_type_id_dock_id'),
    )

    id: Mapped[int] = mapped_column(types.Integer, primary_key=True)
    cargo_type_id: Mapped[int] = mapped_column(ForeignKey('cargo_types.id'))
    dock_id: Mapped[int] = mapped_column(ForeignKey('docks.id'))

