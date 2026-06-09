#Product related Endpoint handler functions

from fastapi import Depends, status, HTTPException, APIRouter
from database.session import get_db
from models.product import Product , Category
from schemas.product import CategorySchema, CreateCategorySchema, ProductSchema, CreateProductSchema, UpdateProductSchema
from sqlalchemy import select
from sqlalchemy.orm import Session

router = APIRouter(
    # prefix="/products",
    tags=["Products"]
)

""" Product Related Endpoints  """

@router.get("/products", response_model=list[ProductSchema])
def get_products(db : Session = Depends(get_db)):
    #product list
    # stmt = select(Product)
    stmt = select(Product).join(Category)  #Naive Join approach. 
    products = db.execute(stmt).scalars().all()
    return products

@router.get("/products/{product_id}", response_model=ProductSchema)
def product_details(product_id: int, db : Session = Depends(get_db)):
    #retrieve single product
    # stmt = select(Product).where(Product.id == product_id)
    # product = db.execute(stmt).scalar_one()
    product = db.get(Product, product_id) # querying via primary key
    if not product:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="Product Not Found")
    return product
    

@router.post("/products", response_model=ProductSchema)
def create_product(given_obj : CreateProductSchema, db:Session = Depends(get_db)):
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

@router.patch("/products/{product_id}", response_model= ProductSchema)
def update_product(
    product_id: int, 
    product_payload: UpdateProductSchema, 
    db:Session = Depends(get_db)
):
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


@router.delete("/products/{product_id}")
def delete_product(product_id :int, db: Session = Depends(get_db)):
    #delete a specific product
    productObj = db.get(Product, product_id)
    db.delete(productObj)
    db.commit()


"""  Category Related Endpoints """

@router.get("/categories", response_model=list[CategorySchema])
def get_categories(db: Session = Depends(get_db)):
    stmt = select(Category)
    categories = db.execute(stmt).scalars().all()
    return categories
    

@router.get("/categories/{category_id}", response_model=CategorySchema)
def specific_category(category_id : int, db : Session = Depends(get_db)):
    #Process-1  ---> 
    category = db.get(Category, category_id)
    #Process-2 ---> 
    # stmt = select(Category).where(Category.id == category_id)
    # category = db.execute(stmt).scalar_one()
    return category

@router.post("/categories", response_model=CategorySchema)
def create_category(inputted_category : CreateCategorySchema, db:Session = Depends(get_db)):
    new_category = Category(
        name = inputted_category.name, 
        description = inputted_category.description
    )
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


@router.patch("/categories/{category_id}")
def update_category(
    category_id : int, 
    updated_obj : CreateCategorySchema, 
    db: Session = Depends(get_db)
):
    category_obj = db.get(Category, category_id)
    if updated_obj.name and updated_obj.name != "string":
        category_obj.name = updated_obj.name
    if updated_obj.description and updated_obj.description != "string":
        category_obj.description = updated_obj.description
    
    db.commit()
    db.refresh(category_obj)
    return category_obj

@router.delete("/categories/{category_id}")
def delete_category(category_id : int, db: Session = Depends(get_db)):
    category_obj = db.get(Category, category_id)
    db.delete(category_obj)
    db.commit()
"""
"""