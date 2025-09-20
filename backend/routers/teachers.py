from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from database import teachers_col, photos_col, attendance_col, students_col
from models import TeacherRegister, LoginRequest
from storage import save_file
from face_service import get_embeddings, match_face
import datetime, numpy as np
from fastapi import Body
import uuid,cv2,os
from face_service import process_class_photo
from bson import ObjectId

def serialize_doc(doc):
    """
    Ensure ObjectId and numpy types are converted to JSON serializable.
    """
    if isinstance(doc, dict):
        out = {}
        for k, v in doc.items():
            if isinstance(v, ObjectId):
                out[k] = str(v)
            elif isinstance(v, (np.float32, np.float64)):
                out[k] = float(v)
            elif isinstance(v, (np.int32, np.int64)):
                out[k] = int(v)
            else:
                out[k] = serialize_doc(v)
        return out
    elif isinstance(doc, list):
        return [serialize_doc(i) for i in doc]
    else:
        return doc

router = APIRouter(prefix="/teachers", tags=["Teachers"])

# Register new teacher
@router.post("/register")
def register_teacher(teacher: dict = Body(...)):
    if teachers_col.find_one({"_id": teacher.get("id")}):
        raise HTTPException(400, "Teacher ID already registered")
    if teachers_col.find_one({"email": teacher.get("email")}):
        raise HTTPException(400, "Email already registered")

    teachers_col.insert_one({
        "_id": teacher.get("id"),   # teacher.id as primary key
        **teacher
    })
    return {"teacher_id": teacher.get("id"), "status": "registered"}


# Teacher login
@router.post("/login")
def login_teacher(req: dict = Body(...)):
    teacher = teachers_col.find_one({"_id": req.get("id"), "password": req.get("password")})
    if not teacher:
        raise HTTPException(401, "Invalid id or password")

    teacher.pop("password", None)
    teacher["userType"]= "faculty"
    return {
        "status": "login successful",
        "userType": "faculty",
        "user": teacher
    }



# Upload class photo → detect faces → mark attendance
@router.post("/upload_class_photo")
async def upload_class_photo(file: UploadFile = File(...)):
    content = await file.read()

    # --- Save original class photo ---
    filename = f"{uuid.uuid4().hex}_{file.filename}"
    save_path = save_file(f"class_photos/{filename}", content)

    # --- Process class photo for attendance ---
    results = process_class_photo(content, save_path, threshold=0.55, min_face_size=60)

    students_attendance = results["students"]       # per-student attendance (all students)
    detected_faces = results["detected_faces"]      # only detected faces (with bbox)

    # --- Annotate image with detected faces ---
    img = cv2.imread(save_path)
    for r in detected_faces:  
        if not r.get("bbox"):   # safety check
            continue

        x1, y1, x2, y2 = r["bbox"]

        if r.get("roll"):  #  matched student
            color = (0, 200, 0)
            label = f"{r['roll']} {r['score']:.2f}"
        else:  #  unmatched face
            continue

        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
        (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        cv2.rectangle(img, (x1, y1 - th - 6), (x1 + tw + 6, y1), color, -1)
        cv2.putText(img, label, (x1 + 3, y1 - 4), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (255, 255, 255), 1, cv2.LINE_AA)

    # --- Save annotated output image ---
    output_path = f"storage/output/{results["date"]}.png"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    cv2.imwrite(output_path, img)

    #  Ensure serializable response
    return {
        "date": results["date"],
        "attendance": serialize_doc(students_attendance),
        "annotated_image": output_path
    }





# Get all students' attendance
@router.get("/attendance/all")
def get_all_attendance():
    students = list(students_col.find({}, {"password": 0}))  # hide password
    for student in students:
        records = list(attendance_col.find({"roll": student["_id"]}))
        student["attendance_records"] = records
    return {"students": students}

# Get attendance for a specific date
@router.get("/attendance/{date}")
def get_attendance_by_date(date):
    record = attendance_col.find_one({"_id": date})
    if not record:
        raise HTTPException(404, f"No attendance record found for {date}")

    return {
        "date": record["class_date"],
        "class_photo": record.get("class_photo"),
        "students": serialize_doc(record["students"])
    }

# Serve annotated images
@router.get("/annotated/{filename}")
async def get_annotated(filename: str):
    filepath = f"storage/output/{filename}"
    if not os.path.exists(filepath):
        raise HTTPException(404, "Annotated file not found")
    return FileResponse(filepath)

@router.get("/files/{date}")
async def get_file(date: str):
    filepath = f"storage/output/{date}.png"
    if not os.path.exists(filepath):
        raise HTTPException(404, "File not found")
    return FileResponse(filepath)
