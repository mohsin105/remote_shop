from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
# from core.config import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM
from core.config import settings

pwd_context = CryptContext(schemes= ["argon2"], deprecated = "auto")


def hash_password(password:str)-> str:
    return pwd_context.hash(password)

def verify_password(plain_password:str, hashed_password:str)->bool:
    return pwd_context.verify(plain_password, hashed_password)


#Helper function - Token generation function
def create_access_token(data : dict):   #data is user information. User's username and role
    to_encode = data.copy()
    expiry_limit = datetime.utcnow() + timedelta(minutes= settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp" : expiry_limit})
    encode_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm= settings.ALGORITHM)   #creating jwt token
    return encode_jwt