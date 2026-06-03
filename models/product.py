#Product related DB Models using SQLAlchemy
from database.session import Base
from sqlalchemy import Column, Integer, DateTime, Text, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key= True)
    name = Column(String(150))
    description = Column(Text)
    category_id = Column(Integer,ForeignKey("categories.id") )
    cateogry = relationship("Category", back_populates="products")
    price = Column(Numeric(10, 2))
    # image = Column
    stock = Column(Integer)
    created_at = Column(DateTime, default= datetime.utcnow)
    updated_at = Column(DateTime, default= datetime.utcnow)


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key= True)
    name = Column(String(80))
    description = Column(Text)
    products = relationship("Product", back_populates= "category")
    created_at = Column(DateTime, default= datetime.utcnow)