#The Database Settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase


SQLALCHEMY_DATABASE_URL = "sqlite:///./remote_shop.db"

#The Actual Connection to DB
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args= {"check_same_thread":False}
)

#Creating DB session
SessionLocal = sessionmaker(
    autoflush= False,
    autocommit = False,
    bind= engine
)


#Passing DB session to router(endpoint handler functions)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#Base  -- All sqlalchemy models will be inherited from here
class Base(DeclarativeBase):
    pass
