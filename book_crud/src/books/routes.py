from fastapi import APIRouter, HTTPException
from src.books.database import book_collection
from src.books.schemas import Book, Books
from typing import Optional
from datetime import date
from bson import ObjectId
from bson.errors import InvalidId

book_router = APIRouter()

@book_router.get('/books', response_model=Books)
async def get_all_books():
    books = await book_collection.find().to_list(length=100)
    return Books(books=books)

@book_router.get('/books/{book_id}', response_model=Book)
async def get_book(book_id: str):
    try:
        # Validate and convert book_id to ObjectId
        object_id = ObjectId(book_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid book ID for format")

    # Query the database
    book = await book_collection.find_one({"_id": object_id})
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book
    
@book_router.post('/books', response_model=Book)
async def add_book(book: Book): 
    book_dict = book.model_dump()
    result = await book_collection.insert_one(book_dict)
    book_dict["_id"] = str(result.inserted_id)
    return book_dict

@book_router.patch('/books/{book_id}')
async def update_book(book_id: str, title: Optional[str] = None, author: Optional[str] = None, publisher: Optional[str] = None, published_date: Optional[date] = None, page_count: Optional[int] = None, language: Optional[str] = None):
    update_data = {}
    if title is not None:
        update_data["title"] = title
    if author is not None:
        update_data["author"] = author
    if publisher is not None:
        update_data["publisher"] = publisher
    if published_date is not None:
        update_data["published_date"] = published_date
    if page_count is not None:
       update_data["page_count"] = page_count
    if language is not None:
        update_data["language"] = language

    result = await book_collection.update_one({"_id": ObjectId(book_id)}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book Updated Succesfully"}

@book_router.delete('/books/{book_id}')
async def delete_book(book_id: str):
    try: 
        object_id = ObjectId(book_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Ivalid book ID for format")
    
    result = await book_collection.delete_one({"_id": object_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="book not found")
    return {"message": "Book deleted successfully"}
   
    