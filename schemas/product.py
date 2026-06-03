#Product related Pydantic Models
"""
from pydantic import BaseModel

class Product(BaseModel):
    id: int
    name :str
    description : str
    category_id :int
    price : float
    stock: int


class CreateProduct(BaseModel):
    name :str
    description : str
    category_id :int
    price : float
    stock: int

class Category(BaseModel):
    pass

class CreateCategory(BaseModel):
    id: int
    name :str
    description : str

"""