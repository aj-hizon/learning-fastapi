from fastapi import APIRouter, HTTPException
from src.books.book_data import books_db
from src.books.schemas import Book, Books
from typing import Optional
from datetime import date

book_router = APIRouter()

@book_router.get('/books')
async def get_all_books():
    return Books(books=books_db)

@book_router.get('/books/{book_id}')
async def get_book(book_id: int):
    for book in books_db:
        if book["id"] == book_id:
            return book
    HTTPException(status_code=404, detail="book not found")
    
@book_router.post('/books', response_model=Book)
async def add_book(book: Book): 
    books_db.append(book.model_dump())
    return book

@book_router.patch('/books/{book_id}')
async def update_book(book_id: int, title: Optional[str] = None, author: Optional[str] = None, publisher: Optional[str] = None, published_date: Optional[date] = None, page_count: Optional[int] = None, language: Optional[str] = None):
    for book in books_db:
        if book["id"] == book_id:
            if title is not None:
                book["title"] = title
            if author is not None:
                book["author"] = author
            if publisher is not None:
                book["publisher"] = publisher
            if published_date is not None:
                book["published_date"] = published_date
            if page_count is not None:
                book["page_count"] = page_count
            if language is not None:
                book["language"] = language
            return {"message": "Book Updated Succesfully"}
    raise HTTPException(status_code=404, detail="Book not found")

@book_router.delete('/books/{book_id}')
async def delete_book(book_id: int):
    for book in books_db:
        if book["id"] == book_id: 
            books_db.remove(book)
            return {"message": "Book deleted successfully"}
    raise HTTPException(status_code=404, detail="book not found")
    