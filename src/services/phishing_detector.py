import joblib
import os
from src.utils.extract_feature import extract_features

class PhishingDetector:
    def __init__(self):
        self.model = None
        self.load_model()
        
    def load_model(self):
        """Load the trained model from file"""
        model_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'random_forest.pkl')
        self.model = joblib.load(model_path)
        
    def check_message(self, url):
        """Check if a message contains phishing URLs"""
        try:
            # Extract features from message
            features = extract_features(url)
            
            # Make prediction
            if self.model:
                is_phishing = bool(self.model.predict([features])[0])
                return is_phishing
            else:
                return False, {'error': 'Model not loaded'}
                
        except Exception as e:
            return False, {'error': str(e)} 