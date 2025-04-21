from fastapi import APIRouter, status, HTTPException
from sqlmodel import select

from models.room_status import RoomStatus, RoomStatusCreate, RoomStatusUpdate
from core.database import SessionDep

router = APIRouter()


#lista de tipos de habitacion
@router.get("/api/roomstatus", response_model=list[RoomStatus], tags=["ROOM STATUS"])
async def list_roomstatus(session: SessionDep):
    return session.exec(select(RoomStatus)).all()#esto ejecuta transacciones de sql


# obtener tipo de habitacion por id para listar
@router.get("/api/roomstatus/{roomstatus_id}", response_model=RoomStatus, tags=["ROOM STATUS"])
async def read_roomstatus(roomstatus_id: int, session: SessionDep):
    roomstatus_db = session.get(RoomStatus, roomstatus_id)
    if not roomstatus_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Room status doesn't exits"
        )#status.http y el codigo y detail es para el mensaje que retorna
    return roomstatus_db

#crear tipo de habitacion
@router.post("/api/roomstatus", response_model=RoomStatus,status_code=status.HTTP_201_CREATED,tags=["ROOM STATUS"])
async def create_roomstatus(room_status_data: RoomStatusCreate,session: SessionDep):
    roomtype = RoomStatus.model_validate(room_status_data.model_dump())

    session.add(roomtype)#insertamos datos
    session.commit()#conectamos la bd
    session.refresh(roomtype)#refrescamos despues de insertar datos
    return roomtype



# obtener room_status por id para eliminar
@router.delete("/api/roomstatus/{roomstatus_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["ROOM STATUS"])
async def delete_roomstatus(roomstatus_id: int, session: SessionDep):
    roomstatus_db = session.get(RoomStatus, roomstatus_id)
    if not roomstatus_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Room status doesn't exits"
        )
    session.delete(roomstatus_db)
    session.commit()
    return {"detail": "ok"}

# obtener tipo de habitacion por id para actualizar
@router.patch("/api/roomstatus/{roomstatus_id}", response_model=RoomStatus, tags=["ROOM STATUS"])
async def update_roomstatus( roomstatus_id: int, roomtype_data: RoomStatusUpdate, session: SessionDep):
    roomstatus_db = session.get(RoomStatus, roomstatus_id)
    if not roomstatus_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Room status doesn't exits"
        )#status.http y el codigo y detail es para el mensaje que retorna
    

    roomtype_data_dict=roomtype_data.model_dump(exclude_unset=True)# esto evita que se envien datos vacios a la base de datos
    roomstatus_db.sqlmodel_update(roomtype_data_dict)
    session.add(roomstatus_db)
    session.commit()
    session.refresh(roomstatus_db)
    return roomstatus_db