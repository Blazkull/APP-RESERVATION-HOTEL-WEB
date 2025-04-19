from fastapi import APIRouter, status, HTTPException
from sqlmodel import select

from models.user import User, UserCreate, UserUpdate, UserBase
from core.database import SessionDep

router = APIRouter()


#lista de tipos de usuario
@router.get("/api/user", response_model=list[User], tags=["USER"])
async def list_user(session: SessionDep):
    return session.exec(select(User)).all()#esto ejecuta transacciones de sql


# obtener tipo de usuario por id para listar
@router.get("/api/user/{user_id}", response_model=User, tags=["USER"])
async def read_user(user_id: int, session: SessionDep):
    user_db = session.get(User, user_id)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User doesn't exits"
        )#status.http y el codigo y detail es para el mensaje que retorna
    return user_db

#crear tipo de usuario
@router.post("/api/user", response_model=User, status_code=status.HTTP_201_CREATED ,tags=["USER"])
async def create_user(user_data: UserCreate,session: SessionDep):
    user = User.model_validate(user_data.model_dump())

    session.add(user)#insertamos datos
    session.commit()#conectamos la bd
    session.refresh(user)#refrescamos despues de insertar datos
    return user



# obtener customer por id para eliminar
@router.delete("/api/user/{user_id}", tags=["USER"])
async def delete_user(user_id: int, session: SessionDep):
    user_db = session.get(User, user_id)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User doesn't exits"
        )
    session.delete(user_db)
    session.commit()
    return {"detail": "ok"}

# obtener tipo de usuario por id para actualizar
@router.patch("/api/user/{user_id}", response_model=User, status_code=status.HTTP_201_CREATED, tags=["USER"])
async def update_user( user_id: int, user_data: UserUpdate, session: SessionDep):
    user_db = session.get(User, user_id)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User doesn't exits"
        )#status.http y el codigo y detail es para el mensaje que retorna
    

    user_data_dict=user_data.model_dump(exclude_unset=True)# esto evita que se envien datos vacios a la base de datos
    user_db.sqlmodel_update(user_data_dict)
    session.add(user_db)
    session.commit()
    session.refresh(user_db)
    return user_db