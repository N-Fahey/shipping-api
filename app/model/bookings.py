from datetime import datetime

from sqlalchemy import types, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db import db

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
    id: Mapped[int] = mapped_column(types.Integer, primary_key=True)
    booking_start: Mapped[datetime] = mapped_column(types.DateTime(timezone=True))
    booking_end: Mapped[datetime] = mapped_column(types.DateTime(timezone=True))
    booking_status: Mapped[str] = mapped_column(types.Enum('PENDING', 'CONFIRMED', name='booking_status_enum'))
    ship_id: Mapped[int] = mapped_column(ForeignKey('ships.id'))
    dock_id: Mapped[int] = mapped_column(ForeignKey('docks.id'))
