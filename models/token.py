from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

class Token(SQLModel, table=True):
    __tablename__ = "token"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    token: str = Field(max_length=500)
    status: str = Field(default="active", max_length=20)  # active, revoked, expired
    issued_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = None
