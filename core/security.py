# D:\APP-RESERVATION-HOTEL-WEB\core\security.py

from sqlmodel import select
from core.database import SessionDep
from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.exceptions import HTTPException

from jose import jwt

# --- INICIO DE LA MODIFICACIÓN ---
# Elimina estas dos líneas:
# from dotenv import load_dotenv
# import os

# Importa tus settings directamente desde core.config
from core.config import settings
from models.user import User
# --- FIN DE LA MODIFICACIÓN ---


# Ahora usa settings.SECRET_KEY y settings.ALGORITHM
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM


#instancia de una clase
outh2_scheme= OAuth2PasswordBearer(tokenUrl="token")

def encode_token(data:dict):
    token = jwt.encode(data,SECRET_KEY,algorithm=ALGORITHM)
    return token 

def decode_token(token:Annotated[str,Depends(outh2_scheme)], session: SessionDep):
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = data.get('username')
        if username is None:
            raise HTTPException(status_code=400, detail="The token data is incomplete")

        user_db = session.exec(select(User).where(User.username == username)).first()

        if user_db is None:
            raise HTTPException(status_code=404, detail="user not found")
        if not user_db.active:
            raise HTTPException(status_code=403, detail="User  disenable. please, contact your manager system") 
        return

    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")