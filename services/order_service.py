from sqlalchemy.orm import Session, selectinload
from fastapi import Depends, status, HTTPException
from models.order import Cart, CartItem, Order, OrderItem
from models.user import User
from sqlalchemy import select

class CartService:

    @staticmethod
    def show_cart_list(current_user, db:Session):
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
    
    @staticmethod
    def show_cart_details(cart_id:int,db:Session):
        cart = db.get(Cart, cart_id)
        return cart

    @staticmethod
    def create_new_cart(current_user, db:Session):
        userstmt = select(User).where(User.username == current_user.get("username"))
        userObj = db.execute(userstmt).scalars().first()
        
        new_cart = Cart(
            user_id = userObj.id
        )
        db.add(new_cart)
        db.commit()
        db.refresh(new_cart)
        return new_cart

    @staticmethod
    def cart_items_list(cart_id:int, db:Session):
        stmt = select(CartItem).where(CartItem.cart_id == cart_id)
        items = db.execute(stmt).scalars().all()
        return items

    @staticmethod
    def create_new_cartItem(cart_id,payload,db:Session):
        new_cartItem = CartItem(
            cart_id = cart_id,
            product_id = payload.product_id,
            quantity = payload.quantity
        )
        db.add(new_cartItem)
        db.commit()
        db.refresh(new_cartItem)
        return new_cartItem

    @staticmethod
    def update_cartItem_quantity(cart_id,item_id,payload,  db:Session):
        itemObj = db.get(CartItem, item_id)
        itemObj.quantity = payload.quantity
        db.commit()
        db.refresh(itemObj)
        return itemObj


    


class OrderService:

    @staticmethod
    def get_orders_list(db:Session):
        #Admin can see any order details. User can only see owned orders
        stmt = select(Order).options(selectinload(Order.items))
        orders = db.execute(stmt).scalars().all()
        return orders

    @staticmethod
    def get_order_details(order_id, db:Session):
        #Admin can see any order details. User can only see owned orders
        order = db.get(Order, order_id)
        return order

    @staticmethod
    def create_new_order(cart_id, current_user, db:Session):
        cartObj = db.get(Cart, cart_id)
        total_price = 0
        for item in cartObj.items:
            total_price += item.product.price * item.quantity


        if cartObj.user.username == current_user.get("username"):
            newOrder = Order(
                user = cartObj.user,
                total_price = total_price
            )
            #Creating OrderItems from Cartitems -> 
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
            return newOrder
        else:
            raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail="User Does Not Match")

    @staticmethod
    def preform_order_update(order_id,payload, db:Session):
        #Admin can change to any status. User can only Cancel the incomplete orders
        orderObj = db.get(Order, order_id)
        orderObj.status = payload.status
        db.commit()
        db.refresh(orderObj)
        return orderObj

class PaymentService:
    pass