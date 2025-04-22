from fastapi import APIRouter, status, HTTPException
from sqlmodel import select

from models.reservation_status import ReservationStatus, ReservationStatusCreate, ReservationStatusUpdate
from core.database import SessionDep

router = APIRouter()


# lista de estados de reserva
@router.get("/api/reservationstatus", response_model=list[ReservationStatus], tags=["RESERVATION STATUS"])
async def list_reservation_status(session: SessionDep):
    return session.exec(select(ReservationStatus)).all()# esto ejecuta transacciones de sql


# obtener estado de reserva por id para listar
@router.get("/api/reservationstatus/{reservationstatus_id}", response_model=ReservationStatus, tags=["RESERVATION STATUS"])
async def read_reservation_status(reservationstatus_id: int, session: SessionDep):
    reservationstatus_db = session.get(ReservationStatus, reservationstatus_id)
    if not reservationstatus_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Reservation status doesn't exist"
        )# status.http y el codigo y detail es para el mensaje que retorna
    return reservationstatus_db

# crear estado de reserva
@router.post("/api/reservationstatus", response_model=ReservationStatus, status_code=status.HTTP_201_CREATED, tags=["RESERVATION STATUS"])
async def create_reservation_status(reservation_status_data: ReservationStatusCreate, session: SessionDep):
    reservation_status = ReservationStatus.model_validate(reservation_status_data.model_dump())

    session.add(reservation_status)# insertamos datos
    session.commit()# conectamos la bd
    session.refresh(reservation_status)# refrescamos despues de insertar datos
    return reservation_status



# obtener reservation_status por id para eliminar
@router.delete("/api/reservationstatus/{reservationstatus_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["RESERVATION STATUS"])
async def delete_reservation_status(reservationstatus_id: int, session: SessionDep):
    reservationstatus_db = session.get(ReservationStatus, reservationstatus_id)
    if not reservationstatus_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Reservation status doesn't exist"
        )
    session.delete(reservationstatus_db)
    session.commit()
    return {"detail": "ok"}

# obtener estado de reserva por id para actualizar
@router.patch("/api/reservationstatus/{reservationstatus_id}", response_model=ReservationStatus, tags=["RESERVATION STATUS"])
async def update_reservation_status( reservationstatus_id: int, reservation_status_data: ReservationStatusUpdate, session: SessionDep):
    reservationstatus_db = session.get(ReservationStatus, reservationstatus_id)
    if not reservationstatus_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Reservation status doesn't exist"
        )# status.http y el codigo y detail es para el mensaje que retorna


    reservation_status_data_dict = reservation_status_data.model_dump(exclude_unset=True)# esto evita que se envien datos vacios a la base de datos
    reservationstatus_db.sqlmodel_update(reservation_status_data_dict)
    session.add(reservationstatus_db)
    session.commit()
    session.refresh(reservationstatus_db)
    return reservationstatus_db