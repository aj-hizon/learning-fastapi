from pydantic import BaseModel
from typing import List, Optional

class Student(BaseModel):
    name: str
    email: str
    age: int
    enrolled_classes: List[str]

class Students(BaseModel):
    students: List[Student]

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = None
    enrolled_classes: Optional[List[str]] = None