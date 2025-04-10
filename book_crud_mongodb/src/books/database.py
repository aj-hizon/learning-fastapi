import motor.motor_asyncio
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Fetch MongoDB URI
MONGODB_URI = os.getenv("MONGODB_URI")
DATABASE = os.getenv("DATABASE")
COLLECTION = os.getenv("COLLECTION")

if not MONGODB_URI:
    raise ValueError("MONGODB_URI is not set in the environment variables")

# Initialize MonogDB client
client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URI)

#Connect to the database and collection
database = client[DATABASE]
book_collection = database[COLLECTION]

