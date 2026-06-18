#Cart & Order related Endpoint handler functions
from fastapi import Depends, status, HTTPException, APIRouter
from database.session import get_db
from models.order import Cart , CartItem, Order, OrderItem
from models.user import User
from models.product import Product
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select
from schemas.order import CartSchema, CartItemSchema, CreateCartItemSchema, UpdateCartItemSchema, OrderItemSchema, OrderSchema, UpdateOrderSchema
from core.dependencies import get_current_user, get_token_payload
from services.order_service import CartService, OrderService, PaymentService

router = APIRouter(
    tags=["Orders"]
)


"""Cart CRUD Route handlers ------->  """


@router.get("/carts", response_model=list[CartSchema])
def cart_list(user_token_value:dict = Depends(get_token_payload),db:Session = Depends(get_db)):
    carts = CartService.show_cart_list(user_token_value, db)
    return carts

@router.get("/carts/{cart_id}", response_model= CartSchema)
def cart_details(cart_id:int, db:Session = Depends(get_db)):
    cart = CartService.show_cart_details(cart_id, db)
    return cart

@router.post("/carts", response_model= CartSchema)
def create_cart(user_token_value:dict = Depends(get_token_payload), db:Session = Depends(get_db)):
    new_cart = CartService.create_new_cart(user_token_value, db)
    return new_cart


"""CartItem CRUD Route handlers ------->  """

@router.get("/cart/{cart_id}/items", response_model=list[CartItemSchema])
def cart_items(cart_id:int, db:Session = Depends(get_db)):
    items = CartService.cart_items_list(cart_id, db)
    return items

@router.post("/cart/{cart_id}/items", response_model= CartItemSchema)
def add_cartItem(
    cart_id:int,
    payload: CreateCartItemSchema, 
    current_user:dict = Depends(get_token_payload), 
    db:Session = Depends(get_db)
):
    new_cartItem = CartService.create_new_cartItem(cart_id, payload, db)
    return new_cartItem

@router.patch("/carts/{cart_id}/items/{item_id}", response_model=CartItemSchema)
def update_cartItem(
    cart_id:int, item_id:int,
    payload :UpdateCartItemSchema, 
    current_user:dict = Depends(get_token_payload),  
    db:Session = Depends(get_db)
):
    itemObj = CartService.update_cartItem_quantity(cart_id, item_id, payload, db)
    return itemObj

@router.delete("/carts/{cart_id}/items/{item_id}")
def remove_cartItem(cart_id:int,item_id: int, db:Session = Depends(get_db)):
    itemObj = db.get(CartItem, item_id)
    db.delete(itemObj)
    db.commit()


""" Order CRUD Route Handlers -------> """

@router.get("/orders", response_model=list[OrderSchema])
def orders_list(db:Session = Depends(get_db)):
    #Admin can see any order details. User can only see owned orders
    orders = OrderService.get_orders_list(db)
    return orders



@router.get("/orders/{order_id}", response_model= OrderSchema)
def order_details(order_id:int , db:Session = Depends(get_db)):
    #Admin can see any order details. User can only see owned orders
    order = OrderService.get_order_details(order_id, db)
    return order


@router.post("/orders", response_model=OrderSchema)
def create_order(
    cart_id: int,user_token_value:dict = Depends(get_token_payload),
    db:Session = Depends(get_db)
):
    newOrder = OrderService.create_new_order(cart_id, user_token_value, db)
    return newOrder


@router.patch("/orders/{order_id}", response_model=OrderSchema)
def update_order(
    order_id:int,payload :UpdateOrderSchema  ,
    user_token_value:dict = Depends(get_token_payload),
    db:Session = Depends(get_db)
):
    #Admin can change to any status. User can only Cancel the incomplete orders
    orderObj = OrderService.preform_order_update(order_id, payload, db)
    return orderObj

"""
"""





