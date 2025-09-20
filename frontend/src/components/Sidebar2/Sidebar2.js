import React from 'react'
import { NavLink } from 'react-router-dom';
import './Sidebar2.css';
import { FaBars, FaTimes } from 'react-icons/fa';

function Sidebar2({ isOpen, toggleSidebar }) {
    return (
        <div className={`sidebar ${isOpen ? 'open' : 'closed'}`}>
            {isOpen && (
                <div className="close-icon" onClick={toggleSidebar}>
                    <FaTimes />
                </div>
            )}
            <nav>
                <ul>
                   <li>
                                       <NavLink
                                               to="faculty/upload-attendance"
                                               end
                                               className={({ isActive }) => isActive ? 'nav-link active-link' : 'nav-link'}
                                           >
                                               Upload Attendance
                                           </NavLink>
                                       </li>
                                       <li>
                                       <NavLink
                                               to="faculty/check-attendance"
                                               end
                                               className={({ isActive }) => isActive ? 'nav-link active-link' : 'nav-link'}
                                           >
                                               Datewise Attendance
                                           </NavLink>
                                       </li>
                                       <li>
                                       <NavLink
                                               to="faculty/overall-attendance"
                                               end
                                               className={({ isActive }) => isActive ? 'nav-link active-link' : 'nav-link'}
                                           >
                                               Overall Attendance
                                           </NavLink>
                                       </li>
                    
                </ul>
            </nav>
            <button className="profile-button">
                <NavLink to="faculty" className="nav-link">Profile</NavLink>
            </button>
        </div>
    )
}

export default Sidebar2
