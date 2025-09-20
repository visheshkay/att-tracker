// src/components/attendance.js
import React, { useState, useEffect } from "react";
import GaugeComponent from "react-gauge-component";
import { useSelector } from 'react-redux'
import "./Attendance.css";

function isNumber(value) {
  return typeof value === 'number';
}

export default function Attendance({ initial = 85.24 }) {
  let {loginUserStatus,currentUser} = useSelector(state=>state.facultyAdminLoginReducer)
  console.log(currentUser)
  const [value, setValue] = useState(Number((isNumber(currentUser.attendance))?currentUser.attendance:initial));

  useEffect(() => {
    setValue(Number((isNumber(currentUser.attendance))?currentUser.attendance:initial));
  }, [initial]);

  return (
    <div className="attendance-page">
      <div className="attendance-card">
        <h3 className="attendance-heading">Overall Attendance</h3>

        <div className="gauge-wrap">
          <GaugeComponent
            value={value}
            type="semicircle"
            arc={{
              width: 0.2,
              padding: 0.01,
              cornerRadius: 3,
              subArcs: [
                { limit: 50, color: "#e74c3c" },   // Red
                { limit: 70, color: "#e67e22" },   // Orange
                { limit: 85, color: "#f1c40f" },   // Yellow
                { limit: 100, color: "#27ae60" }   // Green
              ],
            }}
            pointer={{
              color: "#000000",
              length: 0.8,
              width: 15,
            }}
            labels={{
              valueLabel: {
                formatTextValue: (val) => `${val.toFixed(2)}%`,
                style: { fontSize: "20px", fontWeight: "bold",color:"black" }
              },
              tickLabels: {
                type: "outer",
                ticks: [
                  { value: 0 },
                  { value: 50 },
                  { value: 70 },
                  { value: 85 },
                  { value: 100 }
                ]
              }
            }}
          />
        </div>
      </div>
    </div>
  );
}
