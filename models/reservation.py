from decimal import Decimal
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import date

class Reservation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    reservation_status_id:int = Field(foreign_key="reservationstatus.id")
    client_id : int = Field(foreign_key="client.id")
    room_id : int = Field(foreign_key="room.id")
    check_in_date: date
    check_in_out: date
    note: str
    total: Decimal = Field(default=Decimal(0.00))

    user: Optional["User"] = Relationship(back_populates="reservations")
    reservation_statues: Optional["ReservationStatus"] = Relationship(back_populates="reservations") # Cambiado aquí
    client: Optional["Client"] = Relationship(back_populates="reservations")
    room: Optional["Room"] = Relationship(back_populates="reservations")

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.user import User
    from models.reservation_status import ReservationStatus
    from models.client import Client
    from models.room import Room