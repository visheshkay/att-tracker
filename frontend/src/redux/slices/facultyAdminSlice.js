import { createSlice,createAsyncThunk } from "@reduxjs/toolkit";
import axios from 'axios'
export const facultyAdminLoginThunk=createAsyncThunk('faculty-admin-login',async (userCredObj, thunkApi) => {
    try {
      if (userCredObj.userType === "student") {
        const dbRes = await axios.post(
          "http://127.0.0.1:8000/students/login",
          userCredObj
        );
        if (dbRes.data.status === "login successful") {
          return dbRes.data;
        } else {
          return thunkApi.rejectWithValue(dbRes.data.message);
        }
      }

      if (userCredObj.userType === "faculty") {
        const dbRes = await axios.post(
          "http://127.0.0.1:8000/teachers/login",
          userCredObj
        );
        if (dbRes.data.status === "login successful") {
          return dbRes.data;
        } else {
          return thunkApi.rejectWithValue(dbRes.data.message);
        }
      }
    } catch (err) {
      return thunkApi.rejectWithValue(err.message || "Login failed");
    }
  })
export const facultyAdminSlice=createSlice({
    name:"faculty-admin-login",
    initialState:{
        isPending:false,
        loginUserStatus:false,
        currentUser:{},
        errorOccured:false,
        errMsg:''
    },
    reducers:{
        resetState:(state,action)=>{
            state.isPending=false
            state.loginUserStatus=false
            state.currentUser={}
            state.errorOccured=false
            state.errMsg=''
        }
    },
    extraReducers:builder=>builder
    .addCase(facultyAdminLoginThunk.pending,(state,action)=>{
        state.isPending=true;
    })
    .addCase(facultyAdminLoginThunk.fulfilled,(state,action)=>{
        state.isPending=false;
        state.currentUser=action.payload.user
        state.loginUserStatus=true
        state.errorOccured=false
        state.errMsg=''

    })
    .addCase(facultyAdminLoginThunk.rejected,(state,action)=>{
        state.isPending=false;
        state.currentUser={}
        state.loginUserStatus=false
        state.errorOccured=true
        state.errMsg=action.payload
    }),
})

export const {resetState}=facultyAdminSlice.actions
export default facultyAdminSlice.reducer;