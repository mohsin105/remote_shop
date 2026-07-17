#User related Endpoint handler functions
from database.session import get_db
from fastapi import Depends, HTTPException, status, APIRouter, Request, Response
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.orm import Session
from schemas.user import UserCreateSchema, UserLoginSchema, UserSchema, UserUpdateSchema
from models.user import User
from core.security import hash_password, verify_password, create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from core.dependencies import get_current_user, require_roles
from services.user_service import UserService
from fastapi.responses import JSONResponse

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
def login_user(payload: UserLoginSchema,response:Response, db: Session = Depends(get_db)):
    token = UserService.perform_login(payload, db=db)

    # response = JSONResponse({
    #     "message":"Login Successfull. Cookie sent"
    # })

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=False, #True only for https, not http
        samesite="lax",  #samsite lax and secure false is the combo for local testing
        # samesite="none",  #none requires secure true
    )

    # return response
    return {"message":"Login Successfull. Cookie sent"}

    # return {"access_token":token, "token_type": "bearer"}

#Just a protected Route
@router.get("/protected")
def protected_route(current_user : dict = Depends(require_roles(["user", "admin"]))):
    # print("Current User: -> ",current_user)
    return {"message": f"Hellow, {current_user.get("username")} | You accessed a protected route"}

@router.get("/profile", response_model= UserSchema)
def user_profile(current_user = Depends(get_current_user)):  
    
    return current_user

@router.post("/logout")
def logout_user(response : Response):
    response.delete_cookie("access_token")
    return {"message":"User Logged Out"}

@router.get("/user-dashboard")
def user_dashboard(current_user : dict = Depends(require_roles(["user"]))):
    return {"message": f"Welcome {current_user.get("username")} to User Dashboard , as your role is {current_user.get("role")}"}


@router.get("/admin-dashboard")
def admin_dashboard(current_user: dict = Depends(require_roles(["admin"]))):
    return {"message": f"Welcome {current_user.get("username")} to Admin Dashboard, as your role is {current_user.get("role")} "}



@router.patch("/profile/update", response_model=UserSchema)
def update_profile(
    payload : UserUpdateSchema,
    current_user = Depends(get_current_user),  #User Object will be based on token. Not id/email. 
    db : Session = Depends(get_db)
 ):
    updated_user = UserService.preform_profile_update(payload, current_user, db)
    return updated_user

@router.patch("/profile/password-change")
def change_password():
    pass
