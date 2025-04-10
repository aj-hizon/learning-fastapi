from pydantic import BaseModel
from typing import List

class Class(BaseModel):
    title: str
    code: str
    description: str
    instructor: str
    
class Classes(BaseModel):
    classes: List[Class]
