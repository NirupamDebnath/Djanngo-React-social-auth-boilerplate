import React from 'react';
import { BrowserRouter, Switch, Route } from 'react-router-dom';
import App from './App';
import Signup from './auth/Signup';
import Signin from './auth/Signin';
import Activate from './auth/Activate';
import PrivateRoute from './auth/PrivateRoute';
import StaffRoute from './auth/StaffRoute';
import Profile from './core/user/Profile';
import ForgotPassword from './auth/ForgotPassword';
import ResetPassword from './auth/ResetPassword';

const Routes = () => {
  return (
    <BrowserRouter>
      <Switch>
        <Route path="/" exact component={App} />
        <Route path="/signup" exact component={Signup} />
        <Route path="/signin" exact component={Signin} />
        <Route path="/forgot-password" exact component={ForgotPassword} />
        <Route path="/auth/activate/:token" exact component={Activate} />
        <Route
          path="/auth/reset-password/:token"
          exact
          component={ResetPassword}
        />
        <PrivateRoute path="/profile" exact component={Profile}></PrivateRoute>
      </Switch>
    </BrowserRouter>
  );
};

export default Routes;
