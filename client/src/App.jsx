import React, { useState, useEffect } from "react";
import { detectAttack } from "./api";
import "./App.css";

function App() {
  const [text, setText] = useState("");
  const [response, setResponse] = useState(null);
  const [mode, setMode] = useState("email"); 
  const [error, setError] = useState(""); 

  useEffect(() => {
    const binaryContainer = document.createElement("div");
    binaryContainer.className = "binary-background";
    document.body.appendChild(binaryContainer);

    for (let i = 0; i < 50; i++) {
      let stream = document.createElement("div");
      stream.className = "binary-stream";
      stream.innerText = generateBinaryString();
      stream.style.left = `${Math.random() * 100}vw`;
      stream.style.top = `${Math.random() * 100}vh`;
      stream.style.fontSize = `${12 + Math.random() * 20}px`;
      stream.style.animationDuration = `${3 + Math.random() * 5}s`;
      binaryContainer.appendChild(stream);
    }
  }, []);

  const generateBinaryString = () => {
    let str = "";
    for (let i = 0; i < 30; i++) {
      str += Math.random() > 0.5 ? "1 " : "0 ";
    }
    return str;
  };

  const validateInput = () => {
    if (!text.trim()) {
      setError("Input cannot be empty.");
      return false;
    }
    
    if (mode === "website" && !/^(https?:\/\/)?([\w\d-]+\.)+[\w]{2,}(\/.*)?$/.test(text)) {
      setError("Invalid website URL format.");
      return false;
    }

    if (mode === "email" && text.includes("http")) {
      setError("Email content should not be a URL.");
      return false;
    }    

    setError(""); 
    return true;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validateInput()) return; 

    const data = await detectAttack(text, mode);
    setResponse(data);
  };

  return (
    <div className="container">
      <h1>Social Engineering Attack Detection</h1>
      <form onSubmit={handleSubmit}>
        <select value={mode} onChange={(e) => setMode(e.target.value)}>
          <option value="email">Email</option>
          <option value="phishing_phrases">Phishing Phrases</option>
          <option value="website">Website URLs</option>
        </select>
        <textarea
          rows="4"
          cols="50"
          placeholder={
            mode === "email"
              ? "Enter an email to check..."
              : mode === "phishing_phrases"
              ? "Enter a phrase to check..."
              : "Enter a website URL to check..."
          }
          value={text}
          onChange={(e) => setText(e.target.value)}
        ></textarea>
        <br />
        {error && <p className="error">{error}</p>}
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
