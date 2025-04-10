import uvicorn
from fastapi import FastAPI
from src.books.routes import book_router

version = 'v1'

app = FastAPI(
    title='Bookly',
    description='A RESTful API for a book review web service',
    version=version
)

app.include_router(book_router)

if __name__ == "__main__": 
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)