import './App.css';
import {createBrowserRouter,RouterProvider} from 'react-router-dom'
import RootLayout from './components/RootLayout/RootLayout';
//import AllFaculty from './components/AllFaculty/AllFaculty';
// import AllReviewfac from './components/AllReviewfac/AllReviewfac';
// import AllSDPfac from './components/AllSDPfac/AllSDPfac';
import Dashboard from './components/Dashboard/Dashboard';
import Login from './components/Login/Login';
import Profile from './components/Profile/Profile';
import Register from './components/Register/Register';
// import Review from './components/Review/Review';
// import SDP from './components/SDP/SDP';
// import TableReview from './components/TableReview/TableReview';
// import TableSDP from './components/TableSDP/TableSDP';
// import UploadRev from './components/UploadRev/UploadRev';
// import UploadSDP from './components/UploadSDP/UploadSDP';
import ManagePassword from './components/ManagePassword/ManagePassword';
import ErrorPage from './components/ErrorPage/ErrorPage';
import UploadImage from './components/UploadImage/UploadImage';
import Attendance from './components/Attendance/Attendance';
import UploadAttendance from './components/UploadAttendance/UploadAttendance';
import CheckAttendance from './components/CheckAttendance/CheckAttendance';
import TotalAttendance from './components/TotalAttendance/TotalAttendance';
function App() {
  let router = createBrowserRouter([
    {
      path:'',
      element:<RootLayout/>,
      errorElement:<ErrorPage/>,
      children:[
          // {
          // path:'',
          // element:<RootLayout/>//after login is done remove home, if user is already  logged in goto Dashboard/view all faculty or else goto login
          // },
          {
            path:'login',
            element:<Login/>
          },
          {
            path:'new-user',
            element:<Register/>
          },
          {
            path:'/student',
            children:[
              {
                path:'',
                element:<Profile/> //mainly for change password (something like setting)
              },
              {
                path:'uploadimage',
                element:<UploadImage/>
              },{
                path:'attendance',
                element:<Attendance/>
              }
              
            ]
          },
          {
            path:'/faculty', // directly send to view all faculty while writing the login part
            children:[
                {
                  path:'',
                  element:<Profile/> //mainly for change password (something like setting)
                },
                {
                  path:'upload-attendance',
                  element:<UploadAttendance/>
                },
                {
                  path:'check-attendance',
                  element:<CheckAttendance/>
                },
                {
                  path:'overall-attendance',
                  element:<TotalAttendance/>
                }
            ]
          }
      ]
    }
]);
  return (
    <div>
        <RouterProvider router={router}/>
    </div>
  );
}

export default App;
