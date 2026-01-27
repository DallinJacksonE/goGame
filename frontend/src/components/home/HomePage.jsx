import React from 'react';
import { Link } from 'react-router-dom';
import './HomePage.css'; // We will create this next

export default function HomePage() {
  return (
    <div className="home-container">
      <h1 className="main-title">Go (Weiqi)</h1>
      <p className="subtitle">Choose your game mode</p>

      <div className="menu-options">
        {/* Local Co-op: The game we just built (shared screen) */}
        <Link to="/local" className="menu-card">
          <h2>Local Co-op</h2>
          <p>Play against a friend on this same device.</p>
        </Link>

        {/* Local Network: LAN play (Implementation needed) */}
        <Link to="/network" className="menu-card coming-soon">
          <h2>Local Network</h2>
          <p>Host or join a game on your WiFi.</p>
        </Link>

        {/* Online: Internet play (Implementation needed) */}
        <Link to="/online" className="menu-card coming-soon">
          <h2>Online Game</h2>
          <p>Matchmaking with players worldwide.</p>
        </Link>
      </div>
    </div>
  );
}
