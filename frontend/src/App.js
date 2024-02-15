import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import Layout from "./hocs/Layout";

import Home from "./containers/pages/Home";
import Register from "./containers/pages/account/Register";
import Login from "./containers/pages/account/Login";
import UserProfile from "./containers/pages/account/UserProfile";
import Dashboard from "./containers/pages/Dashboard";
import StockPortfolio from "./containers/pages/StockPortfolio";
import DisplayOverallPortfolio from "./containers/StockTransactions/DisplayOverallPortfolio";
import DisplayOverallCryptoPortfolio from "./containers/CryptoTransactions/DisplayOverallCryptoPortfolio";
import NewsComponent from "./containers/pages/News-Section";

import { Provider } from "react-redux";
import store from "./store";
import CryptoDashboard from "./containers/pages/CryptoDashboard";
import CryptoPortfolio from "./containers/pages/CryptoPortfolio";

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
        <Route
          path="/overallportfolio"
          element={
            <Layout>
              <DisplayOverallPortfolio />
            </Layout>
          }
          />
          <Route
          path="/cryptodashboard"
          element={
            <Layout>
              <CryptoDashboard />
            </Layout>
          }
          />
          <Route
          path="/cryptoportfolio"
          element={
            <Layout>
              <CryptoPortfolio />
            </Layout>
          }
          />
          <Route
          path="/overallcryptoportfolio"
          element={
            <Layout>
              <DisplayOverallCryptoPortfolio/>
            </Layout>
          }
          />
        <Route
          path="/news"
          element={
            <Layout>
              <NewsComponent />
            </Layout>
          }
        />
      </Routes>
    </Router>
  </Provider>
);

export default App;
