import React, { useState, useEffect } from "react";
import { detectAttack } from "./api";
import "./index.css";

function App() {
  const [text, setText] = useState("");
  const [response, setResponse] = useState(null);
  const [hearts, setHearts] = useState([]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const data = await detectAttack(text);
    setResponse(data);
  };

  useEffect(() => {
    console.log("Creating a new heart...");
    const interval = setInterval(() => {
      const newHeart = {
        id: Math.random(),
        left: `${Math.random() * 100}vw`,
        size: `${Math.random() * 20 + 10}px`, // Hearts between 10px-30px
        duration: `${Math.random() * 3 + 2}s`, // 2s - 5s duration
      };

      setHearts((prevHearts) => [...prevHearts, newHeart]);

      setTimeout(() => {
        setHearts((prevHearts) => prevHearts.filter((h) => h.id !== newHeart.id));
      }, 5000);
    }, 500); // Creates a new heart every 500ms

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="app">
      {/* Floating Hearts Container */}
      <div className="heart-container">
        {hearts.map((heart) => (
          <div
            key={heart.id}
            className="heart"
            style={{
              left: heart.left,
              width: heart.size,
              height: heart.size,
              animationDuration: heart.duration,
            }}
          ></div>
        ))}
      </div>

      {/* Main UI */}
      <div className="container">
        <h1>🩷 Social Engineering Detection 🩷</h1>
        <form onSubmit={handleSubmit}>
          <textarea
            className="heart-textarea"
            rows="4"
            cols="50"
            placeholder="💬 Enter a message to check..."
            value={text}
            onChange={(e) => setText(e.target.value)}
          ></textarea>
          <br />
          <button className="heart-button" type="submit">
            💗 Check Message 💗
          </button>
        </form>

        {response && (
          <div className="response-box">
            <h3>Risk Level: {response.risk}</h3>
            <p>{response.message}</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
