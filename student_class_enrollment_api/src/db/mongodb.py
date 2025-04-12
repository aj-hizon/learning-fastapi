import os

from fastapi import Depends
import motor.motor_asyncio
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
DATABASE = os.getenv("DATABASE")
STUDENTS_COLLECTION = os.getenv("STUDENTS_COLLECTION")
CLASSES_COLLECTION = os.getenv("CLASSES_COLLECTION")

if not all([MONGODB_URI, STUDENTS_COLLECTION, CLASSES_COLLECTION]):
    raise ValueError("One or more required environment variables are not set")

_client = None

def get_client():
    global _client
    if _client is None:
        _client = motor.motor_asyncio.AsyncIOMotorClient(
            MONGODB_URI,
            serverSelectionTimeoutMS=5000,
            retryWrites=True
            )
    return _client

try: 
    client = get_client()
    database = client[DATABASE]
    students_collection = database[STUDENTS_COLLECTION]
    classes_collection = database[CLASSES_COLLECTION]
except Exception as e:
    raise RuntimeError(f"Failed to connect to MongoDB: {str(e)}")


def get_students_collection():
    return students_collection

def get_classes_collection():
    return classes_collection