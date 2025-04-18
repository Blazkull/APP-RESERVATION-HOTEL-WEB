
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    type: str  # "income" o "expense"

    reservations: List["Reservation"] = Relationship(back_populates="category")

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.reservation import Reservation