# Import required modules
from flask import Flask, jsonify  # Flask for building the web server and jsonify for API responses
from flask_socketio import SocketIO, emit  # SocketIO for real-time communication
import mysql.connector  # MySQL connector for interacting with the database
import random  # For generating random speed values
import threading  # For running background threads
import time  # To control the simulation frequency

# Initialize the Flask application and SocketIO for real-time updates
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")  # Enable CORS for cross-origin requests

# MySQL database configuration
db_config = {
    'host': 'localhost',  # Use 'db' as the hostname when running in Docker
    'user': 'root',  # Database username
    'password': 'root',  # Database password
    'database': 'speedometer_db'  # Database name
}

# Function to insert speed data into the database
def insert_speed_data(speed):
    """
    Inserts a speed value into the speed_data table in the MySQL database.

    Parameters:
    - speed (float): The speed value to be inserted.
    """
    conn = mysql.connector.connect(**db_config)  # Connect to the database
    cursor = conn.cursor()
    cursor.execute("INSERT INTO speed_data (speed) VALUES (%s)", (speed,))  # Insert the speed value
    conn.commit()  # Commit the transaction
    cursor.close()  # Close the cursor
    conn.close()  # Close the connection

# Function to fetch the latest speed value from the database
def get_latest_speed():
    """
    Retrieves the most recent speed value from the speed_data table.

    Returns:
    - float: The latest speed value, or 0 if no data is found.
    """
    conn = mysql.connector.connect(**db_config)  # Connect to the database
    cursor = conn.cursor()
    cursor.execute("SELECT speed FROM speed_data ORDER BY id DESC LIMIT 1")  # Get the latest speed value
    result = cursor.fetchone()  # Fetch the result
    cursor.close()  # Close the cursor
    conn.close()  # Close the connection
    return result[0] if result else 0  # Return the speed value or 0 if no data is found

# Function to simulate sensor data and send it to clients in real-time
def simulate_sensor_data():
    """
    Simulates the generation of sensor data (speed values) and emits the data to connected clients.
    Also inserts the generated data into the database.
    """
    while True:  # Run indefinitely
        speed = round(random.uniform(0, 120), 2)  # Generate a random speed between 0 and 120 km/h
        insert_speed_data(speed)  # Insert the generated speed into the database
        socketio.emit('speed_update', {'speed': speed})  # Emit the speed to connected clients
        time.sleep(1)  # Wait for 1 second before generating the next value

# Start the sensor simulation in a background thread
threading.Thread(target=simulate_sensor_data, daemon=True).start()

# API endpoint to get the latest speed value
@app.route('/api/speed', methods=['GET'])
def get_speed():
    """
    API endpoint to retrieve the latest speed value from the database.

    Returns:
    - JSON response with the latest speed value.
    """
    speed = get_latest_speed()  # Get the latest speed value
    return jsonify({'speed': speed})  # Return the speed as a JSON response

# Main entry point of the application
if __name__ == '__main__':
    """
    Starts the Flask application and SocketIO server.
    The app runs on all available network interfaces (0.0.0.0) on port 5000.
    """
    socketio.run(app, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)
