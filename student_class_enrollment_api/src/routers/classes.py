from fastapi import APIRouter, status
from src.models.classes import Classes, Class, ClassUpdate
from src.services.class_service import ClassService

class_router = APIRouter()

@class_router.get("/classes", response_model=Classes)
async def get_all_class(skip: int = 0, limit: int = 10) -> Classes:
    return await ClassService.get_all_class(skip, limit)

@class_router.get("/classes/{id}", response_model=Class)
async def get_class_by_id(class_id: str) -> Class:
    return await ClassService.get_class_by_id(class_id)
   
@class_router.post("/classes", response_model=Class)
async def add_class(uni_class: Class) -> Class:
    return await ClassService.add_class(uni_class)
    
@class_router.put("/classes", response_model=Class)
async def update_class(class_id: str, class_update:ClassUpdate):
    return await ClassService.update_class(class_id, class_update) 

@class_router.delete("/classes/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_class(class_id: str):
    await ClassService.delete_class(class_id)
    return
