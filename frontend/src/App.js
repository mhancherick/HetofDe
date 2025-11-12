import { useState } from 'react';
import './App.css';

function App() {
  return (
    <div className="App">
      <main className="container">
        <h1>De of Het?</h1>
        <p>Type a Dutch noun to find its article</p>
        
        <input 
          type="text" 
          id="wordInput" 
          placeholder="Type a Dutch noun..."
        />
        
        <button id="searchBtn">Search</button>
        
        <div id="result"></div>
      </main>
    </div>
  );
}

export default App;