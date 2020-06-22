
import React from 'react';
import  { Route, Redirect } from 'react-router-dom';
import {isAuth} from './helper';


const AdminRoute = ({component: Component, ...rest}) => (
    <Route {...rest} render={
        props => isAuth() && isAuth().is_staff === true ? <Component {...props} /> : <Redirect to={{
            pathname:"/signin",
            state: {from:props.location}
        }}/>    
    }>

    </Route>
)

export default AdminRoute;