from fastapi import APIRouter, status, HTTPException
from sqlmodel import select
from core.database import SessionDep
from core.security import encode_token
from models.user import  User, UserLogin
from core.security import verify_password

router = APIRouter()


@router.post("/login", tags=["AUTH"])
def login(user_data:UserLogin,session: SessionDep):
    try:
        token = encode_token({"username": user_data.username, "email": user_db.email})

        user_db.last_token = token 
        session.add(user_db)
        session.commit()

        return {"acces_token": token, "token_type": "barber"}


        if not user_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        if not verify_password(user_data.password, user_db.password):
            raise HTTPException(status_code=400,detail="Invalid credentials")
        token = encode_token({"username":user_data.username,"email": user_db.email})

        return{"acces_token":token, "token_type":"barber"} # retorna el token para guardarlo en algun lado
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during login: {str(e)}",
        )
