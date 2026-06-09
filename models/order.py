##Cart and Order related DB Models using SQLAlchemy

from database.session import Base
from sqlalchemy import Column,Integer, String, Text, DateTime, Numeric, Float, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum
# from models.user import User

class OrderStatusEnum(str, Enum):
    NOT_PAID ='Not Paid'
    READY_TO_SHIP='Ready To Ship'
    SHIPPED ='Shipped'
    DELIVERED='Delivered'
    CANCELED ='Canceled'

class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key= True, autoincrement= True)
    user_id = Column(Integer, ForeignKey("users.id"), unique= True)  #o2o relation
    user = relationship("User", back_populates="cart")
    items = relationship("CartItem", back_populates= "cart", cascade="all, delete-orphan")
    created_at = Column(DateTime, default= datetime.utcnow)
    updated_at = Column(DateTime, default= datetime.utcnow)

class CartItem(Base):
    __tablename__ = "cartitems"

    id = Column(Integer, primary_key= True, autoincrement=True)
    #Relation with Cart Model
    cart_id = Column(Integer, ForeignKey("carts.id"))   #The SQL DB Connection
    cart = relationship("Cart", back_populates="items") #The orm connection

    #Relation with Product Model
    product_id = Column(Integer, ForeignKey("products.id"))  #The SQL DB Connection
    product = relationship("Product")     #The orm connection

    quantity = Column(Integer)

    created_at = Column(DateTime, default= datetime.utcnow)
    updated_at = Column(DateTime, default= datetime.utcnow)


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key= True, autoincrement=True)
    total_price = Column(Numeric(10,2))
    status = Column(SQLEnum(OrderStatusEnum), default= OrderStatusEnum.NOT_PAID)
    items = relationship("OrderItem", back_populates="order")
    
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="orders")
    
    created_at = Column(DateTime, default= datetime.utcnow)
    updated_at = Column(DateTime, default= datetime.utcnow)


class OrderItem(Base):
    __tablename__ = "orderitems"

    id = Column(Integer, primary_key= True, autoincrement= True)

    #Relation with Order Model
    order_id = Column(Integer, ForeignKey("orders.id"))
    order = relationship("Order", back_populates= "items")

    #Relation with Product Model
    product_id = Column(Integer, ForeignKey("products.id"))
    product = relationship("Product")

    quantity = Column(Integer)
    price = Column(Numeric(10,2))
    total_price = Column(Numeric(10,2))

    created_at = Column(DateTime, default= datetime.utcnow)
    updated_at = Column(DateTime, default= datetime.utcnow)

"""
"""
