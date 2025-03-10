import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/Profile.css";

const Profile = () => {
  const [userData, setUserData] = useState({
    username: "",
    email: "",
    contact_number: "",
    birthdate: "",
  });
  const [editable, setEditable] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const navigate = useNavigate();

  // Fetch user profile data when the component loads
  useEffect(() => {
    const fetchProfileData = async () => {
      const token = localStorage.getItem("token");

      if (!token) {
        navigate("/login");
        return;
      }

      const response = await fetch("http://127.0.0.1:5000/profile", {
        method: "GET",
        headers: { "Authorization": `Bearer ${token}` },
      });

      if (response.ok) {
        const data = await response.json();
        setUserData({
          username: data.username,
          email: data.email,
          contact_number: data.contact_number,
          birthdate: data.birthdate,
        });
      } else {
        setErrorMessage("Failed to fetch user data.");
      }
    };

    fetchProfileData();
  }, [navigate]);

  // Handle profile update
  const handleUpdateProfile = async (e) => {
    e.preventDefault();
    const token = localStorage.getItem("token");

    const response = await fetch("http://127.0.0.1:5000/profile/update", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`,
      },
      body: JSON.stringify(userData),
    });

    if (response.ok) {
      alert("Profile updated successfully!");
      setEditable(false); // Disable editing after saving
    } else {
      setErrorMessage("Failed to update profile.");
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setUserData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  return (
    <div className="profile-container">
      <h2>Profile</h2>
      {errorMessage && <p className="error">{errorMessage}</p>}
      <form onSubmit={handleUpdateProfile}>
        <div>
          <label>Username:</label>
          <input
            type="text"
            name="username"
            value={userData.username}
            onChange={handleChange}
            disabled={!editable}
          />
        </div>
        <div>
          <label>Email:</label>
          <input
            type="email"
            name="email"
            value={userData.email}
            onChange={handleChange}
            disabled={!editable}
          />
        </div>
        <div>
          <label>Contact Number:</label>
          <input
            type="text"
            name="contact_number"
            value={userData.contact_number}
            onChange={handleChange}
            disabled={!editable}
          />
        </div>
        <div>
          <label>Birthdate:</label>
          <input
            type="date"
            name="birthdate"
            value={userData.birthdate}
            onChange={handleChange}
            disabled={!editable}
          />
        </div>
        {editable ? (
          <button type="submit">Save Changes</button>
        ) : (
          <button type="button" onClick={() => setEditable(true)}>
            Edit Profile
          </button>
        )}
      </form>
    </div>
  );
};

export default Profile;
