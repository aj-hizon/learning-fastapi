from pydantic import BaseModel
from typing import List

class Student(BaseModel):
    name: str
    email: str
    age: int
    enrolled_classes: List[str]

class Students(BaseModel):
    students: List[Student]