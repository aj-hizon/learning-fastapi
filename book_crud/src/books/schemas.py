from pydantic import BaseModel
from typing import List, Optional

class Book(BaseModel):
    _id: Optional[str] # Use `id` instead of `_id` for better readability
    title: str
    author: str
    publisher: str
    published_date: Optional[str]
    page_count: Optional[int]
    language: Optional[str]

    class Config:
        from_attributes = True

class Books(BaseModel):
    books: List[Book]