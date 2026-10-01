#CRUD and Business Logic for User model
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, UploadFile
from core.security import verify_password,create_access_token
from models.user import User
from pathlib import Path
from core.image_utils import set_unique_image_filename
import shutil
from core.config import PROFILE_PICS_DIR

# PROFILE_PICS_DIR = Path("/media/profile_images")
# PROFILE_PICS_DIR.mkdir(parents=True, exist_ok=True)

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

    @staticmethod
    def perform_profile_image_update(current_user,image:UploadFile,db:Session):
        unique_filename = set_unique_image_filename(image.filename)
        filepath = PROFILE_PICS_DIR / unique_filename

        old_filename = current_user.profile_image  # capture before overwriting

        #Read the image file and writing it to the new project file
        with filepath.open("wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

        current_user.profile_image = unique_filename
        db.commit()
        db.refresh(current_user)

        if old_filename:
            old_filepath = PROFILE_PICS_DIR / old_filename
            old_filepath.unlink(missing_ok = True)
        return current_user
