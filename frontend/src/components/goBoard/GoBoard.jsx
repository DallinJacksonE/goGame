import React, { useState, useEffect } from 'react';
import './GoBoard.css';

const BOARD_SIZE = 9;

export default function GoBoard() {
  const [board, setBoard] = useState(Array(BOARD_SIZE).fill(Array(BOARD_SIZE).fill(null)));
  const [turn, setTurn] = useState('black');
  const [captured, setCaptured] = useState({ black: 0, white: 0 });
  const [message, setMessage] = useState('');

  useEffect(() => {
    fetchGameState();
  }, []);

  const fetchGameState = async () => {
    try {
      const res = await fetch('/api/stateCoop');
      const data = await res.json();
      updateLocalState(data);
    } catch (err) {
      console.error(err);
      setMessage("Error connecting to server");
    }
  };

  const updateLocalState = (data) => {
    if (!data) return;
    //These need to match the data names set in the python game code
    setBoard(data.board);

    setTurn(data.currentTurn);

    setCaptured(data.captured);
  };

  const handleMove = async (x, y) => {
    try {
      const res = await fetch('/api/moveCoop', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ x, y })
      });

      const data = await res.json();

      if (data.success) {
        updateLocalState(data.game_state || data.gameState);
        setMessage('');
      } else {
        setMessage(data.message);
      }
    } catch (err) {
      setMessage("Failed to send move");
    }
  };

  const handleReset = async () => {
    try {
      const res = await fetch('/api/resetCoop', { method: 'POST' });
      const data = await res.json();
      updateLocalState(data);
      setMessage('');
    } catch (err) {
      setMessage("Failed to reset game");
    }
  };

  return (
    <div className="go-container">
      <h1>Go (9x9)</h1>

      <div className="info-panel">
        <div>
          {/* 5. Safety Check: Prevents crash if turn is null */}
          Turn: <strong>{turn ? turn.charAt(0).toUpperCase() + turn.slice(1) : 'Loading...'}</strong>
        </div>
        <div>Black Captured: {captured ? captured.black : 0}</div>
        <div>White Captured: {captured ? captured.white : 0}</div>
      </div>

      <div className="board">
        {board.map((row, y) => (
          row.map((cellValue, x) => (
            <div
              key={`${x}-${y}`}
              className="cell"
              onClick={() => handleMove(x, y)}
            >
              {cellValue && (
                <div className={`stone ${cellValue}`}></div>
              )}

              {!cellValue && (
                <div
                  className="ghost"
                  style={{ backgroundColor: turn === 'white' ? 'white' : 'black' }}
                ></div>
              )}
            </div>
          ))
        ))}
      </div>

      <div className="error-msg">{message}</div>
      <button className="reset-btn" onClick={handleReset}>New Game</button>
    </div>
  );
}
