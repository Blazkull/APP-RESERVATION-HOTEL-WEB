from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import ValidationError
from sqlmodel import select

from core.security import decode_token, hash_password, verify_password
from models.user import PasswordUpdate, User, UserCreate, UserUpdate, UserBase, UserStatus
from core.database import SessionDep

router = APIRouter()


#lista de tipos de usuario
@router.get("/api/user", response_model=list[User], tags=["USER"],dependencies=[(Depends(decode_token))])
def list_user(session: SessionDep):
    try:
        return session.exec(select(User)).all()#esto ejecuta transacciones de sql
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"this list usertype doesn´t: {str(e)}",
        )


# obtener tipo de usuario por id para listar
@router.get("/api/user/{user_id}", response_model=User, tags=["USER"],dependencies=[(Depends(decode_token))])
def read_user(user_id: int, session: SessionDep):
    try:
        user_db = session.get(User, user_id)
        if not user_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User doesn't exits"
            )#status.http y el codigo y detail es para el mensaje que retorna
        return user_db
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"this list usertype doesn´t: {str(e)}",
        )

#crear  usuario
@router.post("/api/user", response_model=User, status_code=status.HTTP_201_CREATED ,tags=["USER"],dependencies=[(Depends(decode_token))])
def create_user(user_data: UserCreate,session: SessionDep):

    try:
        #validador de longitud de contraseña
        if len(user_data.password) < 6:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="The password must be at least 6 characters."
            )
        
        # Validar y hashear la contraseña
        hashed_password = hash_password(user_data.password)
        
        user_data_dict = user_data.model_dump()
        user_data_dict["password"] = hashed_password
        
        
        user = User.model_validate(user_data_dict) 

        # Validaciones de existencia de username y email
        existing_user = session.exec(select(User).where(User.username == user.username)).first()
        if existing_user:
            raise HTTPException(
               status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered" 
            )
        
        existing_email = session.exec(select(User).where(User.email == user.email)).first()
        if existing_email:
            raise HTTPException(
               status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered" 
            )
        
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

    except HTTPException as http_exc:
        raise http_exc
    except ValidationError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid input data: {str(ve)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while creating user: {str(e)}",
        )

    

# obtener tipo de usuario por id para actualizar
@router.patch("/api/user/{user_id}", response_model=User, status_code=status.HTTP_200_OK, tags=["USER"],dependencies=[(Depends(decode_token))])
def update_user( user_id: int, user_data: UserUpdate, session: SessionDep):

    try:
        user_db = session.get(User, user_id)

        if not user_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User doesn't exits"
            )
        user_data_dict=user_data.model_dump(exclude_unset=True)

        #validador de username
        if "username" in user_data_dict and user_data_dict["username"] != user_db.username:
            existing_user = session.exec(select(User).where(User.username == user_data_dict["username"])).first() # Cambiado de email a username
            if existing_user and existing_user.id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail="User already registered"
                )
            
        #validador de email
        if "email" in user_data_dict and user_data_dict["email"] != user_db.email:
            existing_email = session.exec(select(User).where(User.email == user_data_dict["email"])).first()
            if existing_email and existing_email.id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
                )
        
        # Hashear la nueva contraseña si se proporciona
        if "password" in user_data_dict and user_data_dict["password"] is not None:
            # Validar longitud de la contraseña antes de hashear
            if len(user_data_dict["password"]) < 6:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail="The password must be at least 6 characters."
                )
            user_data_dict["password"] = hash_password(user_data_dict["password"])

        user_db.sqlmodel_update(user_data_dict)
        session.add(user_db)
        session.commit()
        session.refresh(user_db)
        return user_db    
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid input data: {str(ve)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while updating user: {str(e)}",
        )


#actualizar estado de usuario
@router.patch("/api/user/{user_id}/status", response_model=dict, status_code=status.HTTP_200_OK, tags=["USER"],dependencies=[(Depends(decode_token))])
def update_user_status(user_id: int, status_update: UserStatus, session: SessionDep):
    try:
        user_db = session.get(User, user_id)
        if not user_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User doesn't exist"
            )

        # Evita actualizar si el estado no ha cambiado
        if status_update.active == user_db.active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="New status is the same as the current one"
            )

        user_db.active = status_update.active      
        session.add(user_db)
        session.commit()
        session.refresh(user_db)

        return {"message": f"User '{user_db.username}' has successfully updated their status to: {user_db.active}"}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while updating status: {str(e)}",
        )

#actualizar la contraseña

@router.patch("/api/user/{user_id}/password", response_model=dict, status_code=status.HTTP_200_OK, tags=["USER"],dependencies=[(Depends(decode_token))])
def update_user_password(user_id: int, password_update: PasswordUpdate, session: SessionDep):
    try:
        user_db = session.get(User, user_id)
        if not user_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User doesn't exist"
            )
        
        # Verificar la longitud de la nueva contraseña
        if len(password_update.password) < 6:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="The password must be at least 6 characters."
            )

        # Verificar si la nueva contraseña es igual a la actual (hasheada)
        if verify_password(password_update.password, user_db.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="New password cannot be the same as the old password."
            )

        user_db.password = hash_password(password_update.password) # Hashear la nueva contraseña
        session.add(user_db)
        session.commit()
        return {"message": f"User '{user_db.username}' has successfully updated their password"}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while updating password: {str(e)}",
        )