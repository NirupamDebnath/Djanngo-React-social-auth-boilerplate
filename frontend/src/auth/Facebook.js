import React from "react";
import axios from "axios";
import FacebookLogin from 'react-facebook-login/dist/facebook-login-render-props';

const Facebook = ({informParent}) => {
    const responseFacebook = (response) => {
        console.log(response);
        axios({
            method:"POST",
            url:`${process.env.REACT_APP_BACKEND_API}/facebook-login/`,
            data: {
                userID: response.userID,
                accessToken: response.accessToken
            }
        })
        .then(response => {
            console.log("Facebook SIGNIN SUCCESS", response);
            informParent(response);
        })
        .catch(err => {
            console.log("Facebook Signin Error", err);
        })
    }
    return (
        <div className="pb-3">
            <FacebookLogin
                appId={`${process.env.REACT_APP_FACEBOOK_APP_ID}`}
                autoLoad = {false}
                callback={responseFacebook}
                render={renderProps => (
                    <button 
                        onClick={renderProps.onClick} 
                        className='btn btn-primary btn-lg btn-block'
                    >
                        <i className="fab fa-facebook pr-2"/>Login with Facebook
                    </button>
                )}
            />
        </div>
    )
}

export default Facebook;