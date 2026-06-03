from fastapi import FastAPI, Depends, Path,status, HTTPException
from pydantic import BaseModel
from database.session import Base, engine
from models.product import Category, Product

Base.metadata.create_all(bind=engine)   #Later Added, Outside of first demo project
app = FastAPI()

@app.get("/")
def test_path():
    return {"Test response" : "First response in FastAPI"}

@app.get("/another")
def another_handler():
    return {"Response":"This is another path"}

#Path parameter
@app.get("/another/{user_id}")
def another_handler_with_path_param(user_id:int = Path( description="must give the id number")):
    return {"Response":f"This is another path, your id is {user_id}"}


#Query parameter 
@app.get("/greet/{person_id}")
def greet_person(person_id: int, age:int | None = None):  #the endpoint is "greet/person_id?age=value"
    return {"Response": f"Greetings person : your id is {person_id} and age is {age}"}


#THE DATABSE --------->
books = [
    {
        "id" : 1, 
        "title" : "The Alchemist", 
        "author" : "Paulo Coelho", 
        "publish_date" : "1988-01-01"
    },
    {
        "id" : 2, 
        "title" : "The God of Small Things", 
        "author" : "Arundhati Roy", 
        "publish_date" : "1997-04-04"
    },
    {
        "id" : 3, 
        "title" : "The White Tiger", 
        "author" : "Aravind Adiga", 
        "publish_date" : "2008-01-01"
    },
    {
        "id" : 4, 
        "title" : "The Palace of Illusions", 
        "author" : "Chitra Banerjee Divakaruni", 
        "publish_date" : "2008-02-12"
    },
]


#Pydantic Classes-------> 
class Book(BaseModel):
    id: int
    title:str
    author:str
    publish_date : str

class UpdateBook(BaseModel):
    title:str
    author : str
    publish_date : str

@app.get("/books")
def get_books():
    return books

@app.get("/books/{book_id}")
def book_details(book_id:int):
    for book in books:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="Book Not found")

@app.post("/books")
def add_book(book: Book):
    new_book = book.model_dump()
    books.append(new_book)
    return new_book

@app.put("/books/{book_id}")
def update_book(book_id:int, updated_book: UpdateBook ):
    # print("Given Book Id: ", book_id)
    for book in books:
        # print("Listed Book Id: ", book["id"])
        if book["id"] == book_id:
            book["title"] = updated_book.title
            book["author"] = updated_book.author
            book["publish_date"] = updated_book.publish_date
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book Not Found")


"""Another Approach for Update Operation ---
#in Pydantic class  Make every field optional

@app.put("update-student/{student_id}")
def update_student(student_id: int, student: UpdateStudent):
	if student_id not in students: 
		return {"Error": "Student does nto even exists"}
	
	if student.name in not None:
		students[student_id].name = student.name
	if student.age in not None:
		students[student_id].age = student.age
	if student.year in not None:
		students[student_id].year = student.year
	
	return students[student_id]


"""

@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            books.remove(book)
            return {"Message": "Book deleted successfully"}
    raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="Book not found")


