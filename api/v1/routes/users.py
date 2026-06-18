#User related Endpoint handler functions
from database.session import get_db
from fastapi import Depends, HTTPException, status, APIRouter
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.orm import Session
from schemas.user import UserCreateSchema, UserLoginSchema, UserSchema
from models.user import User
from core.security import hash_password, verify_password, create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from core.dependencies import get_current_user, require_roles
from services.user_service import UserService


router = APIRouter(
    tags=["Users"]
)

@router.post("/signup", response_model=UserSchema)
def register_user(user: UserCreateSchema, db:Session = Depends(get_db) ):
    #Check Existence -> 
    exisiting_user = db.query(User).filter(User.username == user.username).first()
    if exisiting_user:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST, 
            detail="User already exists with this username"
        )

    #Password Hasing -> 
    hashed_password = hash_password(user.password)

    #Finally : Create New User Object -> 
    new_user =User(
        username = user.username,
        email = user.email,
        first_name = user.first_name,
        last_name = user.last_name,
        role = user.role,
        hashed_password = hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return user

@router.post("/login")
def login_user(payload: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    #Check user existence -> 
    existing_user = db.query(User).filter(User.username == payload.username).first()
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User Does not Exists")
    
    #password verification
    if not verify_password(payload.password, existing_user.hashed_password):
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail="Password Do Not Match")
    

    #User Exists and Password Verified; Now Create JWT Access Token -> 
    token_data = {"sub": existing_user.username, "role":existing_user.role}  #this "sub" key is vital
    token = create_access_token(token_data)

    return {"access_token":token, "token_type": "bearer"}


@router.get("/protected")
def protected_route(current_user : dict = Depends(require_roles(["user", "admin"]))):
    # print("Current User: -> ",current_user)
    return {"message": f"Hellow, {current_user.get("username")} | You accessed a protected route"}

@router.get("/profile")
def user_profile(current_user:dict = Depends(require_roles(["user"]))):  #require_role will fetch current user, check role, and if passed,  return the user as dicttionary
    return {"message": f"Profile of {current_user.get("username")} role  - {current_user.get("role")}"}

@router.get("/user-dashboard")
def user_dashboard(current_user : dict = Depends(require_roles(["user"]))):
    return {"message": f"Welcome {current_user.get("username")} to User Dashboard , as your role is {current_user.get("role")}"}


@router.get("/admin-dashboard")
def admin_dashboard(current_user: dict = Depends(require_roles(["admin"]))):
    return {"message": f"Welcome {current_user.get("username")} to Admin Dashboard, as your role is {current_user.get("role")} "}



@router.patch("/profile/update")
def update_profile():
    pass

@router.patch("/profile/password-change")
def change_password():
    pass
