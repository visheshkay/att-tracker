import React from 'react';
import { NavLink } from 'react-router-dom';
import './Sidebar.css';
import { FaBars, FaTimes } from 'react-icons/fa';

function Sidebar({ isOpen, toggleSidebar }) {
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
                            to="student/uploadimage"
                            end
                            className={({ isActive }) => isActive ? 'nav-link active-link' : 'nav-link'}
                        >
                            Upload Profile Image
                        </NavLink>
                    </li>
                    <li>
                    <NavLink
                            to="student/attendance"
                            end
                            className={({ isActive }) => isActive ? 'nav-link active-link' : 'nav-link'}
                        >
                            Attendance
                        </NavLink>
                    </li>
                   
                   
                    
                </ul>
            </nav>
            <button className="profile-button">
                <NavLink to="student" className="nav-link">Profile</NavLink>
            </button>
        </div>
    );
}

export default Sidebar;
