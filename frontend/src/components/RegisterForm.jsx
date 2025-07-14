import React, { useState, useRef } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import '../styles/RegisterForm.css';

const RegisterForm = () => {
  const [darkMode, setDarkMode] = useState(true);
  const [email, setEmail] = useState('');
  const [emailError, setEmailError] = useState('');
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    interest: '',
  });

  const navigate = useNavigate();
  const formRef = useRef(null);

  const handleToggle = () => setDarkMode(!darkMode);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleEmailChange = (e) => {
    const value = e.target.value;
    setEmail(value);
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    setEmailError(emailRegex.test(value) ? '' : 'Please enter a valid email address.');
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (emailError) {
      alert('Fix the errors before submitting.');
      return;
    }

    localStorage.setItem('userData', JSON.stringify(formData));
    alert(`Welcome ${formData.name}! You're all set for sentiment prediction.`);
    navigate('/dashboard');
    formRef.current.reset();
  };

  return (
    <div className={`register-container ${darkMode ? 'dark' : 'light'}`}>
      <button className="theme-toggle" onClick={handleToggle}>
        {darkMode ? '☀️ Light' : '🌙 Dark'}
      </button>

      <div className="form-container">
        <h2 className="form-title">Register for Sentiment Insights</h2>
        <form ref={formRef} onSubmit={handleSubmit}>
          <input name="name" placeholder="Full Name" onChange={handleChange} required />
          <input type="email" name="email" placeholder="Email Address" onChange={handleEmailChange} required />
          {emailError && <p className="error">{emailError}</p>}
          <input type="password" name="password" placeholder="Password" onChange={handleChange} required />
          <input name="interest" placeholder="Interests (e.g., AI, NLP)" onChange={handleChange} />
          <button type="submit" className="register-button">Register</button>
        </form>
        <p className="form-footer">Already have an account? <Link to="/login">Login</Link></p>
      </div>
    </div>
  );
};

export default RegisterForm;