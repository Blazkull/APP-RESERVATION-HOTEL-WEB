from fastapi import APIRouter, status, HTTPException
from sqlmodel import select

from models.client import Client, ClientCreate, ClientUpdate
from core.database import SessionDep

router = APIRouter()


#lista de tipos de usuario
@router.get("/api/client", response_model=list[Client], tags=["CLIENT"])
async def list_client(session: SessionDep):
    return session.exec(select(Client)).all()#esto ejecuta transacciones de sql


# obtener tipo de usuario por id para listar
@router.get("/api/client/{client_id}", response_model=Client, tags=["CLIENT"])
async def read_client(client_id: int, session: SessionDep):
    client_db = session.get(Client, client_id)
    if not client_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Client doesn't exits"
        )#status.http y el codigo y detail es para el mensaje que retorna
    return client_db

#crear tipo de usuario
@router.post("/api/client", response_model=Client, status_code=status.HTTP_201_CREATED ,tags=["CLIENT"])
async def create_client(client_data: ClientCreate,session: SessionDep):
    client = Client.model_validate(client_data.model_dump())

    session.add(client)#insertamos datos
    session.commit()#conectamos la bd
    session.refresh(client)#refrescamos despues de insertar datos
    return client



# obtener Client por id para eliminar
@router.delete("/api/client/{client_id}",status_code=status.HTTP_204_NO_CONTENT, tags=["CLIENT"])
async def delete_client(client_id: int, session: SessionDep):
    client_db = session.get(Client, client_id)
    if not client_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Client doesn't exits"
        )
    session.delete(client_db)
    session.commit()
    return {"detail": f"client delete id: {client_id}"}

# obtener tipo de usuario por id para actualizar
@router.patch("/api/client/{client_id}", response_model=Client, status_code=status.HTTP_200_OK, tags=["CLIENT"])
async def update_client( client_id: int, client_data: ClientUpdate, session: SessionDep):
    client_db = session.get(Client, client_id)
    if not client_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Client doesn't exits"
        )#status.http y el codigo y detail es para el mensaje que retorna
    

    client_data_dict=client_data.model_dump(exclude_unset=True)# esto evita que se envien datos vacios a la base de datos
    client_db.sqlmodel_update(client_data_dict)
    session.add(client_db)
    session.commit()
    session.refresh(client_db)
    return client_db