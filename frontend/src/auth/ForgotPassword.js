import React, { useState } from 'react';
import { Link, Redirect } from 'react-router-dom';
import axios from 'axios';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.min.css';

import Layout from '../core/Layout';

const ForgotPassword = () => {
  const [values, setValues] = useState({
    email: 'nirupamdebnath4@gmail.com',
    buttonText: 'Submit',
  });

  const { email, buttonText } = values;

  const handleChange = (name) => (event) => {
    setValues({ ...values, [name]: event.target.value });
  };

  const clickSubmit = (event) => {
    event.preventDefault();
    setValues({ ...values, buttonText: 'Submitting' });
    axios({
      method: 'POST',
      url: `${process.env.REACT_APP_BACKEND_API}/forgot-password/`,
      data: { email },
    })
      .then((response) => {
        setValues({ ...values, name: '', email: '', buttonText: 'Submit' });
        const data = response.data;
        toast.success(String(data[Object.keys(data)[0]]));
      })
      .catch((error) => {
        // console.log(error);
        setValues({ ...values, buttonText: 'Submit' });
        if (error.response) {
          const data = error.response.data;
          toast.error(String(data[Object.keys(data)[0]]));
        } else {
          toast.error('Can not connect to server. Probably you are offline');
        }
      });
  };

  const signupForm = () => (
    <form>
      <div className="form-group">
        <label className="text-muted">Email</label>
        <input
          onChange={handleChange('email')}
          value={email}
          type="email"
          className="form-control"
        />
      </div>
      <div>
        <button className="btn btn-block btn-primary" onClick={clickSubmit}>
          {buttonText}
        </button>
      </div>
    </form>
  );

  return (
    <Layout>
      <div className="col-md-6 offset-md-3">
        <ToastContainer />
        {/* {JSON.stringify({name,email})} */}
        <h1 className="p-5 text-center">Submit</h1>
        {signupForm()}
      </div>
    </Layout>
  );
};

export default ForgotPassword;
