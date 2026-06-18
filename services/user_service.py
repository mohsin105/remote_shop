#CRUD and Business Logic for User model
from sqlalchemy.orm import Session

class UserService:

    @staticmethod
    def create_new_user():
        pass

    @staticmethod
    def perform_login():
        pass

    @staticmethod
    def preform_profile_update(payload,current_user,db:Session):
        update_data = payload.model_dump(exclude_unset=True)
        # print("Clean Update Data of User -> ", update_data)

        for field, value in update_data.items():
            setattr(current_user, field, value)
        
        db.commit()
        db.refresh(current_user)
        return current_user