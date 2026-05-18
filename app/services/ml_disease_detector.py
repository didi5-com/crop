"""
Machine Learning-based Disease Detection using PlantVillage Model
Uses MobileNetV2 for lightweight inference
"""
import os
import numpy as np
from PIL import Image
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MLDiseaseDetector:
    """ML-based disease detection using PlantVillage trained model"""
    
    # PlantVillage 38 disease classes
    CLASS_NAMES = [
        'Apple___Apple_scab',
        'Apple___Black_rot',
        'Apple___Cedar_apple_rust',
        'Apple___healthy',
        'Blueberry___healthy',
        'Cherry_(including_sour)___Powdery_mildew',
        'Cherry_(including_sour)___healthy',
        'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
        'Corn_(maize)___Common_rust_',
        'Corn_(maize)___Northern_Leaf_Blight',
        'Corn_(maize)___healthy',
        'Grape___Black_rot',
        'Grape___Esca_(Black_Measles)',
        'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)',
        'Grape___healthy',
        'Orange___Haunglongbing_(Citrus_greening)',
        'Peach___Bacterial_spot',
        'Peach___healthy',
        'Pepper,_bell___Bacterial_spot',
        'Pepper,_bell___healthy',
        'Potato___Early_blight',
        'Potato___Late_blight',
        'Potato___healthy',
        'Raspberry___healthy',
        'Soybean___healthy',
        'Squash___Powdery_mildew',
        'Strawberry___Leaf_scab',
        'Strawberry___healthy',
        'Tomato___Bacterial_spot',
        'Tomato___Early_blight',
        'Tomato___Late_blight',
        'Tomato___Leaf_Mold',
        'Tomato___Septoria_leaf_spot',
        'Tomato___Spider_mites Two-spotted_spider_mite',
        'Tomato___Target_Spot',
        'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
        'Tomato___Tomato_mosaic_virus',
        'Tomato___healthy'
    ]
    
    def __init__(self):
        """Initialize the ML detector"""
        self.model = None
        self.model_loaded = False
        self.tf_available = False
        
        # Try to import TensorFlow
        try:
            import tensorflow as tf
            self.tf = tf
            self.tf_available = True
            logger.info("TensorFlow is available")
        except ImportError:
            logger.warning("TensorFlow not available - ML detection disabled")
            self.tf_available = False
        
    def load_model(self):
        """Load the pre-trained model"""
        if not self.tf_available:
            logger.error("TensorFlow not available")
            return False
            
        try:
            from pathlib import Path
            model_path = Path('models/plant_disease_model.h5')
            
            if not model_path.exists():
                logger.warning(f"Model file not found at {model_path}")
                return False
            
            logger.info(f"Loading model from {model_path}...")
            self.model = self.tf.keras.models.load_model(str(model_path))
            self.model_loaded = True
            logger.info("Model loaded successfully!")
            return True
            
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            self.model_loaded = False
            return False
    
    def preprocess_image(self, image_path):
        """Preprocess image for model input"""
        try:
            # Load image
            img = Image.open(image_path).convert('RGB')
            
            # Resize to 224x224
            img = img.resize((224, 224))
            
            # Convert to array and normalize
            img_array = np.array(img)
            img_array = img_array.astype('float32') / 255.0
            
            # Add batch dimension
            img_array = np.expand_dims(img_array, axis=0)
            
            return img_array
            
        except Exception as e:
            logger.error(f"Error preprocessing image: {e}")
            return None
    
    def predict(self, image_path):
        """Predict disease from image"""
        if not self.tf_available:
            logger.warning("TensorFlow not available")
            return None
            
        try:
            # Load model if not loaded
            if not self.model_loaded:
                if not self.load_model():
                    return None
            
            # Preprocess image
            img_array = self.preprocess_image(image_path)
            if img_array is None:
                return None
            
            # Make prediction
            predictions = self.model.predict(img_array, verbose=0)
            
            # Get top 3 predictions
            top_3_indices = np.argsort(predictions[0])[-3:][::-1]
            
            results = []
            for idx in top_3_indices:
                class_name = self.CLASS_NAMES[idx]
                confidence = float(predictions[0][idx])
                
                # Parse class name
                parts = class_name.split('___')
                crop = parts[0].replace('_', ' ')
                disease = parts[1].replace('_', ' ') if len(parts) > 1 else 'Unknown'
                
                results.append({
                    'crop': crop,
                    'disease': disease,
                    'confidence': confidence * 100,
                    'is_healthy': 'healthy' in disease.lower()
                })
            
            return results
            
        except Exception as e:
            logger.error(f"Error making prediction: {e}")
            return None
    
    def detect_disease(self, image_path):
        """Main method to detect disease from image"""
        predictions = self.predict(image_path)
        
        if not predictions:
            return {
                'success': False,
                'error': 'ML model not available'
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
ml_detector = MLDiseaseDetector()
