import motor.motor_asyncio
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
DATABASE = os.getenv("DATABASE")
STUDENTS_COLLECTION = os.getenv("STUDENTS_COLLECTION")
CLASSES_COLLECTION = os.getenv("CLASSES_COLLECTION")

if not MONGODB_URI:
    raise ValueError("MONGODB_URI is not set in the environment variables")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URI)

database = client[DATABASE]
students_collection = database[STUDENTS_COLLECTION]
classes_collection = database[CLASSES_COLLECTION]