#Product related Pydantic Models

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Annotated

class SimpleCategorySchema(BaseModel):
    id: int
    name: str
    description :str
    
class ProductSchema(BaseModel):
    id: int
    name :str
    description : str
    category_id :int
    price : float
    stock: int
    category :SimpleCategorySchema
    created_at : datetime
    updated_at : datetime



class CreateProductSchema(BaseModel):
    name :str
    description : str
    category_id :int
    price : Annotated[float, Field(gt=0)]
    stock: Annotated[int, Field(ge= 1)]

class UpdateProductSchema(BaseModel):
    name : str | None = None
    description : str | None = None
    category_id :int | None = None
    price : Annotated[float | None, Field(gt=0)] = None
    stock: Annotated[int | None, Field(ge= 1)] = None

class CategorySchema(BaseModel):
    id: int
    name: str
    description :str
    created_at :datetime




class CreateCategorySchema(BaseModel):
    name :Annotated[str, Field(max_length= 80)]
    description : str

"""
"""