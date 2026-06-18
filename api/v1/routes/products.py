#Product related Endpoint handler functions

from fastapi import Depends, status, HTTPException, APIRouter
from database.session import get_db
from models.product import Product , Category
from schemas.product import CategorySchema, CreateCategorySchema, ProductSchema, CreateProductSchema, UpdateProductSchema
from sqlalchemy import select, delete
from sqlalchemy.orm import Session
from services.product_service import ProductService, CategoryService
from core.dependencies import get_current_user

router = APIRouter(
    # prefix="/products",
    tags=["Products"]
)

""" Product Related Endpoints  """

@router.get("/products", response_model=list[ProductSchema])
def get_products(db : Session = Depends(get_db)):
    #product list 
    products = ProductService.product_list(db)
    return products

@router.get("/products/{product_id}", response_model=ProductSchema)
def product_details(product_id: int, db : Session = Depends(get_db)):
    product = ProductService.specific_product(product_id, db)
    return product
    

@router.post("/products", response_model=ProductSchema)
def create_product(given_obj : CreateProductSchema, db:Session = Depends(get_db)):
    new_product = ProductService.create_new_product(given_obj, db)
    return new_product

@router.patch("/products/{product_id}", response_model= ProductSchema)
def update_product(
    product_id: int, 
    product_payload: UpdateProductSchema, 
    db:Session = Depends(get_db)
):
    productObj = ProductService.preform_product_update(product_id, product_payload, db)
    return productObj


@router.delete("/products/{product_id}")
def delete_product(product_id :int, db: Session = Depends(get_db)):
    #delete a specific product
    productObj = db.get(Product, product_id)
    db.delete(productObj)
    db.commit()


"""  Category Related CRUD  Endpoints -------->     """

@router.get("/categories", response_model=list[CategorySchema])
def get_categories(categories = Depends(CategoryService.category_list)):
    return categories
    

@router.get("/categories/{category_id}", response_model=CategorySchema)
def specific_category(category_id : int, db : Session = Depends(get_db)):
    category = CategoryService.category_details(category_id, db)
    return category

@router.post("/categories", response_model=CategorySchema)
def create_category(inputted_category : CreateCategorySchema, db:Session = Depends(get_db)):
    new_category = CategoryService.create_new_category(inputted_category, db)
    return new_category


@router.patch("/categories/{category_id}")
def update_category(
    category_id : int, 
    updated_obj : CreateCategorySchema, 
    db: Session = Depends(get_db)
):
    category_obj = CategoryService.preform_category_update(category_id, updated_obj, db)
    return category_obj

@router.delete("/categories/{category_id}")
def delete_category(category_id : int, db: Session = Depends(get_db)):
    category_obj = db.get(Category, category_id)
    db.delete(category_obj)
    db.commit()

# @router.delete("/categories/test_bulk_delete")
# def delete_bulk_categories(db:Session = Depends(get_db)):
#     stmt = delete(Category).where(Category.id >22)
#     db.execute(stmt)
#     db.commit()
#     return {"response": "Successfully Deleted"}

"""Product Review related Endpoints ----------->      """
"""
@router.get("products/{product_id}/reviews", response_model=list[ReviewListSchema])
def get_reviews(product_id:int, db:Session = Depends(get_db)):
    pass


@router.post("/products/{product_id}/reviews")
def create_review(
    product_id:int, current_user:dict = Depends(get_current_user),
    payload : ReviewCreateSchema,
    db:Session = Depends(get_db)
):
    pass

@router.patch("/products/{product_id}/reviews/{reivew_id}", response_model=ReviewListSchema)
def update_review(
    product_id:int,reivew_id:int,
    payload : ReviewUpdateSchema,
    current_user : dict = Depends(get_current_user),
    db: Session = Depends(get_db),
 ):
    pass

@router.delete("/products/{product_id}/reviews/{review_id}")
def delete_review(
    product_id: int,
    review_id: int,
):
    pass

"""