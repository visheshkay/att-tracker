# NE01_LIMIT-BREAKERS

# 🎯 AutoMark: Intelligent Attendance Tracker

This project is a **Face Recognition–based Student Attendance System** built for **Neurax Hackathon** 🏆.  
It automates student attendance by detecting and recognizing faces from class photos, eliminating manual roll calls.  

We used **FastAPI** for the backend, **React.js** for the frontend, and **InsightFace (antelopev2)** model for high-accuracy face embeddings.  
Attendance data is stored in **MongoDB**, with annotated class photos and per-student attendance reports generated automatically.

---


## 📂 Project Structure

```bash
att-tracker/
├── backend/
│   ├── main.py                # FastAPI entrypoint
│   ├── database.py            # MongoDB connection
│   ├── face_service.py        # Face detection & embedding logic
│   ├── routers/
│   │   ├── students.py        # Student registration, login, upload face
│   │   ├── teachers.py        # Teacher login, upload class photo, reports
│   ├── storage.py             # File storage utilities
│   ├── storage/
│   │   ├── students/          # Each student folder with face.jpg
│   │   │   ├── 22071A0549/
│   │   │   │   └── face.jpg
│   │   │   ├── 22071A0550/
│   │   │   │   └── face.jpg
│   │   ├── class_photos/      # Uploaded classroom images
│   │   └── output/            # Annotated class photos
│   └── requirements.txt       # Backend dependencies
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── redux/
│   │   └── App.js
│   ├── package.json
│
└── README.md


---

## ⚙️ Tech Stack

- **Backend:** FastAPI (Python), MongoDB (Atlas/Local), InsightFace (antelopev2 model), OpenCV, NumPy, Pandas
- **Frontend:** React.js (CRA), Redux Toolkit, Axios
- **Models Used:**
  - [InsightFace – antelopev2](https://github.com/deepinsight/insightface)
    - Face detection & recognition
    - Cosine similarity matching
  - ONNX Runtime for model inference

---

## 🚀 Setup Instructions

### 1️⃣ Backend

```bash
cd backend
# Create virtual environment
python -m venv venv
source venv/bin/activate    # Mac/Linux
venv\Scripts\activate       # Windows

# Install dependencies
pip install -r requirements.txt

# Run FastAPI server
uvicorn main:app --reload

cd frontend
npm install
npm start

3️⃣ MongoDB Setup

Create a MongoDB database (att-tracker).

Collections used:

students → student details, roll, attendance %

teachers → teacher login

photos → per-student face embeddings

attendance → daily class attendance

Update your database.py with the MongoDB connection string.

📸 Workflow

Student Registration

Register via frontend (roll no, email, password).

Upload face photo → embeddings generated via antelopev2.

Stored in students/{roll}/face.jpg + MongoDB photos collection.

Teacher Uploads Class Photo

Teacher uploads class photo.

All faces detected → embeddings matched with DB.

Daily attendance record stored (one document per date).

Annotated output image generated (storage/output/date_output.png).

Reports

Attendance % automatically updated for each student.

View:

Total Attendance → shows overall %

Daily Attendance → shows Present/Absent for given date

🔑 API Endpoints
Students

POST /students/register → Register new student

POST /students/login → Login

POST /students/{roll}/upload_photo → Upload face photo

GET /students/{roll}/photo → Fetch stored profile photo

Teachers

POST /teachers/register → Register new teacher

POST /teachers/login → Login

POST /teachers/upload_class_photo → Upload class photo & mark attendance

GET /teachers/attendance/all → Get overall attendance summary

GET /teachers/attendance/{date} → Get attendance by date

GET /teachers/annotated/{filename} → Serve annotated output image

🧠 Face Recognition Details

Model: InsightFace antelopev2

Features:

Face detection + embedding extraction

Normalized 512-D embedding vectors

Cosine similarity threshold: 0.55

Steps:

Preprocess face image

Extract embedding

Store in DB (linked to roll no)

During class photo → compare each detected face with embeddings

Mark attendance if similarity ≥ threshold

🏆 Neurax Hackathon Highlight

This project was built as part of Neurax Hackathon, a national-level hackathon that challenged us to solve real-world automation problems with AI/ML.

✨ Key Achievements:

Fully automated attendance tracking system

Real-time face detection & recognition pipeline

Integrated end-to-end system (React + FastAPI + MongoDB)

Usable by both teachers and students

Scalability tested with class-sized images (~70 faces)

This project demonstrated how AI-driven computer vision can significantly reduce manual effort in educational institutions.

👨‍💻 Contributors

Vishesh Kondaveeti, Gujjari Sai Kumar, D Balasubramanyam

Limit Breakers, Neurax Hackathon 2025