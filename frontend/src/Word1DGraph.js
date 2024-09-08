// src/Word1DGraph.js
import React from 'react';

// Scale position to fit within a percentage range between min and max
const scalePosition = (position, min, max) => ((position - min) / (max - min)) * 100;

const Word1DGraph = ({ wordPositions }) => {
  // Define min and max values based on the semantic distances provided
  const minPosition = Math.min(...wordPositions.map((point) => point.position));
  const maxPosition = Math.max(...wordPositions.map((point) => point.position));

  return (
    <div style={{ position: 'relative', width: '100%', maxWidth: '800px', height: '200px', margin: '10px auto' }}>
      {/* Main Line */}
      <div
        style={{
          position: 'absolute',
          top: '50%',
          left: '0%', // Adding margins to avoid points touching the container's edges
          right: '0%',
          height: '2px',
          backgroundColor: '#000',
        }}
      ></div>

      {/* Points and Labels */}
      {wordPositions.map((point, index) => (
        <React.Fragment key={index}>
          <div
            style={{
              position: 'absolute',
              top: '48%', // Adjust position to match the line height
              left: `${scalePosition(point.position, minPosition, maxPosition)}%`,
              transform: 'translateX(-50%)',
              width: '12px',
              height: '12px',
              borderRadius: '50%',
              backgroundColor:
                point.word === 'tropical' || point.word === 'canoe'
                  ? 'blue'
                  : point.word === '?'
                  ? 'blue'
                  : point.word === 'snorkelling'
                  ? 'green'
                  : 'red', // Distinguish correct guesses
            }}
          ></div>
          <div
            style={{
              position: 'absolute',
              top: '30%', // Place labels above the circles
              left: `${scalePosition(point.position, minPosition, maxPosition)}%`,
              transform: 'translateX(-50%)',
              textAlign: 'center',
              fontSize: '14px',
              fontWeight: 'bold',
              whiteSpace: 'nowrap', // Prevent text from wrapping
            }}
          >
            {point.word}
          </div>
        </React.Fragment>
      ))}
    </div>
  );
};

export default Word1DGraph;
