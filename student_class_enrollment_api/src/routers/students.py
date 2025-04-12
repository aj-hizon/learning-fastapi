from fastapi import APIRouter, status 
from src.models.student import Student, Students, StudentUpdate
from src.services.student_service import StudentService

student_router = APIRouter()

@student_router.post("/students", response_model=Student)
async def add_student(student: Student) -> Student:
    return await StudentService.add_student(student)
    
@student_router.get("/students", response_model=Students)
async def get_all_students(skip: int = 0, limit: int = 10) -> Students:
    return await StudentService.get_all_students(skip, limit)
   
@student_router.get("/students/{student_id}", response_model=Student)
async def get_student(student_id: str) -> Student:
    return await StudentService.get_student(student_id)
    
@student_router.patch("/students/{student_id}", response_model=Student)
async def update_student(
    student_id: str,
    student_update: StudentUpdate
    ) -> Student:
   return await StudentService.update_student(student_id, student_update)
       
@student_router.delete("/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(student_id: str):
    await StudentService.delete_student(student_id)
    return