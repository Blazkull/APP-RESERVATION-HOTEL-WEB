
from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from core.database import get_session
from models.reservation import Reservation

router = APIRouter(prefix="/transactions", tags=["Reservation"])

@router.post("/")
def create_reservation(reservation: Reservation, session: Session = Depends(get_session)):
    session.add(reservation)
    session.commit()
    session.refresh(reservation)
    return reservation

@router.get("/")
def list_reservation(session: Session = Depends(get_session)):
    return session.exec(select(Reservation)).all()
