from datetime import datetime

from sqlalchemy import types, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db import db

class Booking(db.Model):
    """
    Bookings model representing a booking for a ship at a dock.

    Fields:
        id: Primary key, unique identifier for the dock
        booking_datetime: The time at the start of the booking
        booking_hours: Duration of the booking in hours
        booking_status: The current status of the booking, from [PENDING, CONFIRMED]
        ship_id: ID of the ship this booking is for (FK to Ships)
        dock_id: ID of the dock this booking is for (FK to Docks)
    """

    __tablename__ = 'bookings'
    id: Mapped[int] = mapped_column(types.Integer, primary_key=True)
    booking_datetime: Mapped[datetime] = mapped_column(types.DateTime(timezone=True))
    booking_hours: Mapped[float] = mapped_column(types.Float)
    booking_status: Mapped[str] = mapped_column(types.Enum('PENDING', 'CONFIRMED', name='booking_status_enum'))
    ship_id: Mapped[int] = mapped_column(ForeignKey('ships.id'))
    dock_id: Mapped[int] = mapped_column(ForeignKey('docks.id'))
