from fastapi import APIRouter, HTTPException, status 
from pymongo.errors import PyMongoError
from src.models.student import Student, Students, StudentUpdate
from src.db.mongodb import students_collection
from bson import ObjectId
from bson.errors import InvalidId
from typing import Optional, List
import logging


logger = logging.getLogger(__name__)

student_router = APIRouter()

@student_router.post("/students", response_model=Student)
async def add_student(student: Student) -> Student:
    student_dict = student.model_dump()

    existing_student = await students_collection.find_one({"email": student.email})
    if existing_student:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A student with this email already exists"
        )

    try:
        result = await students_collection.insert_one(student_dict)
        student_dict["id"] = str(result.inserted_id)
        return Student(**student_dict)
    except PyMongoError as e:
        logger.error(f"Database error: {str(e)}") 
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while inserting the student"
        )

@student_router.get("/students", response_model=Students)
async def get_all_students(skip: int = 0, limit: int = 10) -> Students:
    try:
        students = await students_collection.find().skip(skip).limit(limit).to_list(length=limit)
        if not students: 
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No students found"
            )
        return Students(students=students)
    except PyMongoError as e:
        logger.error(f"Database error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while fetching students"
        )

@student_router.get("/students/{student_id}", response_model=Student)
async def get_student(student_id: str) -> Student:
    try:
        object_id = ObjectId(student_id)
    except InvalidId:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid student ID format"
        )

    try: 
        result = await students_collection.find_one({"_id": object_id})
        if not result:
            logger.warning(f"Student with ID {student_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Student with ID {student_id} not found"
            )
        return Student(**result)
    
    except PyMongoError as e:
        logger.error(f"Database error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while getting the student information"
        )
    except Exception as e:
        logger.error(f"Unexpected error while fetching student with ID {student_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )

@student_router.patch("/students/{student_id}", response_model=Student)
async def update_student(
    student_id: str,
    student_update: StudentUpdate
    ) -> Student:
    try: 
        object_id = ObjectId(student_id)
    except InvalidId:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid ID format {student_id}"
        )
    
    update_data = student_update.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields provided for update"
        )
   
    try: 
        result = await students_collection.update_one(
            {"_id": object_id},
            {"$set": update_data}
        )

        if result.matched_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Student with ID {student_id} not found"
            )
        
        updated_student = await students_collection.find_one({"_id": object_id})
        if not updated_student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Student with ID {student_id} not found"
            )
        
        return Student(**updated_student)
    except PyMongoError as e:
        logger.error(f"Database error while updating student information with ID {student_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while updating the student information"
        )
       
@student_router.delete("/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(student_id: str):
    try: 
        object_id = ObjectId(student_id)
    except InvalidId:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid student ID format"
        )
    
    try:
        result = await students_collection.delete_one({"_id": object_id})
        if result.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student not found"
            )
    except PyMongoError as e:
        logger.error(f"Database error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while deleting the student"
        )
    return