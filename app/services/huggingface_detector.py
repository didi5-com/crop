"""
Hugging Face Inference API for Plant Disease Detection
Uses free Hugging Face models - no API key required!
Uses PROVEN working models with high accuracy
"""
import requests
import logging
import time

logger = logging.getLogger(__name__)

class HuggingFaceDetector:
    """Plant disease detection using Hugging Face Inference API"""
    
    # PROVEN working models from Hugging Face
    MODELS = {
        'primary': "mesabo/agri-plant-disease-resnet50",  # ResNet50 - High accuracy
        'mobilenet': "Daksh159/plant-disease-mobilenetv2",  # MobileNetV2 - 38 classes
        'inception': "kero2111/Plant_Disease",  # InceptionResNetV2 - 38 classes
        'efficientnet': "eymenslimani/plant-disease-detector",  # EfficientNet - 79.86% accuracy
        'vit': "wambugu71/crop_leaf_diseases_vit",  # Vision Transformer - Corn, Potato, Rice, Wheat
    }
    
    def __init__(self):
        """Initialize the Hugging Face detector"""
        # Use proven models in priority order
        self.model_priority = [
            self.MODELS['primary'],
            self.MODELS['mobilenet'],
            self.MODELS['inception'],
            self.MODELS['efficientnet'],
        ]
        
    def predict(self, image_path):
        """Predict disease using Hugging Face Inference API"""
        try:
            # Try each model in priority order
            for model_name in self.model_priority:
                logger.info(f"Trying model: {model_name}")
                result = self._try_model(model_name, image_path)
                
                if result:
                    logger.info(f"✓ Model {model_name} succeeded")
                    return result
                
                # Wait a bit before trying next model
                time.sleep(1)
            
            logger.error("All Hugging Face models failed")
            return None
                
        except Exception as e:
            logger.error(f"Error in Hugging Face prediction: {e}")
            return None
    
    def _try_model(self, model_name, image_path):
        """Try a specific model"""
        try:
            api_url = f"https://api-inference.huggingface.co/models/{model_name}"
            
            # Read image file
            with open(image_path, 'rb') as f:
                image_data = f.read()
            
            # Make request to Hugging Face Inference API (FREE - no API key needed!)
            response = requests.post(
                api_url,
                headers={"Content-Type": "application/octet-stream"},
                data=image_data,
                timeout=30
            )
            
            if response.status_code == 200:
                predictions = response.json()
                logger.info(f"Model response: {predictions[:2] if isinstance(predictions, list) else predictions}")
                return self._parse_predictions(predictions)
            elif response.status_code == 503:
                logger.warning(f"Model {model_name} is loading, waiting...")
                # Model is loading, wait and retry once
                time.sleep(10)
                response = requests.post(
                    api_url,
                    headers={"Content-Type": "application/octet-stream"},
                    data=image_data,
                    timeout=30
                )
                if response.status_code == 200:
                    predictions = response.json()
                    return self._parse_predictions(predictions)
                return None
            else:
                logger.warning(f"Model {model_name} returned {response.status_code}: {response.text[:200]}")
                return None
                
        except Exception as e:
            logger.error(f"Error with model {model_name}: {e}")
            return None
    
    def _parse_predictions(self, predictions):
        """Parse Hugging Face API response"""
        try:
            if not predictions or len(predictions) == 0:
                return None
            
            # Get top 5 predictions for better accuracy
            top_predictions = sorted(predictions, key=lambda x: x['score'], reverse=True)[:5]
            
            results = []
            for pred in top_predictions:
                label = pred['label']
                confidence = pred['score'] * 100
                
                # Parse label - handles multiple formats
                # Format 1: "Crop___Disease" (PlantVillage format)
                # Format 2: "Crop_Disease" 
                # Format 3: "Disease"
                
                crop = "Unknown"
                disease = label
                
                if '___' in label:
                    # PlantVillage format: "Tomato___Early_blight"
                    parts = label.split('___')
                    crop = parts[0].replace('_', ' ').strip()
                    disease = parts[1].replace('_', ' ').strip() if len(parts) > 1 else label
                elif '__' in label:
                    # Alternative format: "Tomato__Early_blight"
                    parts = label.split('__')
                    crop = parts[0].replace('_', ' ').strip()
                    disease = parts[1].replace('_', ' ').strip() if len(parts) > 1 else label
                else:
                    # Try to extract crop from disease name
                    # Common patterns: "Tomato Early blight", "Potato Late blight"
                    words = label.replace('_', ' ').split()
                    if len(words) > 1:
                        # First word might be crop
                        potential_crops = ['tomato', 'potato', 'corn', 'maize', 'pepper', 'cassava', 
                                         'rice', 'wheat', 'apple', 'grape', 'cherry', 'peach', 
                                         'strawberry', 'bell', 'soybean']
                        first_word = words[0].lower()
                        if first_word in potential_crops:
                            crop = words[0]
                            disease = ' '.join(words[1:])
                        else:
                            disease = label.replace('_', ' ')
                    else:
                        disease = label.replace('_', ' ')
                
                # Check if healthy
                is_healthy = any(word in disease.lower() for word in ['healthy', 'normal', 'good'])
                
                results.append({
                    'crop': crop.title(),
                    'disease': disease.title(),
                    'confidence': round(confidence, 2),
                    'is_healthy': is_healthy,
                    'raw_label': label
                })
            
            logger.info(f"Parsed {len(results)} predictions")
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
