from pydantic import BaseModel
from typing import List, Optional

class StudentRegister(BaseModel):
    roll: str
    name: str
    email: str
    password: str
    attendance: float = 0.0

class TeacherRegister(BaseModel):
    id: str
    name: str
    email: str
    password: str

class LoginRequest(BaseModel):
    roll: str
    password: str

class AttendanceRecord(BaseModel):
    roll: str
    class_date: str
    present: bool
    confidence: float
