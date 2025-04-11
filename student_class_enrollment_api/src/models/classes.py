from pydantic import BaseModel
from typing import List, Optional

class Class(BaseModel):
    title: str
    code: str
    description: str
    instructor: str
    
class Classes(BaseModel):
    classes: List[Class]

class ClassUpdate(BaseModel):
    title: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None
    instructor: Optional[str] = None