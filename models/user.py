from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from pydantic import EmailStr


class UserBase(SQLModel):
    username: str = Field(max_length=30,unique=True)
    email: EmailStr = Field(max_length=100,unique=True)
    password: str = Field(max_length=100)
    user_type_id: int = Field(foreign_key="usertype.id") 

class User(UserBase, table=True):
    __tablename__ = "user"  # Nombre de tabla

    id: Optional[int] = Field(default=None, primary_key=True)
    active:bool =Field(default=True)
    

    reservations: List["Reservation"] = Relationship(back_populates="user")#reservationf
    user_type: Optional["UserType"] = Relationship(back_populates="users")#tipo de usuario
    tokens: List["Token"] = Relationship(back_populates="user")#token

class UserLogin(SQLModel):
   username: str = Field(max_length=30)
   password: str = Field(max_length=100)

class UserCreate(UserBase):
    password: str = Field(min_length=6, max_length=100)
    active:bool =Field(default=True)

class UserUpdate(SQLModel):
    username: Optional[str] = Field(default=None, max_length=30)
    email: Optional[EmailStr] = None
    password: str = Field(max_length=100)
    user_type_id: int = Field(foreign_key="usertype.id") 
    active: Optional[bool] =Field(default=True)

class UserRead(UserBase):
    id: int


class PasswordUpdate(SQLModel):
    password: str = Field(max_length=100)

class UserStatus(SQLModel):
    active: Optional[bool] = Field(default=True)
   
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.reservation import Reservation
    from models.user_type import UserType
    from models.token import Token