#User related Pydantic Models
from pydantic import BaseModel, Field, EmailStr
from typing import Annotated
from datetime import datetime
from models.user import UserRoleEnum

class UserCreateSchema(BaseModel):
    username : Annotated[str, Field(max_length=20)]
    email : EmailStr
    first_name : Annotated[str, Field(max_length=20)]
    last_name : Annotated[str, Field(max_length=20)]
    role :UserRoleEnum
    password :str

class UserSchema(BaseModel):
    username : Annotated[str, Field(max_length=20)]
    email : EmailStr
    first_name : Annotated[str, Field(max_length=20)]
    last_name : Annotated[str, Field(max_length=20)]
    role :UserRoleEnum

class UserLoginSchema(BaseModel):
    username :Annotated[str, Field(max_length= 20)]
    password : str