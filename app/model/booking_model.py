from datetime import datetime
from enum import Enum

from sqlalchemy import types, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import ExcludeConstraint
from sqlalchemy import func


from app.db import db

class StatusEnum(Enum):
    PENDING = 'PENDING'
    CONFIRMED = 'CONFIRMED'


class Booking(db.Model):
    """
    Bookings model representing a booking for a ship at a dock.

    Fields:
        id: Primary key, unique identifier for the dock
        booking_start: The date / time of the start of the booking
        booking_end: The date / time of the end of the booking
        booking_status: The current status of the booking, from [PENDING, CONFIRMED]
        ship_id: ID of the ship this booking is for (FK to Ships)
        dock_id: ID of the dock this booking is for (FK to Docks)
    """

    __tablename__ = 'bookings'

    _status_enum = StatusEnum

    id: Mapped[int] = mapped_column(types.Integer, primary_key=True)
    booking_start: Mapped[datetime] = mapped_column(types.DateTime(timezone=True))
    booking_end: Mapped[datetime] = mapped_column(types.DateTime(timezone=True))
    booking_status = mapped_column(types.Enum(StatusEnum))
    ship_id: Mapped[int] = mapped_column(ForeignKey('ships.id'))
    dock_id: Mapped[int] = mapped_column(ForeignKey('docks.id'))

    __table_args__ = (
        ExcludeConstraint(
            ('dock_id', "="),
            (func.tstzrange(booking_start, booking_end, '[]'), "&&"),
            where=("booking_status = 'CONFIRMED'"),
            name='exclude_overlapping_confirmed_bookings_per_dock'
        ),
    )

    #TODO: Add back populates for ship?
    ship: Mapped['Ship'] = relationship()
    dock: Mapped['Dock'] = relationship(back_populates='bookings')