import React from "react";
import { Link } from "react-router-dom";
import "../styles/Navbar.css"; // Import custom CSS for Navbar styling

const Navbar = () => {
  return (
    <nav className="navbar">
      <div className="navbar-brand">
        <Link to="/" className="navbar-logo">Mentora</Link>  {/* "Mentora" text on the left */}
      </div>
      <ul className="navbar-list">
        <li className="navbar-item">
          <Link to="/" className="navbar-link">Home</Link>
        </li>
        <li className="navbar-item">
          <Link to="/login" className="navbar-link">Login</Link>
        </li>
        <li className="navbar-item">
          <Link to="/signup" className="navbar-link">Signup</Link>
        </li>
        <li className="navbar-item">
          <Link to="/Profile" className="navbar-link">Profile</Link>
        </li>
      </ul>
    </nav>
  );
};

export default Navbar;



