from pydantic import BaseModel
from typing import List
from datetime import date

class Book(BaseModel):
    id: int
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str

class Books(BaseModel):
    books: List[Book]