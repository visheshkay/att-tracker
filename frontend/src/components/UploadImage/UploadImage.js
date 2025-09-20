import React, { useState } from "react";
import axios from "axios";
import { useSelector } from 'react-redux'
import "./UploadImage.css";

function UploadImage({ roll }) {
  let {loginUserStatus,currentUser} = useSelector(state=>state.facultyAdminLoginReducer)
  const [preview, setPreview] = useState(null);
  const [file, setFile] = useState(null);
  const [msg, setMsg] = useState("");

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
        `http://127.0.0.1:8000/students/${currentUser.roll?currentUser.roll:currentUser.id}/upload_photo`,
        formData,
        { headers: { "Content-Type": "multipart/form-data" } }
      );

      setMsg(res.data.status);
    } catch (err) {
      console.error(err);
      setMsg("Upload failed");
    }
  };

  return (
    <div className="upload-container">
      <h2 className="upload-title">Upload Your Image</h2>
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
    </div>
  );
}

export default UploadImage;
