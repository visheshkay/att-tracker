from fastapi import FastAPI
from routers import students, teachers
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Attendance Tracker")
origins = [
    "http://localhost:3000",  # React dev server
    "http://127.0.0.1:3000",
    # You can add production domain here later
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(students.router)
app.include_router(teachers.router)
