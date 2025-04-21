from fastapi import APIRouter, status, HTTPException
from sqlmodel import select

from models.room_type import RoomType, RoomTypeCreate, RoomTypeUpdate
from core.database import SessionDep

router = APIRouter()


#lista de tipos de habitacion
@router.get("/api/roomtypes", response_model=list[RoomType], tags=["ROOM TYPES"])
async def list_roomtype(session: SessionDep):
    return session.exec(select(RoomType)).all()#esto ejecuta transacciones de sql


# obtener tipo de habitacion por id para listar
@router.get("/api/roomtypes/{roomtype_id}", response_model=RoomType, tags=["ROOM TYPES"])
async def read_roomtype(roomtype_id: int, session: SessionDep):
    roomtype_db = session.get(RoomType, roomtype_id)
    if not roomtype_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Room type doesn't exits"
        )#status.http y el codigo y detail es para el mensaje que retorna
    return roomtype_db

#crear tipo de habitacion
@router.post("/api/roomtypes", response_model=RoomType,status_code=status.HTTP_201_CREATED,tags=["ROOM TYPES"])
async def create_roomtype(room_types_data: RoomTypeCreate,session: SessionDep):
    roomtype = RoomType.model_validate(room_types_data.model_dump())

    session.add(roomtype)#insertamos datos
    session.commit()#conectamos la bd
    session.refresh(roomtype)#refrescamos despues de insertar datos
    return roomtype



# obtener room_types por id para eliminar
@router.delete("/api/roomtypes/{roomtype_id}",status_code=status.HTTP_204_NO_CONTENT, tags=["ROOM TYPES"])
async def delete_roomtype(roomtype_id: int, session: SessionDep):
    roomtype_db = session.get(RoomType, roomtype_id)
    if not roomtype_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Room type doesn't exits"
        )
    session.delete(roomtype_db)
    session.commit()
    return {"detail": "ok"}

# obtener tipo de habitacion por id para actualizar
@router.patch("/api/roomtypes/{roomtype_id}", response_model=RoomType, tags=["ROOM TYPES"])
async def update_roomtype( roomtype_id: int, roomtype_data: RoomTypeUpdate, session: SessionDep):
    roomtype_db = session.get(RoomType, roomtype_id)
    if not roomtype_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Room type doesn't exits"
        )#status.http y el codigo y detail es para el mensaje que retorna
    

    roomtype_data_dict=roomtype_data.model_dump(exclude_unset=True)# esto evita que se envien datos vacios a la base de datos
    roomtype_db.sqlmodel_update(roomtype_data_dict)
    session.add(roomtype_db)
    session.commit()
    session.refresh(roomtype_db)
    return roomtype_db