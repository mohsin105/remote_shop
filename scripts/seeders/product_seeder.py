from sqlalchemy.orm import Session
from models.product import Product

def seed_products(data, db:Session):
    for item in data:
        new_product = Product(**item)
        db.add(new_product)
    
    db.commit()