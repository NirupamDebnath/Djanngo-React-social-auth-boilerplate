import React from "react";
import axios from "axios";
import GoogleLogin from "react-google-login";

const Google = ({informParent}) => {
    const responseGoogle = (response) => {
        console.log(response.tokenId);
        axios({
            method:"POST",
            url:`${process.env.REACT_APP_BACKEND_API}/google-login/`,
            data: {token: response.tokenId}
        })
        .then(response => {
            console.log("Google SIGNIN SUCCESS", response);
            informParent(response);
        })
        .catch(err => {
            console.log("Google Signin Error", err);
        })
    }
    return (
        <div className="pb-3">
            <GoogleLogin
                clientId={`${process.env.REACT_APP_GOOGLE_CLIENT_ID}`}
                buttonText="Login"
                onSuccess={responseGoogle}
                onFailure={responseGoogle}
                render={renderProps => (
                    <button onClick={renderProps.onClick} disabled={renderProps.disabled}
                        className='btn btn-danger btn-lg btn-block'
                    >
                        <i className="fab fa-google pr-2"/>Login with Google
                    </button>
                )}
                cookiePolicy={'single_host_origin'}
            />
        </div>
    )
}

export default Google;