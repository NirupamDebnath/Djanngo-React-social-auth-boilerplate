import React, {Fragment} from "react";
import { Link, withRouter } from "react-router-dom";
import { isAuth, signout } from "../auth/helper";

const Layout = ({children,match, history}) => {
    const isActive = path => {
        if(match.path === path){
            return "nav-item active";
        }
        return "nav-item";
    }
    const retutnName = user =>{
        if (user.name){
            return user.name;
        }
        return "Profile"
    }
    const nav = () => (
        <nav className = "navbar navbar-expand-sm navbar-light bg-light sticky-top">
            <div className="container">
                <Link to="/" className="navbar-brand">Logo</Link>
                <button className="navbar-toggler" data-toggle="collapse" data-target="#navbarCollapse">
                <span className="navbar-toggler-icon"></span>
                </button>
                <div className="collapse navbar-collapse" id="navbarCollapse">
                    <ul className="navbar-nav ml-auto">
                        <li className={isActive('/')}>
                            <Link to="/" className="nav-link">Home</Link>
                        </li>
                        {!isAuth() && (
                            <Fragment>
                                <li className={isActive('/signup')}>
                                    <Link to="/signup" className="nav-link">Signup</Link>
                                </li>
                                <li className={isActive('/signin')}>
                                    <Link to="/signin" className="nav-link">Signin</Link>
                                </li>
                            </Fragment>
                        )}
                        {isAuth() && (
                            <Fragment>
                                <li className={isActive('/profile')}>
                                    <Link to="/profile" className="nav-link">{retutnName(isAuth())}</Link>
                                </li>
                                <li className="nav-item">
                                    <span style={{cursor: "pointer"}} className="nav-link" onClick={()=>{
                                        signout(()=>{
                                            history.push('/');
                                        });
                                    }}>Signout</span>
                                </li>
                            </Fragment>
                        )}
                    </ul>
                </div>
            </div>
            {/* {JSON.stringify(history)} */}
        </nav>
    )
    return (
        <Fragment>
            {nav()}
            <div className="container">
                {children}
            </div>
        </Fragment>
    )
}

export default withRouter(Layout);