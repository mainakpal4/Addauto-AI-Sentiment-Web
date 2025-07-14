import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';

import Login from './components/login';
import RegisterForm from './components/RegisterForm';
import Dashboard from './components/dashboard';
import Result from './components/Result';

import { ThemeProvider } from './ThemeContext'; // ✅ Add this line

function App() {
  return (
    <ThemeProvider> {/* ✅ Wrap everything inside ThemeProvider */}
      <Router>
        <Routes>
          <Route path="/" element={<Navigate to="/register" replace />} />
          <Route path="/register" element={<RegisterForm />} />
          <Route path="/login" element={<Login />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/result" element={<Result />} />
        </Routes>
      </Router>
    </ThemeProvider>
  );
}

export default App;
