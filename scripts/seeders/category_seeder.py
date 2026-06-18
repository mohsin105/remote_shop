from sqlalchemy.orm import Session
from models.product import Category

def seed_categories(data, db:Session):
    for item in data:
        new_category = Category(**item)
        db.add(new_category)
    
    db.commit()