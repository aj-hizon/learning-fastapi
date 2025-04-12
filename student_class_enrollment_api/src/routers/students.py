from fastapi import APIRouter, status, Depends
from src.models.student import Student, Students, StudentUpdate
from src.services.student_service import StudentService

student_router = APIRouter()

@student_router.post("/students", response_model=Student)
async def add_student(student: Student, service: StudentService = Depends()) -> Student:
    return await service.add_student(student)
    
@student_router.get("/students", response_model=Students)
async def get_all_students(
    skip: int = 0, 
    limit: int = 10,
    service: StudentService = Depends()
    ) -> Students:
    return await service.get_all_students(skip, limit)
   
@student_router.get("/students/{student_id}", response_model=Student)
async def get_student(
    student_id: str,
    service: StudentService = Depends()
    ) -> Student:
    return await service.get_student(student_id)
    
@student_router.patch("/students/{student_id}", response_model=Student)
async def update_student(
    student_id: str,
    student_update: StudentUpdate,
    service: StudentService = Depends()
    ) -> Student:
   return await service.update_student(student_id, student_update)
       
@student_router.delete("/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(
    student_id: str,
    service: StudentService = Depends()
    ):
    await service.delete_student(student_id)
    return