from fastapi import APIRouter, status, HTTPException
from sqlmodel import select
from core.database import SessionDep
from core.security import encode_token
from models.user import  User, UserLogin

router = APIRouter()


@router.post("/login", tags=["AUTH"])
def login(user_data:UserLogin,session: SessionDep):
    try:
        user_db = session.exec(select(User).where(User.username == user_data.username)).first()

        if not user_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        if user_data.password != user_db.password:
            raise HTTPException(status_code=400,detail="Invalid credentials")
        token = encode_token({"username":user_data.username,"email": user_db.email})

        return{"acces_token":token, "token_type":"barber"} # retorna el token para guardarlo en algun lado
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during login: {str(e)}",
        )
