import React, { useState, useEffect } from "react";
import {Link, Redirect} from 'react-router-dom';
import axios from "axios";
import jwt from "jsonwebtoken";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.min.css"

import Layout from "../core/Layout";

const Activate = ({match, history}) =>    {
    const [values, setValues] = useState({
        password1: "",
        password2: "",
        token: "",
        buttonText: "Submit"
    });
    const { password1, password2, token, buttonText} = values;

    useEffect(() => {
        let token = match.params.token;

        if (token){
            setValues({...values, token})
        }
    },[]);

    const handleChange = (name) => (event) => {
        if (document.getElementById("password2").value !== document.getElementById("password1").value){
            document.getElementById("password2").classList.add("border-danger");
            document.getElementById("password2").classList.add("border");
        }else{
            document.getElementById("password2").classList.remove("border-danger");
            document.getElementById("password2").classList.remove("border");
        }
            
        setValues({ ...values, [name]: event.target.value});
    }
    
    const clickSubmit = event => {
        event.preventDefault();
        if (document.getElementById("password2").value !== document.getElementById("password1").value){
            toast.error("Password doesn't match");
            return
        }
        setValues({ ...values, buttonText: "Submitting"});
        axios({
            method: 'POST',
            url: `${process.env.REACT_APP_BACKEND_API}/activate/${token}/`,
            data: {password: password1}
        }).then( response => {
            console.log(response);
            setValues({ ...values, password1:"", password2:"", buttonText: "Submit"});
            const data = response.data;
            toast.success(String(`Hey ${data["name"]}. User created successfully. Please sign in.`));
            setTimeout(() => {
                history.push("/signin");
            }, 5000);
        }).catch(error => {
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

    const ActivateForm = () => (
        <form>
            <div className="form-group">
                <label className="text-muted">Password</label>
                <input onChange={handleChange("password1")} value={password1} id="password1" type="password" className="form-control"/>
            </div>
            <div className="form-group">
                <label className="text-muted">Re-Enter Password</label>
                <input onChange={handleChange("password2")} value={password2} id="password2" type="password" className="form-control"/>
            </div>
            <div>
                <button className="btn btn-block btn-primary" onClick={clickSubmit}>{buttonText}</button>
            </div>
        </form>
    )

    return (
        <Layout>
            <div className="col-md-6 offset-md-3">
            <ToastContainer/>
            {/* {JSON.stringify({name,email})} */}
            <h1 className="p-5 text-center">Activate Account</h1>
            {ActivateForm()}
            </div>
        </Layout>
    )
    }

export default Activate;
