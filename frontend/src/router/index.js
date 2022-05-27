import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";

import Home from "../pages/Home";
import Login from "../pages/accounts/Login";
import SignUp from "../pages/accounts/SignUp";
import Activate from "../pages/accounts/Activate";
import ResetPassword from "../pages/accounts/ResetPassword";
import ResetPasswordConfirm from "../pages/accounts/ResetPasswordConfirm";

const Router = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<SignUp />} />
        <Route path="/activate/:uid/:token" element={<Activate />} />
        <Route path="/reset-password" element={<ResetPassword />} />
        <Route
          path="/password/reset/confirm/:uid/:token"
          element={<ResetPasswordConfirm />}
        />
      </Routes>
    </BrowserRouter>
  );
};

export default Router;
