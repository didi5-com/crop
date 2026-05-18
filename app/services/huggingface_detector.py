"""
Hugging Face Inference API for Plant Disease Detection
Uses free Hugging Face models - no API key required!
"""
import requests
import logging

logger = logging.getLogger(__name__)

class HuggingFaceDetector:
    """Plant disease detection using Hugging Face Inference API"""
    
    # Best free model for plant disease detection
    MODEL = "linkanjarad/mobilenet_v2_1.00_224-plant-disease-identification"
    
    # PlantVillage 38 disease classes
    CLASS_NAMES = [
        'Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 'Apple___healthy',
        'Blueberry___healthy', 'Cherry_(including_sour)___Powdery_mildew', 'Cherry_(including_sour)___healthy',
        'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot', 'Corn_(maize)___Common_rust_',
        'Corn_(maize)___Northern_Leaf_Blight', 'Corn_(maize)___healthy', 'Grape___Black_rot',
        'Grape___Esca_(Black_Measles)', 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 'Grape___healthy',
        'Orange___Haunglongbing_(Citrus_greening)', 'Peach___Bacterial_spot', 'Peach___healthy',
        'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy', 'Potato___Early_blight',
        'Potato___Late_blight', 'Potato___healthy', 'Raspberry___healthy', 'Soybean___healthy',
        'Squash___Powdery_mildew', 'Strawberry___Leaf_scab', 'Strawberry___healthy',
        'Tomato___Bacterial_spot', 'Tomato___Early_blight', 'Tomato___Late_blight',
        'Tomato___Leaf_Mold', 'Tomato___Septoria_leaf_spot',
        'Tomato___Spider_mites Two-spotted_spider_mite', 'Tomato___Target_Spot',
        'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato___Tomato_mosaic_virus', 'Tomato___healthy'
    ]
    
    def __init__(self):
        """Initialize the Hugging Face detector"""
        self.api_url = f"https://api-inference.huggingface.co/models/{self.MODEL}"
        
    def predict(self, image_path):
        """Predict disease using Hugging Face Inference API"""
        try:
            logger.info(f"Using Hugging Face model: {self.MODEL}")
            
            # Read image file
            with open(image_path, 'rb') as f:
                image_data = f.read()
            
            # Make request to Hugging Face Inference API (FREE - no API key needed!)
            response = requests.post(
                self.api_url,
                headers={"Content-Type": "application/octet-stream"},
                data=image_data,
                timeout=30
            )
            
            if response.status_code == 200:
                predictions = response.json()
                logger.info("✓ Hugging Face prediction successful")
                return self._parse_predictions(predictions)
            elif response.status_code == 503:
                logger.warning("Model is loading, please try again in a moment")
                return None
            else:
                logger.error(f"Hugging Face API returned {response.status_code}: {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Error in Hugging Face prediction: {e}")
            return None
    
    def _parse_predictions(self, predictions):
        """Parse Hugging Face API response"""
        try:
            if not predictions or len(predictions) == 0:
                return None
            
            # Get top 3 predictions
            top_predictions = sorted(predictions, key=lambda x: x['score'], reverse=True)[:3]
            
            results = []
            for pred in top_predictions:
                label = pred['label']
                confidence = pred['score'] * 100
                
                # Parse label
                parts = label.split('___')
                crop = parts[0].replace('_', ' ') if len(parts) > 0 else 'Unknown'
                disease = parts[1].replace('_', ' ') if len(parts) > 1 else 'Unknown'
                
                results.append({
                    'crop': crop,
                    'disease': disease,
                    'confidence': confidence,
                    'is_healthy': 'healthy' in disease.lower()
                })
            
            return results
            
        except Exception as e:
            logger.error(f"Error parsing predictions: {e}")
            return None
    
    def detect_disease(self, image_path):
        """Main method to detect disease from image"""
        predictions = self.predict(image_path)
        
        if not predictions:
            return {
                'success': False,
                'error': 'Hugging Face model not available'
            }
        
        # Get top prediction
        top_prediction = predictions[0]
        
        return {
            'success': True,
            'crop': top_prediction['crop'],
            'disease': top_prediction['disease'],
            'confidence': top_prediction['confidence'],
            'is_healthy': top_prediction['is_healthy'],
            'all_predictions': predictions
        }


# Global instance
hf_detector = HuggingFaceDetector()
