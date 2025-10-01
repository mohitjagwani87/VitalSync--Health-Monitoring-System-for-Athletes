from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import threading
import time
import random
from ml_analysis_service import analyzer

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

# ESP32 settings (Change this to your ESP32 IP)
ESP_IP = "http://192.168.137.12"

# Shared dictionary for storing sensor data
sensor_data = {
    'temperature': 0,
    'humidity': 0,
    'heart_rate': 0,
    'ecg': 0
}

# Event to control background data updates
update_event = threading.Event()

def fetch_esp32_data():
    """Fetch sensor data from ESP32, or generate mock data if unreachable."""
    try:
        response = requests.get(ESP_IP, timeout=1)  # 2-second timeout
        data = response.json()
        
        # Print received data from ESP32
        print(f"✅ Received from ESP32: {data}")
        
        return data
    except requests.RequestException:
        mock_data = {
            'temperature': round(random.uniform(35.5, 37.5), 1),
            'humidity': round(random.uniform(15, 25), 1),
            'heart_rate': random.randint(60, 100),
            'ecg': random.randint(100, 900)  # Simulated ECG value
        }

        # Print generated mock data
        print(f"⚠ ESP32 Unreachable! Using Mock Data: {mock_data}")
        
        return mock_data

def update_sensor_data():
    """Background thread that continuously updates sensor data."""
    global sensor_data
    while not update_event.is_set():
        sensor_data = fetch_esp32_data()
        
        # Print data in terminal for debugging
        print(f"🌡 Temp: {sensor_data['temperature']}°C | 💧 Humidity: {sensor_data['humidity']}%")
        print(f"❤ Heart Rate: {sensor_data['heart_rate']} BPM | 📊 ECG: {sensor_data['ecg']}")
        
        time.sleep(1)  # Fetch data every second

@app.route('/data')
def get_data():
    """API endpoint to serve the latest sensor data."""
    return jsonify(sensor_data)

@app.route('/analyze', methods=['POST'])
def analyze_health():
    """API endpoint to analyze heart health using ML model."""
    try:
        # Get current sensor data
        current_data = sensor_data.copy()
        
        # Add age if provided in request
        if request.json and 'age' in request.json:
            current_data['age'] = request.json['age']
        else:
            current_data['age'] = 30  # Default age
        
        # Perform ML analysis
        analysis_result = analyzer.analyze_heart_health(current_data)
        
        return jsonify({
            'success': True,
            'analysis': analysis_result
        })
    
    except Exception as e:
        print(f"❌ Error in health analysis: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'analysis': {
                'category': 'Analysis Error',
                'message': '⚠️ Unable to analyze heart data. Please try again.',
                'risk_score': 0,
                'confidence': 0.0
            }
        }), 500

if __name__ == '__main__':
    # Start background thread
    data_thread = threading.Thread(target=update_sensor_data, daemon=True)
    data_thread.start()

    # Run Flask app
    try:
        print("🚀 Flask server started! Listening on port 5000...")
        app.run(host='0.0.0.0', port=5000, debug=True)
    finally:
        update_event.set()  # Stop the background thread gracefully
