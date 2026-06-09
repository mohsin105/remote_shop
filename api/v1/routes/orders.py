#Cart & Order related Endpoint handler functions
from fastapi import Depends, status, HTTPException, APIRouter
from database.session import get_db
from models.order import Cart , CartItem, Order, OrderItem
from models.user import User
from models.product import Product
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select
from schemas.order import CartSchema, CartItemSchema, CreateCartItemSchema, UpdateCartItemSchema, OrderItemSchema, OrderSchema, UpdateOrderSchema
from core.dependencies import get_current_user

router = APIRouter(
    tags=["Orders"]
)


"""Cart CRUD Route handlers ------->  """


@router.get("/carts", response_model=list[CartSchema])
def cart_list(current_user:dict = Depends(get_current_user),db:Session = Depends(get_db)):
    user_role = current_user.get("role")
    print("Current User-> ", current_user)
    
    #Admin read all. User read only his
    if user_role == "admin":
        stmt = select(Cart)
    else:
        username = current_user.get("username")
        userstmt = select(User).where(User.username == username)
        userObj = db.execute(userstmt).scalars().first()
        stmt = select(Cart).where(Cart.user_id == userObj.id)
    carts = db.execute(stmt).scalars().all()
    return carts

@router.get("/carts/{cart_id}", response_model= CartSchema)
def cart_details(cart_id:int, db:Session = Depends(get_db)):
    cart = db.get(Cart, cart_id)
    return cart

@router.post("/carts", response_model= CartSchema)
def create_cart(current_user:dict = Depends(get_current_user), db:Session = Depends(get_db)):
    userstmt = select(User).where(User.username == current_user.get("username"))
    userObj = db.execute(userstmt).scalars().first()
    new_cart = Cart(
        user_id = userObj.id
    )
    db.add(new_cart)
    db.commit()
    db.refresh(new_cart)
    return new_cart


"""CartItem CRUD Route handlers ------->  """

@router.get("/cart/{cart_id}/items", response_model=list[CartItemSchema])
def cart_items(cart_id:int, db:Session = Depends(get_db)):
    stmt = select(CartItem).where(CartItem.cart_id == cart_id)
    items = db.execute(stmt).scalars().all()
    return items

@router.post("/cart/{cart_id}/items", response_model= CartItemSchema)
def add_cartItem(
    cart_id:int,
    payload: CreateCartItemSchema, 
    current_user:dict = Depends(get_current_user), 
    db:Session = Depends(get_db)
):
    new_cartItem = CartItem(
        cart_id = cart_id,
        product_id = payload.product_id,
        quantity = payload.quantity
    )
    db.add(new_cartItem)
    db.commit()
    db.refresh(new_cartItem)
    return new_cartItem

@router.patch("/carts/{cart_id}/items/{item_id}")
def update_cartItem(
    cart_id:int, item_id:int,
    payload :UpdateCartItemSchema, 
    current_user:dict = Depends(get_current_user),  
    db:Session = Depends(get_db)
):
    itemObj = db.get(CartItem, item_id)
    itemObj.quantity = payload.quantity
    db.commit()
    db.refresh(itemObj)

@router.delete("/carts/{cart_id}/items/{item_id}")
def remove_cartItem(cart_id:int,item_id: int, db:Session = Depends(get_db)):
    itemObj = db.get(CartItem, item_id)
    db.delete(itemObj)
    db.commit()


@router.get("/orders", response_model=list[OrderSchema])
def orders_list(db:Session = Depends(get_db)):
    #Admin can see any order details. User can only see owned orders
    stmt = select(Order).options(selectinload(Order.items))
    orders = db.execute(stmt).scalars().all()
    return orders



@router.get("/orders/{order_id}", response_model= OrderSchema)
def order_details(order_id:int , db:Session = Depends(get_db)):
    #Admin can see any order details. User can only see owned orders
    order = db.get(Order, order_id)
    return order


@router.post("/orders")
def create_order(
    cart_id: int,current_user:dict = Depends(get_current_user),
    db:Session = Depends(get_db)
):
    cartObj = db.get(Cart, cart_id)
    total_price = 0
    for item in cartObj.items:
        total_price += item.product.price * item.quantity

    if cartObj.user.username == current_user.get("username"):
        newOrder = Order(
            user = cartObj.user,
            total_price = total_price
        )

        for item in cartObj.items:
            newOrder.items.append(
                OrderItem(
                    # order = newOrder
                    product_id = item.product_id,
                    quantity = item.quantity,
                    price = item.product.price,
                    total_price = item.product.price * item.quantity

                )
            )

        db.add(newOrder)
        db.commit()
        db.refresh(newOrder)
        db.delete(cartObj)
        db.commit()
    else:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail="User Does Not Match")
    pass


@router.patch("/orders/{order_id}", response_model=OrderSchema)
def update_order(
    order_id:int,payload :UpdateOrderSchema  ,
    current_user:dict = Depends(get_current_user),
    db:Session = Depends(get_db)
):
    #Admin can change to any status. User can only Cancel the incomplete orders
    orderObj = db.get(Order, order_id)
    orderObj.status = payload.status
    db.commit()
    db.refresh(orderObj)
    return orderObj

"""
"""





