from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from models import reservations as model
from models import users, room
from pydantic import BaseModel
from typing import List
from datetime import datetime

router = APIRouter(prefix="/reservations", tags=["Reservations"])

#Esquemas Pydantic
class ReservationBase(BaseModel):
    user_id: int
    room_id: int
    start_date: datetime
    end_date: datetime

class ReservationResponse(ReservationBase):
    id: int
    total_amount: float

    class Config:
        orm_mode = True

#Calcula el total según los días y precio de la habitación
def calculate_total_amount(price_per_night: float, start_date: datetime, end_date: datetime) -> float:
    nights = (end_date - start_date).days
    if nights <= 0:
        raise HTTPException(status_code=400, detail="La fecha de fin debe ser posterior a la fecha de inicio")
    return nights * price_per_night

#Verifica conflictos de fechas en una habitación
def check_date_conflict(db: Session, room_id: int, start_date: datetime, end_date: datetime, exclude_reservation_id: int = None):
    query = db.query(model.Reservation).filter(
        model.Reservation.room_id == room_id,
        model.Reservation.start_date < end_date,
        model.Reservation.end_date > start_date
    )
    if exclude_reservation_id:
        query = query.filter(model.Reservation.id != exclude_reservation_id)

    return db.query(query.exists()).scalar()

#Todas las reservas
@router.get("/", response_model=List[ReservationResponse])
def get_all_reservations(db: Session = Depends(get_db)):
    return db.query(model.Reservation).all()

# ➕ POST: Crear nueva reserva
@router.post("/", response_model=ReservationResponse)
def create_reservation(reservation: ReservationBase, db: Session = Depends(get_db)):
    user = db.query(users.User).filter(users.User.id == reservation.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    room_exist = db.query(room.Room).filter(room.Room.id == reservation.room_id).first()
    if not room_exist:
        raise HTTPException(status_code=404, detail="Habitación no encontrada")

    if check_date_conflict(db, reservation.room_id, reservation.start_date, reservation.end_date):
        raise HTTPException(status_code=409, detail="Conflicto de fechas con otra reserva para esta habitación")

    total = calculate_total_amount(room_exist.price, reservation.start_date, reservation.end_date)

    new_reservation = model.Reservation(**reservation.dict(), total_amount=total)
    db.add(new_reservation)
    db.commit()
    db.refresh(new_reservation)
    return new_reservation

#Actualizar reserva existente
@router.put("/{reservation_id}", response_model=ReservationResponse)
def update_reservation(reservation_id: int, updated_data: ReservationBase, db: Session = Depends(get_db)):
    reservation = db.query(model.Reservation).filter(model.Reservation.id == reservation_id).first()
    if not reservation:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")

    user = db.query(users.User).filter(users.User.id == updated_data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    room_exist = db.query(room.Room).filter(room.Room.id == updated_data.room_id).first()
    if not room_exist:
        raise HTTPException(status_code=404, detail="Habitación no encontrada")

    if check_date_conflict(db, updated_data.room_id, updated_data.start_date, updated_data.end_date, exclude_reservation_id=reservation_id):
        raise HTTPException(status_code=409, detail="Conflicto de fechas con otra reserva")

    total = calculate_total_amount(room_exist.price, updated_data.start_date, updated_data.end_date)

    for key, value in updated_data.dict().items():
        setattr(reservation, key, value)
    reservation.total_amount = total

    db.commit()
    db.refresh(reservation)
    return reservation

#Eliminar una reserva
@router.delete("/{reservation_id}")
def delete_reservation(reservation_id: int, db: Session = Depends(get_db)):
    reservation = db.query(model.Reservation).filter(model.Reservation.id == reservation_id).first()
    if not reservation:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")

    db.delete(reservation)
    db.commit()
    return {"message": f"Reserva {reservation_id} eliminada correctamente"}
