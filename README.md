# VitalSync – Health Monitoring System for Athletes 🏃‍♂️❤️‍🩹

VitalSync is an advanced health monitoring system that combines real-time sensor data with machine learning to provide intelligent health analysis for athletes and fitness enthusiasts. 🧠📈

## 🚀 Features

### Real-Time Monitoring
- **Heart Rate Monitoring**: Continuous BPM tracking with ECG visualization
- **Temperature & Humidity**: Environmental and body temperature monitoring
- **Activity Tracking**: Step counting and distance calculation
- **Live ECG Display**: Real-time electrocardiogram visualization

### AI-Powered Health Analysis
- **Machine Learning Integration**: Uses trained logistic regression model for heart health prediction
- **Risk Assessment**: Categorizes health status as Healthy, Low Risk, Moderate Risk, or High Risk
- **Intelligent Alerts**: Context-aware health recommendations and warnings
- **Confidence Scoring**: Provides confidence levels for all health predictions

### Modern Web Interface
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Real-Time Updates**: Live data streaming from ESP32 sensors
- **Interactive Charts**: Dynamic ECG and health metric visualizations
- **Professional UI**: Clean, medical-grade interface design

## 🏗️ Architecture

### Frontend
- **HTML5/CSS3/JavaScript**: Modern web technologies
- **Chart.js**: Real-time ECG and data visualization
- **Responsive Design**: Mobile-first approach
- **Real-Time Communication**: WebSocket-like data fetching

### Backend
- **Flask API**: RESTful API for sensor data and ML analysis
- **Machine Learning**: Scikit-learn based heart health prediction
- **CORS Support**: Cross-origin resource sharing enabled
- **Mock Data Fallback**: Works without physical sensors

### Machine Learning
- **Dataset**: Heart disease prediction dataset (303 samples)
- **Model**: Logistic Regression with feature selection
- **Accuracy**: 80%+ prediction accuracy
- **Features**: Age, heart rate, blood pressure, ECG metrics, and derived features

## 📋 Prerequisites

- Python 3.8+
- Modern web browser
- ESP32 device (optional, for real sensor data)

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/mohitjagwani87/VitalSync-Health-Monitoring-System-for-Athletes.git
   cd VitalSync-Health-Monitoring-System-for-Athletes
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the Flask backend**
   ```bash
   python esp32data.py
   ```

4. **Open the web interface**
   - Navigate to `analysis.html` in your web browser
   - The system will automatically connect to the backend

## 🔧 Configuration

### ESP32 Setup (Optional)
- Update the `ESP_IP` variable in `esp32data.py` with your ESP32's IP address
- Ensure your ESP32 is running compatible sensor code

### ML Model Customization
- Modify `ml_analysis_service.py` to adjust risk thresholds
- Retrain the model with new data by updating the dataset path
- Adjust feature importance weights as needed

## 📊 API Endpoints

### GET /data
Returns current sensor data
```json
{
  "temperature": 36.5,
  "humidity": 50.0,
  "heart_rate": 75,
  "ecg": 600
}
```

### POST /analyze
Performs ML-based health analysis
```json
{
  "age": 25
}
```

Response:
```json
{
  "success": true,
  "analysis": {
    "category": "Healthy Heart",
    "message": "💪 Excellent heart condition! Keep pushing forward!",
    "risk_score": 0,
    "confidence": 0.85,
    "prediction": 0,
    "heart_rate": 75,
    "max_hr": 195,
    "temperature": 36.5
  }
}
```

## 🎯 Usage

1. **Open Analysis Page**: Navigate to `analysis.html`
2. **View Real-Time Data**: Monitor live sensor readings
3. **Get Health Analysis**: Click "Update Analysis" for AI-powered health assessment
4. **Monitor ECG**: Watch real-time electrocardiogram display
5. **Track Activity**: View step count and distance metrics

## 🔬 Machine Learning Details

### Dataset
- **Source**: Heart Disease Prediction Dataset
- **Samples**: 303 patient records
- **Features**: 13 medical parameters including age, sex, chest pain type, blood pressure, cholesterol, etc.

### Model Training
- **Algorithm**: Logistic Regression
- **Preprocessing**: StandardScaler normalization
- **Feature Selection**: SelectKBest with f_classif
- **Cross-Validation**: 5-fold CV for hyperparameter tuning
- **Final Accuracy**: 80%+ on test set

### Risk Assessment Logic
The system combines ML predictions with real-time sensor data:
- Heart rate analysis (relative to max HR)
- Temperature monitoring
- Model confidence scoring
- Multi-factor risk calculation

## 🚨 Health Warnings

**Important**: This system is for fitness and wellness purposes only. It is not a substitute for professional medical advice. Always consult healthcare professionals for medical concerns.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Team

- **Shreesh**: Data Analysis & ML Integration
- **Anurag**: Frontend Development & UI/UX
- **Mohit**: Backend Development & System Integration
- **Om**: Hardware Integration & Testing

## 📞 Support

For support, email support@vitalsync.com or create an issue in this repository.

## 🔄 Version History

- **v1.0.0**: Initial release with basic monitoring
- **v1.1.0**: Added ML integration and health analysis
- **v1.2.0**: Enhanced UI and real-time features
- **v2.0.0**: Complete AI-powered health monitoring system

---

**VitalSync** - Empowering athletes with intelligent health insights! 🏃‍♂️💪