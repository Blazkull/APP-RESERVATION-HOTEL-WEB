from fastapi import APIRouter, status, HTTPException, Query
from sqlmodel import Session, select
from typing import List, Optional
from decimal import Decimal
from datetime import date

from core.database import SessionDep
from models.room import Room  # Asegúrate de que este modelo exista
from models.reservation import Reservation, ReservationCreate, ReservationRead, ReservationUpdate

router = APIRouter()

def calculate_total_reservation(session: SessionDep, reservation: Reservation) -> Decimal:
    """Calcula el total de la reserva basado en las fechas y el precio por noche de la habitación."""
    room = session.exec(select(Room).where(Room.id == reservation.room_id)).first()
    if room:
        duration = reservation.check_out_date - reservation.check_in_date
        total = room.price_per_night * Decimal(duration.days)
        return total
    return Decimal(0.00)

# POST para crear una nueva reserva
@router.post("/reservations/", response_model=ReservationRead, status_code=status.HTTP_201_CREATED, tags=["RESERVATION"])
def create_reservation(reservation: ReservationCreate, session: SessionDep):
    db_reservation = Reservation.model_validate(reservation.model_dump())
    db_reservation.total = calculate_total_reservation(session, db_reservation)
    session.add(db_reservation)
    session.commit()
    session.refresh(db_reservation)
    return db_reservation

# GET para obtener una reserva por su ID
@router.get("/reservations/{reservation_id}", response_model=ReservationRead, status_code=status.HTTP_200_OK, tags=["RESERVATION"])
def read_reservation(reservation_id: int, session: SessionDep):
    db_reservation = session.get(Reservation, reservation_id)
    if db_reservation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reservation not found")
    return db_reservation

# GET para obtener todas las reservas (con paginación opcional)
@router.get("/reservations/", response_model=List[ReservationRead], status_code=status.HTTP_200_OK, tags=["RESERVATION"])
def read_all_reservations(
    session: SessionDep,
    page: Optional[int] = Query(1, ge=1, description="Número de página a obtener"),
    limit: Optional[int] = Query(10, ge=1, le=100, description="Cantidad de items por página"),
):
    query = select(Reservation)
    if page is not None and limit is not None:
        offset = (page - 1) * limit
        reservations = session.exec(query.offset(offset).limit(limit)).all()
    else:
        reservations = session.exec(query).all()
    return reservations

# PUT para actualizar una reserva existente (usando PATCH semánticamente más correcto para actualizaciones parciales)
@router.patch("/reservations/{reservation_id}", response_model=ReservationRead, status_code=status.HTTP_200_OK, tags=["RESERVATION"])
def update_reservation(reservation_id: int, reservation: ReservationUpdate, session: SessionDep):
    db_reservation = session.get(Reservation, reservation_id)
    if db_reservation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reservation not found")

    reservation_data = reservation.model_dump(exclude_unset=True)
    for key, value in reservation_data.items():
        setattr(db_reservation, key, value)

    db_reservation.total = calculate_total_reservation(session, db_reservation) # Recalcular el total si las fechas o la habitación cambian
    session.add(db_reservation)
    session.commit()
    session.refresh(db_reservation)
    return db_reservation

# DELETE para eliminar una reserva
@router.delete("/reservations/{reservation_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["RESERVATION"])
def delete_reservation(reservation_id: int, session: SessionDep):
    db_reservation = session.get(Reservation, reservation_id)
    if db_reservation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reservation not found")
    session.delete(db_reservation)
    session.commit()
    return  # No se devuelve contenido con HTTP 204