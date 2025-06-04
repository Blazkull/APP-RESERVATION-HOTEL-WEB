
from datetime import datetime, timedelta
from sqlmodel import select
from core.database import SessionDep
from models.user import  User
from typing import Annotated
from fastapi import Depends
from fastapi.security import  OAuth2PasswordBearer
from fastapi.exceptions import HTTPException
from models.token import Token as DBToken

from jose import JWTError, jwt

from dotenv import load_dotenv
import os

load_dotenv()
SECRET_KEY= os.getenv('SECRET_KEY')
ALGORITHM= os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')
#instancia de una clase
outh2_scheme= OAuth2PasswordBearer(tokenUrl="token")

def encode_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token, expire # Retorna el token, la fecha de expiración y fecha de creacion
    
def decode_token(token: Annotated[str, Depends(outh2_scheme)], session: SessionDep):
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = data.get('username')
        if username is None:
            raise HTTPException(status_code=400, detail="The token data is incomplete")
        
        user_db = session.exec(select(User).where(User.username == username)).first()
        
        if user_db is None:
            raise HTTPException(status_code=404, detail="user not found")
        if not user_db.active:
            raise HTTPException(status_code=403, detail="User disabled. Please, contact your system manager") 
        
        #Comprobar si el token está activo en la base de datos
        db_token = session.exec(
            select(DBToken)
            .where(DBToken.token == token, DBToken.user_id == user_db.id, DBToken.status_token == True)
        ).first()

        if not db_token:
            raise HTTPException(status_code=401, detail="Token has been invalidated or not found in database.")
        
        return user_db # Retornar el usuario si el token es válido y activo

    except JWTError: #recoleccion de errores especificos
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        # Captura cualquier otra excepción inesperada
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

