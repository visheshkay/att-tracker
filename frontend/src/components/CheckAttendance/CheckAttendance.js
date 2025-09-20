import { useState } from "react";
import axios from "axios";
import "./CheckAttendance.css";

function CheckAttendance() {
  const [selectedDate, setSelectedDate] = useState("");
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [classPhoto, setClassPhoto] = useState(null);

  const handleChange = async (e) => {
    const date = e.target.value;
    setSelectedDate(date);

    if (!date) return;

    setLoading(true);
    setError("");
    try {
      const res = await axios.get(
        `http://127.0.0.1:8000/teachers/attendance/${date}`
      );
      if (res.data) {
        setStudents(res.data.students || []);
        setClassPhoto(res.data.class_photo || null);
      }
    } catch (err) {
      console.error(err);
      setError("No attendance record found for this date");
      setStudents([]);
      setClassPhoto(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <div className="content-box">
        <h1>📅 Student Attendance</h1>

        {/* Date Picker */}
        <input
          type="date"
          value={selectedDate}
          onChange={handleChange}
          className="date-select"
        />

        {loading && <p>Loading attendance...</p>}
        {error && <p style={{ color: "red" }}>{error}</p>}

        {!loading && !error && students.length > 0 && (
          <>
            {/* Attendance Table */}
            <table className="attendance-table">
              <thead>
                <tr>
                  <th>Roll No</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {students.map((student) => (
                  <tr key={student.roll}>
                    <td>{student.roll}</td>
                    <td
                      className={student.present ? "present" : "absent"}
                    >
                      {student.present ? "Present" : "Absent"}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>

            {/* Class Photo */}
            {classPhoto && (
              <div className="photo-preview">
                <h3 style={{marginTop:'20px'}}>Class Photo</h3>
                <img
                  src={`http://127.0.0.1:8000/teachers/files/${selectedDate}`}
                  alt="Class"
                  className="class-photo"
                  width={320}
                />
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}

export default CheckAttendance;
