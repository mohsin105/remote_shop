#User related Pydantic Models
from pydantic import BaseModel, Field, EmailStr, computed_field
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
    id:int
    username : Annotated[str, Field(max_length=20)]
    email : EmailStr
    first_name : Annotated[str, Field(max_length=20)]
    last_name : Annotated[str, Field(max_length=20)]
    role :UserRoleEnum
    # image:str

    @computed_field
    @property
    def full_name(self) ->str:
        return f"{self.first_name} {self.last_name}"

class SimpleUserSchema(BaseModel):
    id:int
    username : Annotated[str, Field(max_length=20)]
    first_name : Annotated[str, Field(max_length=20)]
    last_name : Annotated[str, Field(max_length=20)]

class UserLoginSchema(BaseModel):
    username :Annotated[str, Field(max_length= 20)]
    password : str

class UserUpdateSchema(BaseModel):
    first_name :str | None = None
    last_name: str | None = None