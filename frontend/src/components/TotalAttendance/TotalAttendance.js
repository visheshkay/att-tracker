import { useState, useEffect } from "react";
import axios from "axios";
import "./TotalAttendance.css";

function TotalAttendance() {
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchAttendance = async () => {
      try {
        const res = await axios.get("http://127.0.0.1:8000/teachers/attendance/all");
        if (res.data && res.data.students) {
          setStudents(res.data.students);
        }
      } catch (err) {
        console.error(err);
        setError("Failed to fetch attendance");
      } finally {
        setLoading(false);
      }
    };

    fetchAttendance();
  }, []);

  return (
    <div className="container">
      <div className="content-box">
        <h1>📅 Total Student Attendance</h1>

        {loading ? (
          <p>Loading attendance...</p>
        ) : error ? (
          <p style={{ color: "red" }}>{error}</p>
        ) : (
          <table className="attendance-table">
            <thead>
              <tr>
                <th>Roll No</th>
                <th>Name</th>
                <th>Attendance (%)</th>
              </tr>
            </thead>
            <tbody>
              {students.map((student) => (
                <tr key={student._id}>
                  <td>{student.roll}</td>
                  <td>{student.name}</td>
                  <td>{student.attendance?.toFixed(2) ?? "0.00"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}

export default TotalAttendance;
