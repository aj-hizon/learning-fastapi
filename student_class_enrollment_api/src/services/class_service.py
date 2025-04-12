import logging

from fastapi import HTTPException, status
from pymongo.errors import PyMongoError, DuplicateKeyError
from bson.errors import InvalidId
from bson import ObjectId

from src.models.classes import Class, Classes, ClassUpdate
from src.db.mongodb import classes_collection

logger = logging.getLogger(__name__)

class ClassService: 
    @staticmethod
    async def get_all_class(skip: int = 0, limit: int = 10) -> Classes:
        try:
            classes = await classes_collection.find().skip(skip).limit(limit).to_list(length=100)
            if not classes:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Classes not found"
                    )
            return Classes(classes=classes)
        except PyMongoError as e:
            logger.error(f"Database error: {str(e)}") 
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while fetching classes"
            )
    
    @staticmethod
    async def get_class_by_id(class_id: str) -> Class:
        try:
            object_id = ObjectId(class_id)
        except InvalidId:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid Class ID format"
            )

        try:
            result = await classes_collection.find_one({"_id": object_id})
            if not result:
                logger.error(f"Class with Class ID {object_id} not found")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Class with ID: {object_id} not found"
                )
            return Class(**result)
        except PyMongoError as e:
            logger.error(f"Database error occurred: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while getting the class information"
            )
    
    @staticmethod
    async def add_class(uni_class: Class) -> Class:  
        class_dict = uni_class.model_dump()

        existing_class = await classes_collection.find_one({"code": uni_class.code})
        if existing_class:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A class with this code already exists"
            )
        try:
            result = await classes_collection.insert_one(class_dict)
            class_dict["id"] = str(result.inserted_id)
            return Class(**class_dict)
        except DuplicateKeyError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A class with this code already exists"
            )
        except PyMongoError as e:
            logger.error(f"Database error occurred: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while inserting class"
            )
    
    @staticmethod
    async def update_class(class_id: str, class_update: ClassUpdate) -> Class:
        try: 
            object_id = ObjectId(class_id)
        except InvalidId:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid Class ID format"
            )
        
        update_data = class_update.model_dump(exclude_unset=True)

        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields provided for update"
            )
        
        try:
            result = await classes_collection.update_one(
                {"_id": object_id},
                {"$set": update_data}
            )
            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Student with ID {object_id} not found"
                )
            
            updated_class = await classes_collection.find_one({"_id": object_id})
            if not updated_class:
                raise HTTPException(
                    status=status.HTTP_404_NOT_FOUND,
                    detail=f"Student with ID {object_id} not found"
                )
            
            return Class(**updated_class) 
        except PyMongoError as e:
            logger.error(f"Database error occurred: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while updating class"
            )
        
    @staticmethod
    async def delete_class(class_id: str):
        try:
            object_id = ObjectId(class_id)
        except InvalidId:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid class ID format"
                )
            
        try: 
            result = await classes_collection.delete_one({"_id": object_id})
            if result.deleted_count == 0:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Class ID not found"
                    )
        except PyMongoError as e:
            logger.error(f"Database error occurred: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while deleting class"
                )
        
        