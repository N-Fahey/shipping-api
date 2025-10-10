from sqlalchemy import types, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db import db

class Dock(db.Model):
    """
    Docks model representing a dock.

    Fields:
        id: Primary key, unique identifier for the dock
        dock_code: Unique identifying code for the dock
        dock_length: Size of the dock in metres, also maximum length of ship using the dock
        cargo_type_id: ID of the cargo type this dock is configured for (FK to cargo_types)
                        Can be set to Null when dock is unusable, e.g: being reconfigured or another cargo
    """

    __tablename__ = 'docks'
    id: Mapped[int] = mapped_column(types.Integer, primary_key=True)
    dock_code: Mapped[str] = mapped_column(types.String(10), unique=True)
    dock_length: Mapped[int] = mapped_column(types.Integer)
    cargo_type_id: Mapped[int] = mapped_column(ForeignKey('cargo_types.id'), nullable=True)
