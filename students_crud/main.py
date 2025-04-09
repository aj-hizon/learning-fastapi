import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from fastapi import HTTPException
from typing import Optional

class Student(BaseModel):
    studentId: int
    firstName: str
    lastName: str
    section: str = None

class Students(BaseModel):
    students: List[Student]

app = FastAPI()

memory_db = {"Students": []}

@app.get('/')
async def get_students():
    return Students(students=memory_db["Students"])

@app.post('/students ', response_model=Student)
async def add_credentials(student: Student):
    memory_db["Students"].append(student)
    return student
    
@app.patch('/students/{studentId}')
async def update_student(studentId: int, firstName: Optional[str] = None, lastName: Optional[str] = None, section: Optional[str] = None, newStudentId: Optional[int] = None):
    for student in memory_db["Students"]:
        if student.studentId == studentId:
            if firstName is not None:
                student.firstName = firstName
            if lastName is not None:
                student.lastName = lastName
            if section is not None: 
                student.section = section
            if studentId is not None:
                student.studentId = newStudentId
        return {"message": "Student Information Update Succesfully", "student": student}
    raise HTTPException(status_code=404, detail="Student not found")
    
@app.delete('/students/{studentId}')
async def delete_student(studentId: int):
    for student in memory_db["Students"]: 
        if student.studentId == studentId:
            memory_db["Students"].remove(student)
            return {"message": "Student deleted succesfully"}
        raise HTTPException(status_code=404, detail="Student not found")
    
if __name__ == "__main__":
    # uvicorn.run(app, host="0.0.0.0", port=3001)
    uvicorn.run(app)



# @app.put('/students/{student_id}/section')
# async def update_student_section(student_id: int, new_section: str):
#     for student in memory_db["Students"]:
#         if student.studentId == student_id:
#             student.section = new_section
#             return {"message": "Section updated successfully", "student": student}
#     raise HTTPException(status_code=404, detail="Student not found")