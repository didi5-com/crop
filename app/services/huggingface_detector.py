"""
Hugging Face Inference API for Plant Disease Detection
Uses free Hugging Face models - no API key required!
Supports both PlantVillage crops AND African crops (cassava, maize, etc.)
"""
import requests
import logging

logger = logging.getLogger(__name__)

class HuggingFaceDetector:
    """Plant disease detection using Hugging Face Inference API"""
    
    # Multiple models for different crop types
    MODELS = {
        'african_crops': "swaggerlish/farmguard-ai-multi-crops-disease",  # Cassava, Maize, Pepper, Tomato
        'cassava_specific': "nexusbert/resnet50-cassava-finetuned",  # Cassava only (5 diseases)
        'plantvillage': "linkanjarad/mobilenet_v2_1.00_224-plant-disease-identification",  # 38 classes
    }
    
    def __init__(self):
        """Initialize the Hugging Face detector"""
        # Try African crops model first (includes cassava!)
        self.primary_model = self.MODELS['african_crops']
        self.fallback_model = self.MODELS['plantvillage']
        
    def predict(self, image_path):
        """Predict disease using Hugging Face Inference API"""
        try:
            # Try primary model (African crops including cassava)
            logger.info(f"Trying primary model: {self.primary_model}")
            result = self._try_model(self.primary_model, image_path)
            
            if result:
                logger.info("✓ Primary model (African crops) succeeded")
                return result
            
            # Fallback to PlantVillage model
            logger.info(f"Trying fallback model: {self.fallback_model}")
            result = self._try_model(self.fallback_model, image_path)
            
            if result:
                logger.info("✓ Fallback model (PlantVillage) succeeded")
                return result
            
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
                return self._parse_predictions(predictions)
            elif response.status_code == 503:
                logger.warning(f"Model {model_name} is loading...")
                return None
            else:
                logger.warning(f"Model {model_name} returned {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error with model {model_name}: {e}")
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
                
                # Parse label (handles both formats: "Crop___Disease" and "Crop_Disease")
                if '___' in label:
                    parts = label.split('___')
                elif '_' in label:
                    # For African crops model format
                    parts = label.split('_', 1)
                else:
                    parts = [label]
                
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
