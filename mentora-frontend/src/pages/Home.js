import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion"; // Import Framer Motion
import "../styles/Home.css";

const Home = () => {
  const [showMessage, setShowMessage] = useState(false);

  // This effect will show the message box immediately after the page loads (0 seconds delay)
  useEffect(() => {
    setShowMessage(true); // Show the message right away
  }, []);

  return (
    <div className="home-container">
      <header className="hero-section">
        <h1>Welcome to <span className="mentora-brand">Mentora</span></h1>
        <p>Your AI-powered mental health companion.</p>
        <p className="tagline">"Your mind matters. Healing begins with a conversation."</p>
        <Link to="/login" className="cta-button">
          Get Started
        </Link>
      </header>

      {/* Conditional rendering of the message box with Framer Motion */}
      {showMessage && (
        <motion.div
          className="message-box"
          initial={{ opacity: 0, scale: 0 }} // Start with no opacity and scale
          animate={{ opacity: 1, scale: 1 }} // Animate to full opacity and scale
          transition={{
            duration: 1,
            ease: "easeOut",
            scale: { type: "spring", stiffness: 100, damping: 20 }, // Make the box "bounce" in
          }}
        >
           <h3>😊 Hi! I'm your Mentora companion.</h3> {/* Added emoji before Hi! */}
          <p>I'm here to listen, support, and brighten your day!</p>
        </motion.div>
      )}

      <section className="features">
        <h2>Why Choose Mentora?</h2>
        <ul>
          <li>🧠 AI-driven mental health insights</li>
          <li>💬 Real-time supportive conversations</li>
          <li>📊 Personalized mental health reports</li>
        </ul>
      </section>

      <footer className="footer">
        <p>© 2025 Mentora. All rights reserved.</p>
      </footer>
    </div>
  );
};

export default Home;





