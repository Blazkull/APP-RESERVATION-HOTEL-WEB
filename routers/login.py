from fastapi import APIRouter, status, HTTPException
from sqlmodel import select
from core.database import SessionDep
from core.security import encode_token, verify_password
from models.user import  User, UserLogin
from core.security import verify_password

router = APIRouter()


@router.post("/login", tags=["AUTH"])
 user_db = session.exec(select(User).where(User.username == user_data.username)).first()
        if not user_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        if not verify_password(user_data.password, user_db.password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials")

    token_str = encode_token({"username": user_db.username, "email": user_db.email})

    # Guardar token en la tabla Token
    new_token = Token(user_id=user_db.id, token=token_str)
    session.add(new_token)
    session.commit()

    return {"access_token": token_str, "token_type": "bearer"}

        if not user_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
       except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during login: {str(e)}",
        )

