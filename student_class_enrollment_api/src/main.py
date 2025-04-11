import os
import uvicorn
from fastapi import FastAPI
from src.routers.students import student_router
from src.routers.classes import class_router

HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", 8001))

version = "v1"

app = FastAPI(
    title="Student-Class Enrollment API",
    description="A RESTful API for student-class enrollment",
    version=version
)

app.include_router(student_router)
app.include_router(class_router)

if __name__ == "__main__": 
    uvicorn.run("src.main:app", host=HOST, port=PORT, reload=True)


