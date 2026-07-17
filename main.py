from fastapi import FastAPI, Depends, Path,status, HTTPException
from pydantic import BaseModel
from database.session import Base, engine
from models.product import Category, Product, Review
from models.user import User
from models.order import Cart, CartItem, Order, OrderItem
from api.v1.routes.products import router as product_router
from api.v1.routes.users import router as user_router
from api.v1.routes.orders import router as order_router
from fastapi.middleware.cors import CORSMiddleware

# Review.__table__.drop(engine)
Base.metadata.create_all(bind=engine)  

#THE FastAPI Project -> 
app = FastAPI(
    title= "Remote Shop API",
    description=  "Ecommerce Web Platform built with FastAPI",
    version= "1.0.0",
    # debug=True
)

#CORS Policy as Middleware -> 
app.add_middleware(
    CORSMiddleware, 
    allow_origins = [
        "http://localhost:3000",
    ],
    allow_methods = ["*"],
    allow_headers = ["*"],
    allow_credentials = True #must need for Cookie
)

#Routes from different files
app.include_router(product_router)
app.include_router(user_router)
app.include_router(order_router)

@app.get("/")
def homePage():
    return {"Message" : "This is Homepage to RemoteShop"}



