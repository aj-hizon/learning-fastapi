from fastapi import APIRouter, HTTPException, status 
from src.models.student import Student, Students
from src.db.mongodb import students_collection

student_router = APIRouter()

@student_router.post("/students", response_model=Student)
async def add_student(student: Student):
    student_dict = student.model_dump()

    try:
        result = await students_collection.insert_one(student_dict)
        student_dict["_id"] = str(result.inserted_id)
        return Student(**student_dict)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error inserting student into database: {str(e)}"
        )

    
# @student_router.get()
# @student_router.get()
# @student_router.put()
# @student_router.delete()
