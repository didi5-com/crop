"""
Machine Learning-based Disease Detection using PlantVillage Model
Uses a pre-trained EfficientNetB4 model from Hugging Face
"""
import os
import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow import keras
import requests
from pathlib import Path

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
        self.model_path = Path('models/plant_disease_model.h5')
        self.input_size = (224, 224)  # Standard size for most models
        
    def download_model(self):
        """Download pre-trained model from Hugging Face"""
        try:
            # Create models directory
            self.model_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Download model from Hugging Face
            model_url = "https://huggingface.co/liriope/PlantDiseaseDetection/resolve/main/plant_disease_efficientnetb4.h5"
            
            print(f"Downloading model from {model_url}...")
            response = requests.get(model_url, stream=True, timeout=300)
            response.raise_for_status()
            
            with open(self.model_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"Model downloaded successfully to {self.model_path}")
            return True
            
        except Exception as e:
            print(f"Error downloading model: {e}")
            return False
    
    def load_model(self):
        """Load the pre-trained model"""
        try:
            # Check if model exists, if not download it
            if not self.model_path.exists():
                print("Model not found locally. Downloading...")
                if not self.download_model():
                    raise Exception("Failed to download model")
            
            # Load model
            print(f"Loading model from {self.model_path}...")
            self.model = keras.models.load_model(self.model_path)
            print("Model loaded successfully!")
            return True
            
        except Exception as e:
            print(f"Error loading model: {e}")
            return False
    
    def preprocess_image(self, image_path):
        """Preprocess image for model input"""
        try:
            # Load image
            img = Image.open(image_path).convert('RGB')
            
            # Resize to model input size
            img = img.resize(self.input_size)
            
            # Convert to array and normalize
            img_array = np.array(img)
            img_array = img_array.astype('float32') / 255.0
            
            # Add batch dimension
            img_array = np.expand_dims(img_array, axis=0)
            
            return img_array
            
        except Exception as e:
            print(f"Error preprocessing image: {e}")
            return None
    
    def predict(self, image_path):
        """Predict disease from image"""
        try:
            # Load model if not loaded
            if self.model is None:
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
            print(f"Error making prediction: {e}")
            return None
    
    def detect_disease(self, image_path):
        """Main method to detect disease from image"""
        predictions = self.predict(image_path)
        
        if not predictions:
            return {
                'success': False,
                'error': 'Failed to analyze image'
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
