import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import joblib
import os

class HeartHealthAnalyzer:
    def __init__(self):
        self.model = None
        self.scaler = None
        self.feature_names = ['age', 'sex', 'cp', 'trtbps', 'restecg', 'thalachh', 'exng', 'oldpeak', 'slp']
        self.model_file = 'heart_model.pkl'
        self.scaler_file = 'heart_scaler.pkl'
        
    def load_or_train_model(self):
        """Load existing model or train new one from heart dataset"""
        if os.path.exists(self.model_file) and os.path.exists(self.scaler_file):
            try:
                self.model = joblib.load(self.model_file)
                self.scaler = joblib.load(self.scaler_file)
                print("✅ Loaded existing model and scaler")
                return
            except Exception as e:
                print(f"⚠️ Error loading model: {e}, training new one...")
        
        # Train new model
        self._train_model()
    
    def _train_model(self):
        """Train the heart health model from the dataset"""
        try:
            # Load the heart dataset
            df = pd.read_csv('heart-dataset-checkpoint.csv')
            
            # Preprocess data (same as notebook)
            df = df.drop(columns=["chol", "fbs", "caa", "thall"])
            df["Cardio_Stress"] = df["trtbps"] / df["thalachh"]
            
            # Prepare features and target
            X = df.drop(columns=["output"])
            y = df["output"]
            
            # Convert y to binary (same as notebook)
            y = (y >= 0.5).astype(int)
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
            
            # Scale features
            self.scaler = StandardScaler()
            X_train_scaled = self.scaler.fit_transform(X_train)
            X_test_scaled = self.scaler.transform(X_test)
            
            # Train model
            self.model = LogisticRegression(C=0.01, solver='liblinear', random_state=42)
            self.model.fit(X_train_scaled, y_train)
            
            # Save model and scaler
            joblib.dump(self.model, self.model_file)
            joblib.dump(self.scaler, self.scaler_file)
            
            print("✅ Model trained and saved successfully")
            
        except Exception as e:
            print(f"❌ Error training model: {e}")
            # Create a fallback model
            self._create_fallback_model()
    
    def _create_fallback_model(self):
        """Create a simple fallback model if training fails"""
        print("🔄 Creating fallback model...")
        self.scaler = StandardScaler()
        # Create dummy data for fallback
        dummy_X = np.random.randn(100, len(self.feature_names))
        dummy_y = np.random.randint(0, 2, 100)
        self.scaler.fit(dummy_X)
        self.model = LogisticRegression(random_state=42)
        self.model.fit(self.scaler.transform(dummy_X), dummy_y)
    
    def analyze_heart_health(self, sensor_data):
        """
        Analyze heart health based on sensor data
        Returns risk category and message
        """
        try:
            # Extract relevant data from sensor readings
            age = sensor_data.get('age', 30)  # Default age if not provided
            heart_rate = sensor_data.get('heart_rate', 70)
            temperature = sensor_data.get('temperature', 36.5)
            humidity = sensor_data.get('humidity', 50)
            
            # Calculate derived features
            max_hr = 220 - age
            cardio_stress = 120 / heart_rate if heart_rate > 0 else 1.0  # Using default BP
            
            # Create feature vector (matching training data)
            features = np.array([[
                age,                           # age
                1,                             # sex (default male)
                0,                             # cp (chest pain type)
                120,                           # trtbps (resting BP - default)
                1,                             # restecg (resting ECG)
                heart_rate,                    # thalachh (max HR achieved)
                0,                             # exng (exercise induced angina)
                0.5,                           # oldpeak (ST depression)
                1,                             # slp (slope)
                cardio_stress                  # Cardio_Stress
            ]])
            
            # Scale features
            features_scaled = self.scaler.transform(features)
            
            # Make prediction
            prediction = self.model.predict(features_scaled)[0]
            prediction_proba = self.model.predict_proba(features_scaled)[0]
            
            # Calculate risk score based on multiple factors
            risk_score = 0
            
            # Heart rate analysis
            if heart_rate > max_hr * 0.9:
                risk_score += 3  # Very high heart rate
            elif heart_rate > max_hr * 0.8:
                risk_score += 2  # High heart rate
            elif heart_rate > max_hr * 0.7:
                risk_score += 1  # Elevated heart rate
            
            # Temperature analysis
            if temperature > 37.5:
                risk_score += 2  # Fever
            elif temperature < 35.0:
                risk_score += 1  # Hypothermia
            
            # Model prediction influence
            if prediction == 1:
                risk_score += 2  # Model predicts heart disease
            
            # Determine risk category
            if risk_score >= 5:
                category = "High Risk"
                confidence = prediction_proba[1] if prediction == 1 else prediction_proba[0]
                messages = [
                    "🚨 Seek immediate medical attention! Signs of heart strain detected!",
                    "⚠️ Warning: Your heart is under extreme stress. Stop running immediately!",
                    "🚨 High risk of heart attack! Consult a cardiologist before running again!"
                ]
            elif risk_score >= 3:
                category = "Moderate Risk"
                confidence = prediction_proba[1] if prediction == 1 else prediction_proba[0]
                messages = [
                    "⚠️ Be cautious! Your heart is working harder than normal.",
                    "🔴 Slow down! Your heart rate is beyond safe running limits.",
                    "⚠️ Moderate risk detected. Consider consulting a doctor for a checkup."
                ]
            elif risk_score >= 1:
                category = "Low Risk"
                confidence = prediction_proba[1] if prediction == 1 else prediction_proba[0]
                messages = [
                    "✅ You're doing fine, but stay aware of your limits.",
                    "📉 Maintain a steady pace to keep your heart in optimal condition.",
                    "✅ Slight risk detected. Keep training smartly and monitor your stats."
                ]
            else:
                category = "Healthy Heart"
                confidence = prediction_proba[0] if prediction == 0 else prediction_proba[1]
                messages = [
                    "💪 Excellent heart condition! Keep pushing forward!",
                    "🔥 You're in great shape! Maintain this pace for peak performance.",
                    "💙 No heart concerns detected. Keep running strong and stay hydrated!"
                ]
            
            # Select random message from category
            import random
            message = random.choice(messages)
            
            return {
                'category': category,
                'message': message,
                'risk_score': risk_score,
                'confidence': float(confidence),
                'prediction': int(prediction),
                'heart_rate': heart_rate,
                'max_hr': max_hr,
                'temperature': temperature
            }
            
        except Exception as e:
            print(f"❌ Error in heart health analysis: {e}")
            return {
                'category': 'Analysis Error',
                'message': '⚠️ Unable to analyze heart data. Please check sensor connections.',
                'risk_score': 0,
                'confidence': 0.0,
                'prediction': 0,
                'heart_rate': sensor_data.get('heart_rate', 0),
                'max_hr': 0,
                'temperature': sensor_data.get('temperature', 0)
            }

# Global analyzer instance
analyzer = HeartHealthAnalyzer()
analyzer.load_or_train_model()
