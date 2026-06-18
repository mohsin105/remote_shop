from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
# from core.config import SECRET_KEY, ALGORITHM
from core.config import settings
from sqlalchemy.orm import Session
from sqlalchemy import select
from database.session import get_db
from models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_token_payload(token : str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="Unauthorized", 
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(token ,settings.SECRET_KEY,algorithms=settings.ALGORITHM) #decode the token and extract values encrypted inside it.
        username :str = payload.get("sub")
        role : str = payload.get("role")
        if username is None or role is None:
            raise credential_exception
        
    except JWTError:
        raise credential_exception
    
    return {"username":username ,"role":role}


def get_current_user(payload:dict = Depends(get_token_payload), db:Session = Depends(get_db)):
    username = payload.get("username")
    userstmt = select(User).where(User.username == username)
    userObj = db.execute(userstmt).scalars().first()
    return userObj

#Role Checker -> 
def require_roles(allowed_roles: list[str]):
    def role_checker(current_user:dict = Depends(get_token_payload)):
        user_role = current_user.get("role")
        if user_role not in allowed_roles:
            raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail="Access Denied, Role does not match")
        
        return current_user
    return role_checker