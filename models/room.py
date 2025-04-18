from decimal import Decimal
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from pydantic import EmailStr
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.reservation import Reservation
    from models.room_type import RoomType
    from models.room_status import RoomStatus

class Room(SQLModel, table=True):
    __tablename__ = "room"  # Nombre explícito de la tabla

    id: Optional[int] = Field(default=None, primary_key=True)
    room_number: str = Field(max_length=30)
    price_per_night: Decimal
    capacity: int = Field(default=1)
    room_type_id: int = Field(foreign_key="roomtype.id") 
    room_status_id: int = Field(foreign_key="roomstatus.id") 

    reservations: List["Reservation"] = Relationship(back_populates="room")
    room: Optional["RoomType"] = Relationship(back_populates="room_type")
    room: Optional["RoomStatus"] = Relationship(back_populates="room_status")

class RoomBase(SQLModel):
    username: str = Field(max_length=30)
    email: EmailStr = Field(max_length=100)

class RoomCreate(RoomBase):
    password: str = Field(min_length=6, max_length=100)

class RoomUpdate(SQLModel):
    username: Optional[str] = Field(default=None, max_length=30)
    email: Optional[EmailStr] = None

class RoomRead(RoomBase):
    id: int
