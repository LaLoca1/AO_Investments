import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import Layout from "./hocs/Layout";

import Home from "./containers/Home";
import Register from "./containers/Register";
import Login from "./containers/Login";
import UserProfile from "./containers/UserProfile";
import Dashboard from "./containers/Dashboard";
import StockPortfolio from "./containers/StockPortfolio";

import { Provider } from "react-redux";
import store from "./store";

const App = () => (
  <Provider store={store}>
    <Router>
      <Routes>
        <Route
          path="/"
          element={
            <Layout>
              <Home />
            </Layout>
          }
        />
        <Route
          path="/register"
          element={
            <Layout>
              <Register />
            </Layout>
          }
        />
        <Route
          path="/login"
          element={
            <Layout>
              <Login />
            </Layout>
          }
        />
        <Route
          path="/userprofile"
          element={
            <Layout>
              <UserProfile />
            </Layout>
          }
        />
        <Route
          path="/dashboard"
          element={
            <Layout>
              <Dashboard />
            </Layout>
          }
        />
        <Route
          path="/stockportfolio"
          element={
            <Layout>
              <StockPortfolio />
            </Layout>
          }
        />
      </Routes>
    </Router>
  </Provider>
);

export default App;
