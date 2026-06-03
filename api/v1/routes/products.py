#Product related Endpoint handler functions
"""
from fastapi import Depends, status, HTTPException
from database.session import get_db
from main import app

@app.get("/products")
def get_products():
    #product list
    pass

@app.get("/products/{product_id}")
def product_details(product_id: int):
    #retrieve single product
    pass

@app.post("/products")
def create_product():
    pass

@app.patch("/products/{product_id}")
def update_product(product_id: int):
    #Parital Update the product
    pass

@app.delete("/products/{product_id}")
def delete_product(product_id :int):
    #delete a specific product
    pass

"""