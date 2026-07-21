#Cart and Order related Pydantic Models
from pydantic import BaseModel, Field, ConfigDict , computed_field
from datetime import datetime
from schemas.product import SimpleProductSchema
from schemas.user import SimpleUserSchema
from typing import Annotated
from models.order import OrderStatusEnum
from decimal import Decimal


class CartItemSchema(BaseModel):
    #To display the CartItem with the Cart
    model_config = ConfigDict(
        from_attributes= True
    )

    id: int
    cart_id : int
    product_id : int
    product : SimpleProductSchema
    quantity : Annotated[int, Field(ge=1)]
    created_at : datetime
    updated_at : datetime

    @computed_field
    @property
    def total_price(self)->float:
        return self.product.price * self.quantity

class CartSchema(BaseModel):
    #To display the Cart
    model_config = ConfigDict(
        from_attributes= True
    )

    id:int
    user_id: int
    # total_price : Annotated[Decimal, Field(max_digits=10, decimal_places=2)] = 0.00
    user: SimpleUserSchema
    items : list[CartItemSchema] = []
    created_at : datetime
    updated_at : datetime

    @computed_field
    @property
    def total_price(self)->float:
        sum = 0
        for item in self.items:
            sum += item.product.price * item.quantity
        return sum



class CreateCartSchema(BaseModel):
    #Not Needed. Auto Created in Backend. 
    pass



class CreateCartItemSchema(BaseModel):
    # cart_id: int
    product_id:int
    quantity : Annotated[int, Field(ge=1)]

class UpdateCartItemSchema(BaseModel):
    quantity : Annotated[int, Field(ge=1)]

class OrderItemSchema(BaseModel):
    #To display the OrderItem with the Order
    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    order_id : int
    product_id : int
    quantity : Annotated[int, Field(ge=1)]
    price : Annotated[Decimal, Field(max_digits=10, decimal_places=2)]
    total_price : Annotated[Decimal, Field(max_digits=10, decimal_places= 2)]



class OrderSchema(BaseModel):
    #To display the Order
    model_config = ConfigDict(
        from_attributes= True
    )

    id : int
    total_price : Annotated[Decimal, Field(max_digits=10, decimal_places=2)]
    status: OrderStatusEnum
    items : list[OrderItemSchema] = []  #Another approach about default=> =Field(default_factory = [])
    user_id : int
    user: SimpleUserSchema
    created_at : datetime
    updated_at : datetime

class UpdateOrderSchema(BaseModel):
    status : OrderStatusEnum

class CreateOrderSchema(BaseModel):
    cart_id: int






"""
"""