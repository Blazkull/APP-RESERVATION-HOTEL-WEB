from fastapi import APIRouter, status, HTTPException
from sqlmodel import select
from core.database import SessionDep
from fastapi.responses import JSONResponse
from models.user import User

router = APIRouter()

@router.post("/api/login", response_model=User, tags=["AUTH"])
def login(login_data: User, session: SessionDep):
    try:
        user_db = session.exec(select(User).where(User.username == login_data.username)).first()

        if not user_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        if user_db.password != login_data.password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect password",
            )
        return JSONResponse(
            status_code=status.HTTP_202_ACCEPTED,
            content={
                "message": f"Bienvenido, {user_db.username}!",
                "username": user_db.username
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during login: {str(e)}",
        )