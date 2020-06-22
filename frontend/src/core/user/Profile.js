import React, { useState, useEffect } from "react";
import Layout from "../Layout";
import axios from "axios";
import { ToastContainer, toast } from "react-toastify";
import 'react-toastify/dist/ReactToastify.min.css';
import { isAuth, getCookie, signout, updateUserInfo, getLocalStorage } from "../../auth/helper";


const Private = ({history}) => {
    const [values, setValues] = useState({
        name:'',
        email:'',
        password:'',
        buttonText:'Submit'
    });

    const token = getCookie("token");

    useEffect(() => {
        loadProfile()
    },[])
    

    const loadProfile = () => {
        axios({
            method: 'GET',
            url: `${process.env.REACT_APP_BACKEND_API}/profile/${JSON.parse(getLocalStorage("user")).id}/`,
            headers: {
                Authorization: `Bearer ${token}`
            }
        })
        .then(response => {
            console.log("Profile update", response);
            const {name, email} = response.data;
            setValues({...values, name, email})
        })
        .catch(error => {
            // console.log(error);
            setValues({ ...values, buttonText: "Submit"});
            if (error.response){
                const data = error.response.data;
                toast.error(String(data[Object.keys(data)[0]]));
            }
            else{
                toast.error("Can not connect to server. Probably you are offline");
            }
        })

    }
    
    const { name, email, password, buttonText} = values

    const handleChange = (name) => (event) => {
        setValues({...values, [name]: event.target.value})
    }

    const clickSubmit = event => {
        event.preventDefault();
        setValues({...values, buttonText: 'Submitting ...'})
        axios({
            method: 'PATCH',
            url: `${process.env.REACT_APP_BACKEND_API}/profile/${JSON.parse(getLocalStorage("user")).id}/`,
            data: { name, password},
            headers: {
                Authorization: `Bearer ${token}`
            }
        })
        .then( response => {
            console.log("PROFILE UPDATE SUCCESS", response);
            updateUserInfo(response,() => {
                setValues({...values, buttonText: 'Submit'});
                toast.success("Profile updated successfully");
            });
        })
        .catch(error => {
            // console.log(error);
            setValues({ ...values, buttonText: "Submit"});
            if (error.response){
                const data = error.response.data;
                toast.error(String(Object.keys(data)[0])+" : "+String(data[Object.keys(data)[0]]));
            }
            else{
                toast.error("Can not connect to server. Probably you are offline");
            }
        })

    }

    const updateForm = () => (
        <form>
            <div className="form-grop">
                <label className="text-muted">Name</label>
                <input onChange={handleChange('name')} value={name} type="text" className="form-control"/>
            </div>

            <div className="form-grop">
                <label className="text-muted">Email</label>
                <input defaultValue={email} type="text" className="form-control" disabled/>
            </div>

            <div className="form-grop">
                <label className="text-muted">Password</label>
                <input onChange={handleChange('password')} autoComplete="off" value={password} type="password" className="form-control"/>
            </div>

            <div>
                <button className="btn btn-primary mt-4" onClick={clickSubmit}>{buttonText}</button>
            </div>
        </form>
    )

    return(
        <Layout>
            <div className="col-md-6 offset-md-3">
                <ToastContainer />
                <h1>Profile Update</h1>
                {updateForm()}
            </div>
        </Layout>
    )
};

export default Private;