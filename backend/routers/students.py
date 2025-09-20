from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from database import students_col, photos_col, attendance_col
from models import StudentRegister, LoginRequest
from storage import save_file
from face_service import get_embeddings
import cv2
import numpy as np
import os

router = APIRouter(prefix="/students", tags=["Students"])

# Register new student
@router.post("/register")
def register_student(student: StudentRegister):
    if students_col.find_one({"_id": student.roll}):
        raise HTTPException(400, "Roll number already registered")
    if students_col.find_one({"email": student.email}):
        raise HTTPException(400, "Email already registered")

    students_col.insert_one({
        "_id": student.roll,   # roll is primary key
        **student.dict()
    })
    return {"roll": student.roll, "status": "registered"}


# Student login
from fastapi import Body

@router.post("/login")
def login_student(payload: dict = Body(...)):
    roll = payload.get("roll")
    password = payload.get("password")

    student = students_col.find_one({"_id": roll, "password": password})
    if not student:
        raise HTTPException(401, "Invalid roll number or password")

    student.pop("password", None)
    student["userType"] = "student"
    return {
        "status": "login successful",
        "userType": "student",
        "user": student
    }




# Upload student photo (for embeddings)
@router.post("/{roll}/upload_photo")
async def upload_photo(roll: str, file: UploadFile = File(...)):
    student = students_col.find_one({"_id": roll})
    if not student:
        raise HTTPException(404, "Student not found")

    # Read uploaded file
    content = await file.read()

    # Decode and re-encode to JPEG
    arr = np.frombuffer(content, np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if img is None:
        raise HTTPException(400, "Invalid image file")

    # Ensure directory
    save_dir = f"storage/students/{roll}"
    os.makedirs(save_dir, exist_ok=True)

    # Always save as .jpg
    save_path = os.path.join(save_dir, "face.jpg")
    cv2.imwrite(save_path, img)

    # Generate embeddings
    embeddings = get_embeddings(cv2.imencode(".jpg", img)[1].tobytes())
    if not embeddings:
        raise HTTPException(400, "No face detected")

    emb = embeddings[0]["embedding"].tolist()
    photos_col.insert_one({
        "roll": roll,
        "path": save_path,
        "embedding": emb
    })

    return {"status": "photo saved", "path": save_path}


# Get attendance records for a student
@router.get("/{roll}/attendance")
def get_attendance(roll: str):
    student = students_col.find_one({"_id": roll})
    if not student:
        raise HTTPException(404, "Student not found")

    records = list(attendance_col.find({"roll": roll}))
    return {"roll": roll, "attendance_records": records}

@router.get("/{roll}/photo")
async def get_student_photo(roll: str):
    filepath = f"storage/students/{roll}/face.jpg"
    if not os.path.exists(filepath):
        raise HTTPException(404, "Photo not found")
    return FileResponse(filepath)
