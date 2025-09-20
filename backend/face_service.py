import os
import cv2
import numpy as np
from math import isfinite
from insightface.app import FaceAnalysis
from sklearn.metrics.pairwise import cosine_similarity
from database import students_col, photos_col, attendance_col
import datetime

# Initialize InsightFace
face_app = FaceAnalysis(name="antelopev2", allowed_modules=['detection','recognition'])
face_app.prepare(ctx_id=-1, det_size=(640,640))   # -1 = CPU, 0 = GPU

# ----------------------------
# Student Photo Embeddings
# ----------------------------
def get_embeddings(img_bytes: bytes):
    arr = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    faces = face_app.get(img)
    result = []
    for f in faces:
        emb = np.array(f.embedding, dtype=np.float32)
        norm = np.linalg.norm(emb)
        if norm > 0:
            emb = emb / norm
        result.append({"bbox": f.bbox.tolist(), "embedding": emb})
    return result


# ----------------------------
# Utility Functions
# ----------------------------
def cosine_similarity_vec(a, b):
    a = np.asarray(a, dtype=np.float32)
    b = np.asarray(b, dtype=np.float32)
    denom = (np.linalg.norm(a) * np.linalg.norm(b))
    if denom == 0 or not isfinite(denom):
        return -1.0
    return float(np.dot(a, b) / denom)


def match_face(detected_emb, known_db, threshold=0.55):
    best_id, best_score = None, -1
    for sid, emb_list in known_db.items():
        arr = np.vstack(emb_list)
        sims = cosine_similarity(arr, detected_emb.reshape(1, -1)).reshape(-1)
        top = float(np.max(sims))
        if top > best_score:
            best_score, best_id = top, sid
    if best_score >= threshold:
        return best_id, best_score
    return None, best_score


# ----------------------------
# Class Photo Attendance Processing
# ----------------------------
def process_class_photo(img_bytes: bytes, save_path: str, threshold=0.55, min_face_size=60):
    """
    Detect faces in class photo, match with DB embeddings,
    and update attendance (1 record per day, with bbox).
    """
    import datetime
    today = str(datetime.date.today())

    # Decode image
    arr = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    faces = face_app.get(img)

    # Build DB of known embeddings (by roll no)
    known_db = {}
    for doc in photos_col.find():
        roll = str(doc["roll"])  # ensure string
        emb = np.array(doc["embedding"], dtype=np.float32)
        known_db.setdefault(roll, []).append(emb)

    present_rolls = {}
    detected_faces = []

    # Match each detected face
    for f in faces:
        x1, y1, x2, y2 = [int(round(v)) for v in f.bbox[:4]]
        if (x2 - x1) < min_face_size or (y2 - y1) < min_face_size:
            continue

        emb = np.array(f.embedding, dtype=np.float32)
        n = np.linalg.norm(emb)
        if n > 0:
            emb = emb / n

        roll, score = match_face(emb, known_db, threshold)
        if roll:
            present_rolls[roll] = {
                "bbox": [x1, y1, x2, y2],
                "score": score
            }
            detected_faces.append({
                "roll": roll,
                "bbox": [x1, y1, x2, y2],
                "score": score,
                "status": "present"
            })
        else:
            detected_faces.append({
                "roll": None,
                "bbox": [x1, y1, x2, y2],
                "score": None,
                "status": "unmatched"
            })

    # Build attendance list for all registered students
    students_attendance = []
    all_students = [str(s["_id"]) for s in students_col.find()]
    print(all_students, present_rolls.keys())
    for roll in all_students:
        if roll in present_rolls:
            students_attendance.append({
                "roll": roll,
                "present": True,
                "confidence": present_rolls[roll]["score"],
                "bbox": present_rolls[roll]["bbox"]
            })
        else:
            students_attendance.append({
                "roll": roll,
                "present": False,
                "confidence": None,
                "bbox": None
            })

    # Save/update attendance record for today (1 doc per date)
    attendance_doc = {
        "_id": today,
        "class_date": today,
        "class_photo": save_path,
        "students": students_attendance
    }
    attendance_col.replace_one({"_id": today}, attendance_doc, upsert=True)

    # Update cumulative attendance % for each student
    total_classes = attendance_col.count_documents({})
    for roll in all_students:
        present_count = attendance_col.count_documents({
            "students": {"$elemMatch": {"roll": roll, "present": True}}
        })
        attendance_rate = (present_count / total_classes) * 100
        students_col.update_one({"_id": roll}, {"$set": {"attendance": attendance_rate}})

    return {
        "date": today,
        "students": students_attendance,
        "detected_faces": detected_faces
    }
