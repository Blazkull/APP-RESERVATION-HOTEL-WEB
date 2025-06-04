from datetime import datetime, timedelta, timezone
from typing import TYPE_CHECKING, Optional, List
from sqlmodel import SQLModel, Field, Relationship


class AccessTokenResponse(SQLModel): 
    acces_token: str
    token_type: str
    

class Token(SQLModel, table=True):
    __tablename__ = "token" # Nombre de la tabla en la base de datos

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id") 
    token: str
    status_token: bool = Field(default=True) # True: activo, False: expirado/invalidado
    expiration: datetime # Fecha y hora de expiración del token
    date_token: datetime = Field(default_factory=datetime.now) 
    

    user: Optional["User"] = Relationship(back_populates="tokens") # Relación apuntando al campo 'tokens' en el modelo User


if TYPE_CHECKING:
    from models.user import User