import React, { useState } from "react";

const SentimentAnalysis = () => {
  const [report, setReport] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  // Function to fetch sentiment report
  const fetchSentimentReport = async () => {
    try {
      setLoading(true);
      setError("");
      setReport("");

      const token = localStorage.getItem("token"); // Get JWT token
      if (!token) {
        setError("User not authenticated");
        setLoading(false);
        return;
      }

      console.log("Sending Token:", token); // Debugging

      const response = await fetch("http://127.0.0.1:5000/analyze_sentiment", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`, // Send JWT
        },
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.error || "Error fetching sentiment report");
      }

      setReport(data.sentiment_report);
    } catch (err) {
      setError(err.message);
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  // Function to download sentiment report
  const downloadSentimentReport = async () => {
    try {
      const token = localStorage.getItem("token");
      if (!token) {
        setError("User not authenticated");
        return;
      }

      const response = await fetch("http://127.0.0.1:5000/download_report", {
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        throw new Error("Error downloading report");
      }

      // Convert response to blob and create a download link
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "Sentiment_Report.pdf";
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
    } catch (err) {
      setError(err.message);
      console.error(err);
    }
  };

  return (
    <div style={styles.container}>
      <h2 style={styles.heading}>Sentiment Analysis Report</h2>
      <p style={styles.description}>Click below to generate your sentiment report.</p>

      <div style={styles.buttonContainer}>
        <button onClick={fetchSentimentReport} style={styles.button} disabled={loading}>
          {loading ? "Fetching... It may take 30-60 seconds" : "Get Report"}
        </button>
        
        <button onClick={() => window.open("http://127.0.0.1:5000/download_report", "_blank")} style={styles.button}>
        Download Report
        </button>
      </div>

      {error && <p style={styles.error}>{error}</p>}
      {report && (
        <div style={styles.reportBox}>
          <h3>Your Sentiment Report:</h3>
          <div style={styles.reportText}>
            {report.split("\n").map((line, index) => (
              line.trim() !== "" && <p key={index}>{line.trim()}</p>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

// Inline Styles
const styles = {
  container: { textAlign: "center", maxWidth: "500px", margin: "auto", padding: "20px" },
  heading: { fontSize: "24px", fontWeight: "bold" },
  description: { color: "#555", marginBottom: "10px" },
  buttonContainer: { display: "flex", justifyContent: "center", gap: "10px", marginBottom: "15px" },
  button: {
    backgroundColor: "#007bff",
    color: "#fff",
    padding: "10px 15px",
    border: "none",
    cursor: "pointer",
    borderRadius: "5px",
  },
  downloadButton: {
    backgroundColor: "#28a745",
    color: "#fff",
    padding: "10px 15px",
    border: "none",
    cursor: "pointer",
    borderRadius: "5px",
  },
  error: { color: "red", marginTop: "10px" },
  reportBox: { backgroundColor: "#f4f4f4", padding: "15px", marginTop: "15px", borderRadius: "5px", textAlign: "left" },
  reportText: {
    fontSize: "16px",
    lineHeight: "1.6",
    marginBottom: "8px",
  },  
};

export default SentimentAnalysis;
