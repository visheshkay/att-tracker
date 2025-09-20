import React from 'react'
import { useSelector } from 'react-redux'
import { useNavigate } from 'react-router-dom'
import './Profile.css'

function Profile() {
    let {loginUserStatus,currentUser} = useSelector(state=>state.facultyAdminLoginReducer)
    let navigate = useNavigate();
    // const manage = ()=>{
    //     navigate('/faculty/profile/manage-password');
    // }
    return (
        <div className="profile-container">
            <div className="profile-card" style={{textAlign:'center'}}>
                <h2>Profile</h2>
                <div className="profile-info" style={{textAlign:'center'}}>
                    {currentUser.userType=='student'&& <img src={`http://127.0.0.1:8000/students/${currentUser.roll}/photo`}alt="Class"
                  className="class-photo"
                  width={120}
                /> }
                    <p><strong>Name:</strong> {currentUser.name}</p>
                    <p><strong>{currentUser.userType=='student'? <span>Roll No.</span> : <span>Id</span>}</strong> {currentUser.roll?currentUser.roll:currentUser.id}</p>
                    <p><strong>Email:</strong> {currentUser.email}</p>
                </div>
                {/* <button className="manage-password-button" onClick={manage}>Manage Password</button> */}
            </div>
        </div>
    )
}

export default Profile
