import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './components/home/HomePage';
import GoBoard from './components/goBoard/GoBoard';
import './App.css';

function App() {
  return (
    <Router>
      <Routes>
        {/* The Home Page (Menu) */}
        <Route path="/" element={<HomePage />} />

        {/* The Game Board (Local Co-op) */}
        <Route path="/local" element={<GoBoard />} />

        {/* Placeholders for future modes */}
        <Route path="/network" element={<div style={{ textAlign: 'center', marginTop: '50px' }}>Local Network Lobby (Coming Soon)</div>} />
        <Route path="/online" element={<div style={{ textAlign: 'center', marginTop: '50px' }}>Online Matchmaking (Coming Soon)</div>} />
      </Routes>
    </Router>
  );
}

export default App;
