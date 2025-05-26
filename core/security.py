
from sqlmodel import select
from core.database import SessionDep
from models.user import  User
from typing import Annotated
from fastapi import Depends
from fastapi.security import  OAuth2PasswordBearer
from fastapi.exceptions import HTTPException
import bcrypt

from jose import jwt

from dotenv import load_dotenv
import os

load_dotenv()
SECRET_KEY= os.getenv('SECRET_KEY')
ALGORITHM= os.getenv('ALGORITHM')


#instancia de una clase
outh2_scheme= OAuth2PasswordBearer(tokenUrl="token")

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

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
            raise HTTPException(status_code=403, detail="User  disenable. please, contact your manager system") 
        return

    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


