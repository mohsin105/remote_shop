#CRUD and Business Logic for User model
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from core.security import verify_password,create_access_token
from models.user import User
class UserService:

    @staticmethod
    def create_new_user():
        pass

    @staticmethod
    def perform_login(payload, db: Session):
        #Check user existence -> 
        existing_user = db.query(User).filter(User.username == payload.username).first()
        if not existing_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="User Does not Exists"
            )
        
        #password verification
        if not verify_password(payload.password, existing_user.hashed_password):
            raise HTTPException(
                status_code= status.HTTP_401_UNAUTHORIZED, detail="Password Do Not Match"
            )
        
        #User Exists and Password Verified; Now Create JWT Access Token -> 
        token_data = {"sub": existing_user.username, "role":existing_user.role}  #this "sub" key is vital
        token = create_access_token(token_data)
        return token

    @staticmethod
    def preform_profile_update(payload,current_user,db:Session):
        update_data = payload.model_dump(exclude_unset=True)
        # print("Clean Update Data of User -> ", update_data)

        for field, value in update_data.items():
            setattr(current_user, field, value)
        
        db.commit()
        db.refresh(current_user)
        return current_user