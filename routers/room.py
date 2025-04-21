from typing import List
from fastapi import APIRouter, Query, status, HTTPException
from sqlmodel import select

from models.room import Room, RoomCreate, RoomUpdate
from core.database import SessionDep

router = APIRouter()


#lista de tipos de room
@router.get("/api/room", response_model=List[Room], tags=["ROOM"])
async def list_room(
    session: SessionDep,
    #paginacion
    page: int = Query(1, ge=1, description="Número de página a obtener"),
    limit: int = Query(10, ge=1, le=100, description="Cantidad de items por página"),
    ):
    offset = (page - 1) * limit
    rooms = session.exec(select(Room).offset(offset).limit(limit)).all()
    return rooms


# obtener tipo de room por id para listar
@router.get("/api/room/{room_id}", response_model=Room, tags=["ROOM"])
async def read_room(room_id: int, session: SessionDep):
    room_db = session.get(Room, room_id)
    if not room_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Room doesn't exits"
        )#status.http y el codigo y detail es para el mensaje que retorna
    return room_db

#crear tipo de room
@router.post("/api/room", response_model=Room, status_code=status.HTTP_201_CREATED ,tags=["ROOM"])
async def create_room(room_data: RoomCreate,session: SessionDep):
    room = Room.model_validate(room_data.model_dump())

    session.add(room)#insertamos datos
    session.commit()#conectamos la bd
    session.refresh(room)#refrescamos despues de insertar datos
    return room



# obtener Room por id para eliminar
@router.delete("/api/room/{room_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["ROOM"])
async def delete_room(room_id: int, session: SessionDep):
    room_db = session.get(Room, room_id)
    if not room_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Room doesn't exits"
        )
    session.delete(room_db)
    session.commit()
    return {"detail": "ok"}

# obtener tipo de room por id para actualizar
@router.patch("/api/room/{room_id}", response_model=Room, status_code=status.HTTP_200_OK, tags=["ROOM"])
async def update_room( room_id: int, room_data: RoomUpdate, session: SessionDep):
    room_db = session.get(Room, room_id)
    if not room_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Room doesn't exits"
        )#status.http y el codigo y detail es para el mensaje que retorna


    room_data_dict=room_data.model_dump(exclude_unset=True)# esto evita que se envien datos vacios a la base de datos
    room_db.sqlmodel_update(room_data_dict)
    session.add(room_db)
    session.commit()
    session.refresh(room_db)
    return room_db