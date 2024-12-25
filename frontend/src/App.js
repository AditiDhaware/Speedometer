// Import necessary React and third-party libraries
import React, { useState, useEffect } from 'react'; // React hooks for state and lifecycle management
import Speedometer from 'react-d3-speedometer'; // A library for rendering a speedometer component
import io from 'socket.io-client'; // Socket.IO client for real-time communication with the backend

// Initialize a Socket.IO connection to the backend server
const socket = io('http://localhost:5000'); // Replace 'http://localhost:5000' with the actual backend URL if different

// Main App component
function App() {
  // Declare a state variable to store the current speed value
  const [speed, setSpeed] = useState(0); // Initial speed is set to 0

  // useEffect hook to handle real-time updates from the backend
  useEffect(() => {
    // Listen for the 'speed_update' event emitted by the backend
    socket.on('speed_update', (data) => {
      setSpeed(data.speed); // Update the speed state with the new value received from the backend
    });

    // Cleanup function to remove the event listener when the component is unmounted
    return () => socket.off('speed_update');
  }, []); // Empty dependency array ensures this effect runs only once when the component mounts

  return (
    // Main container for the app with inline styles for centering
    <div style={{ textAlign: 'center', marginTop: '50px' }}>
      {/* App title */}
      <h1>Real-Time Speedometer</h1>

      {/* Speedometer component */}
      <Speedometer
        value={speed} // Current speed value to display on the speedometer
        minValue={0} // Minimum speed on the scale
        maxValue={120} // Maximum speed on the scale
        segments={10} // Number of segments in the speedometer
        needleColor="red" // Color of the speedometer needle
        startColor="green" // Color for the start of the speed range
        endColor="red" // Color for the end of the speed range
        textColor="black" // Color of the text on the speedometer
      />

      {/* Display the current speed below the speedometer */}
      <p>Current Speed: {speed} km/h</p>
    </div>
  );
}

// Export the App component as the default export
export default App;
