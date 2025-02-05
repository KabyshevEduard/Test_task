from fastapi import HTTPException, status
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import os
from datetime import datetime, timezone
load_dotenv(os.chdir('../'))


ALG = os.getenv('ALG')
SECRET_KEY = os.getenv('SECRET_KEY')
ALG_SGNT = os.getenv('ALG_SGNT')

def create_access_token(data):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=366)
    to_encode.update({'exp': expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, ALG)
    return encode_jwt


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    data_to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=30)
    data_to_encode.update({'exp': expire})
    encode_jwt = jwt.encode(data_to_encode, SECRET_KEY, ALG)
    return encode_jwt


def check_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, ALG)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Wrong token or time is gone')
    
    user_id = payload.get('sub')
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Sub user id is not found')
    
    return int(user_id)


sgnt_context = CryptContext(schemes=[ALG_SGNT], deprecated='auto')

def get_signature(strng):
    return sgnt_context.hash(strng) 

def check_signature(sgnt, hash_sgnt):
    return sgnt_context.verify(sgnt, hash_sgnt)

