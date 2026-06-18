#CRUD and Business Logic for Product and Category Models
from models.product import Product , Category
from fastapi import Depends, status, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from database.session import get_db

class ProductService:

    @staticmethod
    def product_list(db):
        stmt = select(Product).join(Category)  #Naive Join approach. 
        products = db.execute(stmt).scalars().all()
        return products

    @staticmethod
    def specific_product(product_id, db):
        product = db.get(Product, product_id) # querying via primary key
        if not product:
            raise HTTPException(
                status_code= status.HTTP_404_NOT_FOUND, 
                detail="Product Not Found"
            )
        return product

    @staticmethod
    def create_new_product(given_obj, db:Session):
        categoryId = given_obj.category_id
        categoryObj = db.get(Category, categoryId)
        new_product = Product(
            name = given_obj.name,
            description = given_obj.description,
            price = given_obj.price,
            stock = given_obj.stock,
            category = categoryObj
        )
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        return new_product

    @staticmethod
    def preform_product_update(product_id, product_payload, db:Session):
        productObj = db.get(Product, product_id)
        if not productObj:
            raise HTTPException(
                status_code= status.HTTP_404_NOT_FOUND, detail= "Product Not Found"
            )
        # print("Original Payload-> ", product_payload)
        #Parital Update the product
        update_data = product_payload.model_dump(exclude_unset=True)  #exlucding the fields that were not given

        # print("Clean Excluded Payload -> ", update_data)
        #Updating the attributes of the productObject
        for field, value in update_data.items():
            setattr(productObj, field, value)
        db.commit()
        db.refresh(productObj)
        return productObj


class CategoryService:

    @staticmethod
    def category_list(db:Session = Depends(get_db)):
        stmt = select(Category)
        categories = db.execute(stmt).scalars().all()
        return categories

    @staticmethod
    def category_details(category_id, db:Session):
        category = db.get(Category, category_id)
        if not category:
            raise HTTPException(
                status_code= status.HTTP_404_NOT_FOUND, 
                detail="Category Not Found"
            )
        return category
    
    @staticmethod
    def create_new_category(inputted_category,db:Session):
        new_category = Category(
            name = inputted_category.name, 
            description = inputted_category.description
        )
        db.add(new_category)
        db.commit()
        db.refresh(new_category)
        return new_category

    @staticmethod
    def preform_category_update(category_id,updated_obj,db:Session):
        category_obj = db.get(Category, category_id)
        if updated_obj.name and updated_obj.name != "string":
            category_obj.name = updated_obj.name
        if updated_obj.description and updated_obj.description != "string":
            category_obj.description = updated_obj.description
        
        db.commit()
        db.refresh(category_obj)
        return category_obj

class ReviewService:

    @staticmethod
    def review_list(product_id,db:Session):
        pass

    @staticmethod
    def create_new_review(db:Session):
        pass

    def update_product_review(db:Session):
        pass