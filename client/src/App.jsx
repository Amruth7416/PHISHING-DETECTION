import React, { useState, useEffect } from "react";
import { detectAttack } from "./api";
import "./App.css";

function App() {
  const [text, setText] = useState("");
  const [response, setResponse] = useState(null);

  useEffect(() => {
    const binaryContainer = document.createElement("div");
    binaryContainer.className = "binary-background";
    document.body.appendChild(binaryContainer);

    for (let i = 0; i < 50; i++) { // Increase number of binary streams
      let stream = document.createElement("div");
      stream.className = "binary-stream";
      stream.innerText = generateBinaryString();
      stream.style.left = `${Math.random() * 100}vw`; // Spread across full width
      stream.style.top = `${Math.random() * 100}vh`; // Spread across full height
      stream.style.fontSize = `${12 + Math.random() * 20}px`; // Random font size (12px - 32px)
      stream.style.animationDuration = `${3 + Math.random() * 5}s`; // Random speed (3s - 8s)
      binaryContainer.appendChild(stream);
    }
  }, []);

  const generateBinaryString = () => {
    let str = "";
    for (let i = 0; i < 30; i++) { // More characters per stream
      str += Math.random() > 0.5 ? "1 " : "0 ";
    }
    return str;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const data = await detectAttack(text);
    setResponse(data);
  };

  return (
    <div className="container">
      <h1>Social Engineering Attack Detection</h1>
      <form onSubmit={handleSubmit}>
        <textarea
          rows="4"
          cols="50"
          placeholder="Enter a message to check..."
          value={text}
          onChange={(e) => setText(e.target.value)}
        ></textarea>
        <br />
        <button type="submit">Check Message</button>
      </form>
      {response && (
        <div className="response-box">
          <h3>Risk Level: {response.risk}</h3>
          <p>{response.message}</p>
        </div>
      )}
    </div>
  );
}

export default App;
