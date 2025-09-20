import React, { useState } from "react";
import axios from "axios";
import { useSelector } from "react-redux";
import "./UploadAttendance.css";

function UploadAttendance() {
  let { currentUser } = useSelector((state) => state.facultyAdminLoginReducer);
  const [preview, setPreview] = useState(null);
  const [file, setFile] = useState(null);
  const [msg, setMsg] = useState("");
  const [annotated, setAnnotated] = useState(null);

  const handleFileChange = (e) => {
    const f = e.target.files[0];
    if (f) {
      setFile(f);
      setPreview(URL.createObjectURL(f));
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setMsg("Please choose a file first");
      return;
    }
    try {
      const formData = new FormData();
      formData.append("file", file);

      const res = await axios.post(
        `http://127.0.0.1:8000/teachers/upload_class_photo`,
        formData,
        { headers: { "Content-Type": "multipart/form-data" } }
      );

      setMsg("Attendance processed");
      if (res.data.annotated_image) {
        // Backend returns "storage/output/xxx.png"
        const filename = res.data.annotated_image.split("/").pop();
        setAnnotated(`http://127.0.0.1:8000/teachers/annotated/${filename}`);
      }
    } catch (err) {
      console.error(err);
      setMsg("Upload failed");
    }
  };

  return (
    <div className="upload-container">
      <h2 className="upload-title">Upload Class Attendance Image</h2>
      <label className="upload-button">
        Choose Image
        <input
          type="file"
          accept="image/*"
          onChange={handleFileChange}
          hidden
        />
      </label>

      {preview && (
        <div className="preview-box">
          <img src={preview} alt="Preview" className="preview-img" />
          <button onClick={handleUpload} className="upload-submit">
            Upload
          </button>
        </div>
      )}

      {msg && <p>{msg}</p>}

      {annotated && (
        <div className="result-box">
          <h3>Annotated Attendance Result:</h3>
          <img src={annotated} alt="Annotated Result" className="result-img" width={320}/>
        </div>
      )}
    </div>
  );
}

export default UploadAttendance;
