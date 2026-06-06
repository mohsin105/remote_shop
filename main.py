from fastapi import FastAPI, Depends, Path,status, HTTPException
from pydantic import BaseModel
from database.session import Base, engine
from models.product import Category, Product
from models.user import User
from api.v1.routes.products import router as product_router
from api.v1.routes.users import router as user_router

Base.metadata.create_all(bind=engine)   
app = FastAPI()
app.include_router(product_router)
app.include_router(user_router)

@app.get("/")
def homePage():
    return {"Message" : "This is Homepage to RemoteShop"}



