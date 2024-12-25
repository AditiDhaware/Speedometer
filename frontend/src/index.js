// Import necessary modules and components
import React from 'react'; // Core React library
import ReactDOM from 'react-dom'; // ReactDOM is used to render React components into the DOM
import App from './App'; // Import the main App component
import './index.css'; // Import the global CSS file for styling

// Render the App component into the root DOM element
ReactDOM.render(
  // Use React.StrictMode to highlight potential problems in the app
  <React.StrictMode>
    <App /> {/* The main App component is wrapped in StrictMode */}
  </React.StrictMode>,
  document.getElementById('root') // The DOM element with id 'root' is the target for rendering
);
