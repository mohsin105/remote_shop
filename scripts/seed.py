import json
from scripts.seeders.category_seeder import seed_categories
from scripts.seeders.product_seeder import seed_products
from database.session import SessionLocal

def run_seed():
    db = SessionLocal()

    try:
        # with open("scripts/data/categories.json", "r") as f:
        #     categories_data = json.load(f)
        
        # seed_categories(categories_data, db)

        with open("scripts/data/products.json", "r") as f:
            products_data = json.load(f)
        
        seed_products(products_data, db)
    
    finally:
        db.close()

run_seed()
            