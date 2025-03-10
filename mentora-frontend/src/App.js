import React from "react";
import { BrowserRouter as Router, Route, Routes, Navigate } from "react-router-dom";
import Login from "./components/Login";
import Signup from "./components/Signup";
import Chat from "./components/Chat";
import SentimentAnalysis from "./components/sa";
import Navbar from "./pages/Navbar";
import Home from "./pages/Home";

const App = () => {
    // Check if the user is logged in
    const isLoggedIn = localStorage.getItem("token");
  
    return (
      <Router>
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          
          {/* If logged in, navigate to Chat, otherwise to Login */}
          <Route
            path="/login"
            element={ <Login />}
          />
          
          {/* If logged in, navigate to Chat, otherwise to Signup */}
          <Route
            path="/signup"
            element={<Signup />}
          />
          
          {/* If not logged in, redirect to Signup page */}
          <Route
            path="/chat"
            element={isLoggedIn ? <Chat /> : <Navigate to="/signup" />}
          />

          <Route
           path="/sentiment-analysis" element={<SentimentAnalysis />} />  
        </Routes>
      </Router>
    );
  };
  
  export default App;
  
  