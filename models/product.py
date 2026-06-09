#Product related DB Models using SQLAlchemy
from database.session import Base
from sqlalchemy import Column, Integer, DateTime, Text, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key= True, autoincrement=True)
    name = Column(String(150))
    description = Column(Text)
    category_id = Column(Integer,ForeignKey("categories.id") )
    category = relationship("Category", back_populates="products")
    price = Column(Numeric(10, 2))
    # image = Column
    stock = Column(Integer)
    created_at = Column(DateTime, default= datetime.utcnow)
    updated_at = Column(DateTime, default= datetime.utcnow)


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key= True, autoincrement=True)
    name = Column(String(80))
    description = Column(Text)
    products = relationship("Product", back_populates= "category")
    created_at = Column(DateTime, default= datetime.utcnow)

"""
class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, autoincrement= True)
    product_id = Column(Integer, ForeignKey("products.id"))
    product = relationship("Product", back_populates="reviews")

    user_id = Column(Integer , ForeignKey("users.id"))
    user = relationship("User")

    content = Column(Text)

    created_at = Column(DateTime, default= datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)


"""