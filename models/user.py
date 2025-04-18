from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from pydantic import EmailStr


class User(SQLModel, table=True):
    __tablename__ = "user"  # Nombre explícito de la tabla

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(max_length=30)
    email: EmailStr = Field(max_length=100)
    password: str = Field(max_length=100)
    user_type_id: int = Field(foreign_key="usertype.id") 

    reservations: List["Reservation"] = Relationship(back_populates="user")
    user_type: Optional["UserType"] = Relationship(back_populates="users")


class UserBase(SQLModel):
    username: str = Field(max_length=30)
    email: EmailStr = Field(max_length=100)

class UserCreate(UserBase):
    password: str = Field(min_length=6, max_length=100)

class UserUpdate(SQLModel):
    username: Optional[str] = Field(default=None, max_length=30)
    email: Optional[EmailStr] = None

class UserRead(UserBase):
    id: int

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.reservation import Reservation
    from models.user_type import UserType