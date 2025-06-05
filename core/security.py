from datetime import datetime, timedelta
from sqlmodel import select
from core.database import SessionDep
from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.exceptions import HTTPException
from models.token import Token as DBToken

from jose import JWTError, jwt

from core.config import settings 

from models.user import User


SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM

ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES 

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def encode_token(data:dict):
   
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) 
    return token

def decode_token(token:Annotated[str,Depends(oauth2_scheme)], session: SessionDep):
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = data.get('username')
        if username is None:
            raise HTTPException(status_code=400, detail="The token data is incomplete")

        user_db = session.exec(select(User).where(User.username == username)).first()

        if user_db is None:
            raise HTTPException(status_code=404, detail="User not found")
        if not user_db.active:
            raise HTTPException(status_code=403, detail="User disabled. Please, contact your system manager")
        
        
        return user_db 

    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
