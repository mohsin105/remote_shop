#CRUD and Business Logic for Product and Category Models
import math
from models.product import Product , Category, Review
from fastapi import Depends, status, HTTPException
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from database.session import get_db
from core.dependencies import get_current_user
from schemas.product import ProductListSchema, ProductSchema

class ProductService:

    @staticmethod
    def product_list(page, limit, name,category,price_gt, price_lt,order_by, db):
        stmt = select(Product).join(Category)  #Naive Join approach.
        count_stmt = select(func.count()).select_from(Product).join(Category)
        
        
        #Filtering by Product Name -> 
        if name is not None:
            stmt = stmt.where(Product.name.ilike(f"%{name}%")) 
            count_stmt = count_stmt.where(Product.name.ilike(f"%{name}%"))
        #Filtering by Product Category -> 
        if category is not None:
            stmt = stmt.where(Category.name.ilike(f"%{category}%"))  #Because Join done beforehand
            count_stmt = count_stmt.where(Category.name.ilike(f"%{category}%"))
        #Price Range based filtering  -> 
        if price_gt is not None:
            stmt = stmt.where(Product.price >=price_gt)
            count_stmt = count_stmt.where(Product.price >=price_gt)
        
        if price_lt is not None:
            stmt = stmt.where(Product.price <= price_lt)
            count_stmt = count_stmt.where(Product.price <= price_lt)
        
        if order_by == "price":
            stmt = stmt.order_by(Product.price)
            # count_stmt = count_stmt.order_by(Product.price)
        elif order_by == "-price":
            stmt = stmt.order_by(Product.price.desc())
        elif order_by == "created_at":
            stmt = stmt.order_by(Product.created_at)
        elif order_by == "-created_at":
            stmt = stmt.order_by(Product.created_at.desc())

        #Pagination -> 
        if page != 1:
            offsetValue = (page-1)*limit
            stmt = stmt.offset(offsetValue)

        stmt = stmt.limit(limit)
        
        product_count = db.scalar(count_stmt)
        # print('Product Count=> ', product_count)
        total_pages = math.ceil(product_count/limit)
        # print("Total Pages Needed =>", total_pages)
        products = db.execute(stmt).scalars().all()
        has_next = True if page<total_pages else False
        has_previous = True if page > 1 else False
        next_page = page+1
        product_items =[ProductSchema.model_validate(product) for product in products]
        # return products
        return ProductListSchema(
            items=product_items,
            total_items=product_count,
            total_pages=total_pages,
            page_size=limit,
            page=page,
            has_next=has_next,
            has_previous=has_previous
        )

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
        stmt = select(Review).where(Review.product_id == product_id)
        reviews = db.execute(stmt).scalars().all()
        return reviews

    @staticmethod
    def create_new_review(product_id, payload,user_token_value, db:Session):
        userObj = get_current_user(user_token_value, db)
        new_review = Review(
            product_id = product_id,
            user = userObj,
            rating = payload.rating,
            content = payload.content
        )
        db.add(new_review)
        db.commit()
        db.refresh(new_review)
        return new_review
    
    @staticmethod
    def update_product_review(product_id,review_id, payload, user_token_value, db:Session):
        reviewObj = db.get(Review, review_id)
        update_data = payload.model_dump(exclude_unset = True)

        for field, value in update_data.items():
            setattr(reviewObj, field, value)
        
        db.commit()
        db.refresh(reviewObj)
        return reviewObj