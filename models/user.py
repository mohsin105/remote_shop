#User related DB Models using SQLAlchemy
from database.session import Base
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum


class UserRoleEnum(str, Enum):
    USER = "user"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key= True, autoincrement= True)
    username = Column(String(20), unique=True)
    email = Column(String(50), unique= True)
    
    first_name = Column(String(20))
    last_name = Column(String(20))
    address = Column(Text, nullable= True)
    phone_number = Column(String(21), nullable= True)

    hashed_password = Column(String(255))
    role = Column(SQLEnum(UserRoleEnum), default= UserRoleEnum.USER)

    created_at = Column(DateTime, default= datetime.utcnow)
    updated_at = Column(DateTime, default=  datetime.utcnow)
