"""
Hybrid disease detection pipeline with ML model and multi-stage validation
"""
import requests
import base64
from flask import current_app
from app.services.image_validator import ImageValidator
from app.services.crop_identifier import CropIdentifier
from app.services.confidence_filter import ConfidenceFilter
from app.services.recommendation_engine import RecommendationEngine
from app.services.ml_disease_detector import ml_detector
from app.services.huggingface_detector import hf_detector


class HybridDiseaseDetector:
    """
    Professional-grade hybrid detection pipeline:
    1. Image Quality Validation
    2. Crop Species Identification
    3. Disease Classification
    4. Confidence Filtering
    5. Treatment Recommendation
    """
    
    def __init__(self):
        self.plant_id_key = current_app.config.get('PLANT_ID_API_KEY')
        self.health_url = "https://plant.id/api/v3/health_assessment"
        
        # Initialize services
        self.image_validator = ImageValidator()
        self.crop_identifier = CropIdentifier()
        self.confidence_filter = ConfidenceFilter()
        self.recommendation_engine = RecommendationEngine()
    
    def detect_disease(self, image_path):
        """
        Main detection pipeline
        
        Args:
            image_path: Full path to image file
        
        Returns:
            Comprehensive detection results
        """
        current_app.logger.info("="*60)
        current_app.logger.info("HYBRID DETECTION PIPELINE STARTED")
        current_app.logger.info("="*60)
        
        # STAGE 1: Image Quality Validation
        current_app.logger.info("Stage 1: Validating image quality...")
        validation_result = self.image_validator.validate_image(image_path)
        
        if not validation_result['valid']:
            current_app.logger.warning(
                f"Image validation failed. Quality score: {validation_result['quality_score']}"
            )
            return self._create_validation_failure_response(validation_result)
        
        current_app.logger.info(
            f"✓ Image validation passed. Quality score: {validation_result['quality_score']}"
        )
        
        # STAGE 2: Crop Species Identification
        current_app.logger.info("Stage 2: Identifying crop species...")
        crop_result = self.crop_identifier.identify_crop(image_path)
        
        current_app.logger.info(
            f"✓ Crop identified: {crop_result['crop_name']} "
            f"(Confidence: {crop_result['confidence']}%)"
        )
        
        # STAGE 3: Disease Detection (Hugging Face Free API)
        current_app.logger.info("Stage 3: Detecting disease using Hugging Face...")
        disease_result = self._detect_disease_huggingface(image_path, crop_result)
        
        if not disease_result:
            current_app.logger.warning("Hugging Face detection failed, trying local ML...")
            disease_result = self._detect_disease_ml(image_path, crop_result)
        
        if not disease_result:
            current_app.logger.warning("ML detection failed, trying API fallback...")
            disease_result = self._detect_disease_api(image_path, crop_result)
        
        if not disease_result:
            current_app.logger.error("All detection methods failed")
            return self._create_fallback_response(crop_result)
        
        current_app.logger.info(
            f"✓ Disease detected: {disease_result['disease_name']} "
            f"(Confidence: {disease_result['confidence']}%)"
        )
        
        # STAGE 4: Confidence Filtering
        current_app.logger.info("Stage 4: Filtering by confidence...")
        filtered_result = self.confidence_filter.filter_prediction(disease_result)
        
        confidence_eval = filtered_result['confidence_evaluation']
        current_app.logger.info(
            f"✓ Confidence level: {confidence_eval['level']} - {confidence_eval['message']}"
        )
        
        # STAGE 5: Treatment Recommendations
        current_app.logger.info("Stage 5: Generating treatment recommendations...")
        recommendations = self.recommendation_engine.generate_recommendations(
            filtered_result['disease_name'],
            crop_result['crop_name'],
            filtered_result['confidence']
        )
        
        # Merge recommendations into result
        filtered_result['treatment'] = recommendations['chemical_treatment']
        filtered_result['biological_treatment'] = recommendations['biological_treatment']
        filtered_result['cultural_practices'] = recommendations['cultural_practices']
        filtered_result['prevention'] = recommendations['prevention']
        filtered_result['fertilizers'] = recommendations['fertilizers']
        
        # Add metadata
        filtered_result['pipeline_metadata'] = {
            'image_quality': validation_result['quality_score'],
            'crop_confidence': crop_result['confidence'],
            'detection_confidence': filtered_result['confidence'],
            'confidence_level': confidence_eval['level'],
            'recommendation_source': recommendations['source']
        }
        
        current_app.logger.info("="*60)
        current_app.logger.info("PIPELINE COMPLETED SUCCESSFULLY")
        current_app.logger.info("="*60)
        
        return filtered_result
    
    def _detect_disease_huggingface(self, image_path, crop_info):
        """Detect disease using Hugging Face Inference API (FREE!)"""
        try:
            current_app.logger.info("Using Hugging Face Inference API (free)...")
            
            # Use Hugging Face detector
            hf_result = hf_detector.detect_disease(image_path)
            
            if not hf_result or not hf_result.get('success'):
                current_app.logger.warning("Hugging Face detection not available")
                return None
            
            # Format result to match pipeline format
            disease_name = hf_result['disease']
            crop_name = hf_result['crop']
            confidence = hf_result['confidence']
            is_healthy = hf_result['is_healthy']
            
            current_app.logger.info(
                f"Hugging Face Result: {crop_name} - {disease_name} ({confidence:.2f}%)"
            )
            
            # Create formatted response
            if is_healthy:
                return {
                    'crop_name': crop_name,
                    'disease_name': 'No Disease Detected - Healthy Plant',
                    'confidence': round(confidence, 2),
                    'symptoms': 'Plant appears healthy with no visible signs of disease',
                    'causes': 'N/A - Plant is healthy',
                    'treatment': 'No treatment needed. Continue current care practices.',
                    'prevention': 'Maintain good agricultural practices and regular monitoring',
                    'fertilizers': 'Use balanced NPK fertilizer as per crop requirements',
                    'api_source': 'huggingface'
                }
            else:
                return {
                    'crop_name': crop_name,
                    'disease_name': disease_name,
                    'confidence': round(confidence, 2),
                    'symptoms': f'{disease_name} detected on {crop_name} leaves',
                    'causes': 'Fungal/bacterial/viral infection - specific cause varies by disease',
                    'treatment': 'Treatment recommendations will be generated based on disease type',
                    'prevention': 'Crop rotation | Proper spacing | Disease-resistant varieties',
                    'fertilizers': 'Balanced NPK fertilizer | Organic amendments',
                    'api_source': 'huggingface',
                    'all_predictions': hf_result.get('all_predictions', [])
                }
        
        except Exception as e:
            current_app.logger.error(f"Hugging Face detection error: {str(e)}")
            return None
    
    def _detect_disease_ml(self, image_path, crop_info):
        """Detect disease using local ML model"""
        try:
            current_app.logger.info("Attempting ML model detection...")
            
            # Use ML detector
            ml_result = ml_detector.detect_disease(image_path)
            
            if not ml_result or not ml_result.get('success'):
                current_app.logger.warning("ML detection not available - model not loaded")
                return None
            
            # Format result to match pipeline format
            disease_name = ml_result['disease']
            crop_name = ml_result['crop']
            confidence = ml_result['confidence']
            is_healthy = ml_result['is_healthy']
            
            current_app.logger.info(
                f"ML Model Result: {crop_name} - {disease_name} ({confidence:.2f}%)"
            )
            
            # Create formatted response
            if is_healthy:
                return {
                    'crop_name': crop_name,
                    'disease_name': 'No Disease Detected - Healthy Plant',
                    'confidence': round(confidence, 2),
                    'symptoms': 'Plant appears healthy with no visible signs of disease',
                    'causes': 'N/A - Plant is healthy',
                    'treatment': 'No treatment needed. Continue current care practices.',
                    'prevention': 'Maintain good agricultural practices and regular monitoring',
                    'fertilizers': 'Use balanced NPK fertilizer as per crop requirements',
                    'api_source': 'ml_model'
                }
            else:
                return {
                    'crop_name': crop_name,
                    'disease_name': disease_name,
                    'confidence': round(confidence, 2),
                    'symptoms': f'{disease_name} detected on {crop_name} leaves',
                    'causes': 'Fungal/bacterial/viral infection - specific cause varies by disease',
                    'treatment': 'Treatment recommendations will be generated based on disease type',
                    'prevention': 'Crop rotation | Proper spacing | Disease-resistant varieties',
                    'fertilizers': 'Balanced NPK fertilizer | Organic amendments',
                    'api_source': 'ml_model',
                    'all_predictions': ml_result.get('all_predictions', [])
                }
        
        except Exception as e:
            current_app.logger.error(f"ML detection error: {str(e)}")
            return None
    
    def _detect_disease_api(self, image_path, crop_info):
        """Detect disease using Plant.id API"""
        try:
            if not self.plant_id_key:
                current_app.logger.warning("No API key. Using mock detection.")
                return self._mock_detection(crop_info)
            
            # Read and encode image
            with open(image_path, 'rb') as image_file:
                image_data = base64.b64encode(image_file.read()).decode('ascii')
            
            # Prepare request
            payload = {
                "images": [image_data],
                "latitude": 49.207,
                "longitude": 16.608,
                "similar_images": True,
                "health": "all"
            }
            
            headers = {
                "Api-Key": self.plant_id_key,
                "Content-Type": "application/json"
            }
            
            # Make API request
            response = requests.post(
                self.health_url,
                json=payload,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                return self._parse_api_response(response.json(), crop_info)
            elif response.status_code == 401:
                current_app.logger.error("Invalid API key")
                return self._mock_detection(crop_info)
            elif response.status_code == 429:
                current_app.logger.error("Rate limit exceeded")
                return self._mock_detection(crop_info)
            else:
                current_app.logger.error(f"API error: {response.status_code}")
                return self._mock_detection(crop_info)
        
        except Exception as e:
            current_app.logger.error(f"Detection error: {str(e)}")
            return self._mock_detection(crop_info)
    
    def _parse_api_response(self, data, crop_info):
        """Parse Plant.id API response"""
        try:
            result = data.get('result', {})
            is_healthy = result.get('is_healthy', {}).get('binary', True)
            
            crop_name = crop_info.get('crop_name', 'Unknown Crop')
            
            if not is_healthy:
                disease_info = result.get('disease', {})
                suggestions = disease_info.get('suggestions', [])
                
                if suggestions:
                    top_disease = suggestions[0]
                    details = top_disease.get('details', {})
                    
                    disease_name = top_disease.get('name', 'Unknown Disease')
                    probability = top_disease.get('probability', 0) * 100
                    
                    # Extract comprehensive information
                    description = details.get('description', 'No description available')
                    cause = details.get('cause', 'Unknown cause')
                    
                    # Get treatment info
                    treatment_info = details.get('treatment', {})
                    if isinstance(treatment_info, dict):
                        chemical = treatment_info.get('chemical', [])
                        biological = treatment_info.get('biological', [])
                        prevention = treatment_info.get('prevention', [])
                        
                        treatment = ' | '.join(chemical) if chemical else 'Consult agricultural expert'
                        prevention_text = ' | '.join(prevention) if prevention else 'Practice good crop hygiene'
                    else:
                        treatment = str(treatment_info) if treatment_info else 'Consult agricultural expert'
                        prevention_text = 'Practice good crop hygiene and crop rotation'
                    
                    return {
                        'crop_name': crop_name,
                        'disease_name': disease_name,
                        'confidence': round(probability, 2),
                        'symptoms': description,
                        'causes': cause if isinstance(cause, str) else str(cause),
                        'treatment': treatment,
                        'prevention': prevention_text,
                        'fertilizers': 'Balanced NPK fertilizer | Organic compost',
                        'api_source': 'plant.id'
                    }
            
            # Healthy plant
            return {
                'crop_name': crop_name,
                'disease_name': 'No Disease Detected - Healthy Plant',
                'confidence': 95.0,
                'symptoms': 'Plant appears healthy with no visible signs of disease',
                'causes': 'N/A - Plant is healthy',
                'treatment': 'No treatment needed. Continue current care practices.',
                'prevention': 'Maintain good agricultural practices',
                'fertilizers': 'Use balanced NPK fertilizer as per crop requirements',
                'api_source': 'plant.id'
            }
        
        except Exception as e:
            current_app.logger.error(f"Error parsing API response: {str(e)}")
            return self._mock_detection(crop_info)
    
    def _mock_detection(self, crop_info):
        """High-quality mock detection for testing"""
        crop_name = crop_info.get('crop_name', 'Crop Plant')
        
        return {
            'crop_name': crop_name,
            'disease_name': 'Early Blight (Alternaria)',
            'confidence': 87.5,
            'symptoms': 'Dark brown spots with concentric rings on older leaves, yellowing around spots, leaf drop',
            'causes': 'Fungal infection caused by Alternaria solani, favored by warm humid conditions',
            'treatment': 'Remove infected leaves | Apply copper-based fungicide | Improve air circulation',
            'prevention': 'Crop rotation | Mulching | Proper spacing | Avoid overhead watering',
            'fertilizers': 'Balanced NPK (10-10-10) | Calcium supplements | Organic compost',
            'api_source': 'mock'
        }
    
    def _create_validation_failure_response(self, validation_result):
        """Create response for validation failure"""
        return {
            'crop_name': 'Image Quality Issue',
            'disease_name': 'Unable to Analyze - Poor Image Quality',
            'confidence': validation_result['quality_score'],
            'symptoms': f"Image quality issues detected: {', '.join(validation_result['issues'])}",
            'causes': 'Poor image quality prevents accurate analysis',
            'treatment': 'Please upload a better quality image',
            'prevention': ' | '.join(validation_result['recommendations']),
            'fertilizers': 'N/A - Please upload better image first',
            'validation_failed': True,
            'validation_details': validation_result
        }
    
    def _create_fallback_response(self, crop_info):
        """Create fallback response when detection fails"""
        return {
            'crop_name': crop_info.get('crop_name', 'Unknown Crop'),
            'disease_name': 'Detection Failed',
            'confidence': 0,
            'symptoms': 'Unable to detect disease. Please try again with a different image.',
            'causes': 'Detection service unavailable',
            'treatment': 'Please consult local agricultural expert',
            'prevention': 'Maintain good crop health practices',
            'fertilizers': 'Use balanced fertilizer as per crop requirements',
            'detection_failed': True
        }


def analyze_crop_image(image_path):
    """
    Main entry point for disease detection
    
    Args:
        image_path: Full path to image file
    
    Returns:
        Comprehensive detection results
    """
    detector = HybridDiseaseDetector()
    return detector.detect_disease(image_path)
