from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017"
client = MongoClient(MONGO_URI)
db = client["automark"]

# Collections
students_col = db["students"]
teachers_col = db["teachers"]
photos_col = db["photos"]
attendance_col = db["attendance"]
