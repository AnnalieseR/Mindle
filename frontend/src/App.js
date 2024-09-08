// src/App.js
import React, { useState, useEffect } from 'react';
import Word1DGraph from './Word1DGraph'; // Ensure this component renders the graph correctly
import './App.css'; // Assuming your styling is done here

const App = () => {
  const [word1] = useState('tropical');
  const [word2] = useState('canoe');
  const [correctWord] = useState('snorkelling'); // Example correct word; replace with dynamic value if needed
  const [guesses, setGuesses] = useState([]);
  const [showCorrectWord, setShowCorrectWord] = useState(false); // State to control visibility of the correct word
  const [arrow, setArrow] = useState(''); // State to control arrow direction
  const maxGuesses = 5;

  useEffect(() => {
    if (guesses.length >= maxGuesses && !guesses.map(guess => guess.word).includes(correctWord)) {
      setArrow('Better luck next time!'); 
      setShowCorrectWord(true);
      return;
    }
  }, [guesses])

  const handleAddGuess = async (guess) => {
    if (guesses.length >= maxGuesses) {
      setShowCorrectWord(true);
      return;
    }

    // Fetch the position from the backend
    const response = await fetch('http://127.0.0.1:5000/calculate-position', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ guess, word1, word2 }),
    });

    const data = await response.json();

    if (response.ok) {
      const position = data.position;

      setGuesses([...guesses, { word: guess, position }]);

      // Determine the feedback based on the correct guess
      if (guess === correctWord) {
        setArrow('Correct!'); // Remove the arrow when correct
        setShowCorrectWord(true); // Reveal the correct word when guessed correctly
      } else if (position < 0.5) {
        setArrow('→'); // Set arrow pointing right
      } else {
        setArrow('←'); // Set arrow pointing left
      }
    } 
  };

  return (
    <div className="App">
      <h1>Mindle</h1>
      <div className="graph-container">
        <div className="arrow-feedback">{arrow}</div>
        <Word1DGraph
          wordPositions={[
            { word: word1, position: 0 },
            { word: word2, position: 1 },
            { word: showCorrectWord ? correctWord : '?', position: 0.5 }, // Show '?' initially, reveal correct word when guessed correctly
            ...guesses.map((guess) => ({
              word: guess.word,
              position: guess.position,
            })),
          ]}
        />
      </div>
      <form
        onSubmit={(e) => {
          e.preventDefault();
          const guessInput = e.target.elements.guess.value.trim();
          if (guessInput) {
            handleAddGuess(guessInput);
            e.target.elements.guess.value = '';
          }
        }}
      >
        <input type="text" name="guess" placeholder="Enter your guess" disabled={guesses.length >= maxGuesses} />
        <button type="submit" disabled={guesses.length >= maxGuesses}>
          Submit Guess
        </button>
      </form>
      <p>Guesses Left: {maxGuesses - guesses.length}</p>
    </div>
  );
};

export default App;
