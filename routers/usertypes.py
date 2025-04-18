from fastapi import APIRouter, status, HTTPException
from sqlmodel import select

from models.user_type import UserType, UserTypeCreate, UserTypeUpdate
from core.database import SessionDep

router = APIRouter()


#lista de tipos de usuario
@router.get("/api/usertypes", response_model=list[UserType], tags=["USER TYPES"])
async def list_usertype(session: SessionDep):
    return session.exec(select(UserType)).all()#esto ejecuta transacciones de sql


# obtener tipo de usuario por id para listar
@router.get("/api/usertypes/{usertype_id}", response_model=UserType, tags=["USER TYPES"])
async def read_usertype(usertype_id: int, session: SessionDep):
    usertype_db = session.get(UserType, usertype_id)
    if not usertype_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User Type doesn't exits"
        )#status.http y el codigo y detail es para el mensaje que retorna
    return usertype_db

#crear tipo de usuario
@router.post("/api/usertypes", response_model=UserType, tags=["USER TYPES"])
async def create_usertype(customer_data: UserTypeCreate,session: SessionDep):
    usertype = UserType.model_validate(customer_data.model_dump())

    session.add(usertype)#insertamos datos
    session.commit()#conectamos la bd
    session.refresh(usertype)#refrescamos despues de insertar datos
    return usertype



# obtener customer por id para eliminar
@router.delete("/api/usertypes/{usertype_id}", tags=["USER TYPES"])
async def delete_usertype(customer_id: int, session: SessionDep):
    usertype_db = session.get(UserType, customer_id)
    if not usertype_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User Type doesn't exits"
        )
    session.delete(usertype_db)
    session.commit()
    return {"detail": "ok"}

# obtener tipo de usuario por id para actualizar
@router.patch("/api/usertypes/{usertype_id}", response_model=UserType, status_code=status.HTTP_201_CREATED, tags=["USER TYPES"])
async def update_usertype( usertype_id: int, usertype_data: UserTypeUpdate, session: SessionDep):
    usertype_db = session.get(UserType, usertype_id)
    if not usertype_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer doesn't exits"
        )#status.http y el codigo y detail es para el mensaje que retorna
    

    usertype_data_dict=usertype_data.model_dump(exclude_unset=True)# esto evita que se envien datos vacios a la base de datos
    usertype_db.sqlmodel_update(usertype_data_dict)
    session.add(usertype_db)
    session.commit()
    session.refresh(usertype_db)
    return usertype_db