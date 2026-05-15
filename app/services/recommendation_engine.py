"""
Treatment recommendation engine - provides detailed treatment recommendations
"""
from flask import current_app
from app.models.disease import DiseaseDatabase


class RecommendationEngine:
    """Generates treatment recommendations based on disease detection"""
    
    def __init__(self):
        # Comprehensive disease treatment database
        self.treatment_database = {
            'early_blight': {
                'chemical': [
                    'Chlorothalonil (Bravo, Daconil)',
                    'Mancozeb (Dithane, Manzate)',
                    'Azoxystrobin (Quadris)',
                    'Copper-based fungicides'
                ],
                'biological': [
                    'Bacillus subtilis',
                    'Trichoderma harzianum',
                    'Neem oil spray'
                ],
                'cultural': [
                    'Remove and destroy infected leaves',
                    'Improve air circulation',
                    'Use drip irrigation instead of overhead watering',
                    'Mulch around plants',
                    'Stake plants to keep foliage off ground'
                ],
                'prevention': [
                    'Crop rotation (3-4 years)',
                    'Use resistant varieties',
                    'Avoid working with plants when wet',
                    'Remove plant debris after harvest',
                    'Space plants properly for air circulation'
                ],
                'fertilizers': [
                    'Balanced NPK (10-10-10)',
                    'Calcium supplements',
                    'Avoid excess nitrogen',
                    'Organic compost'
                ]
            },
            'late_blight': {
                'chemical': [
                    'Copper hydroxide',
                    'Chlorothalonil',
                    'Mancozeb',
                    'Metalaxyl (Ridomil)'
                ],
                'biological': [
                    'Copper-based organic fungicides',
                    'Bacillus amyloliquefaciens'
                ],
                'cultural': [
                    'Remove infected plants immediately',
                    'Destroy volunteer plants',
                    'Improve drainage',
                    'Avoid overhead irrigation'
                ],
                'prevention': [
                    'Plant resistant varieties',
                    'Use certified disease-free seed',
                    'Monitor weather conditions',
                    'Apply preventive fungicides in humid conditions'
                ],
                'fertilizers': [
                    'Potassium-rich fertilizer',
                    'Avoid excess nitrogen',
                    'Balanced micronutrients'
                ]
            },
            'powdery_mildew': {
                'chemical': [
                    'Sulfur-based fungicides',
                    'Potassium bicarbonate',
                    'Myclobutanil',
                    'Trifloxystrobin'
                ],
                'biological': [
                    'Neem oil',
                    'Baking soda solution (1 tbsp per gallon)',
                    'Milk spray (1:9 milk to water)',
                    'Bacillus subtilis'
                ],
                'cultural': [
                    'Prune infected parts',
                    'Improve air circulation',
                    'Reduce humidity',
                    'Water at base of plant'
                ],
                'prevention': [
                    'Plant in full sun',
                    'Proper spacing',
                    'Avoid overhead watering',
                    'Use resistant varieties'
                ],
                'fertilizers': [
                    'Avoid high nitrogen',
                    'Potassium sulfate',
                    'Balanced NPK'
                ]
            }
        }
    
    def generate_recommendations(self, disease_name, crop_name, confidence):
        """
        Generate comprehensive treatment recommendations
        
        Args:
            disease_name: Detected disease name
            crop_name: Crop species
            confidence: Detection confidence
        
        Returns:
            dict: Comprehensive recommendations
        """
        # Normalize disease name for lookup
        disease_key = self._normalize_disease_name(disease_name)
        
        # Check database first
        db_recommendation = self._get_database_recommendation(crop_name, disease_name)
        
        if db_recommendation:
            return db_recommendation
        
        # Check built-in database
        if disease_key in self.treatment_database:
            treatment_data = self.treatment_database[disease_key]
            
            return {
                'chemical_treatment': ' | '.join(treatment_data['chemical']),
                'biological_treatment': ' | '.join(treatment_data['biological']),
                'cultural_practices': ' | '.join(treatment_data['cultural']),
                'prevention': ' | '.join(treatment_data['prevention']),
                'fertilizers': ' | '.join(treatment_data['fertilizers']),
                'source': 'built-in'
            }
        
        # Generic recommendations
        return self._generic_recommendations(crop_name)
    
    def _normalize_disease_name(self, disease_name):
        """Normalize disease name for database lookup"""
        disease_lower = disease_name.lower()
        
        if 'early blight' in disease_lower or 'alternaria' in disease_lower:
            return 'early_blight'
        elif 'late blight' in disease_lower or 'phytophthora' in disease_lower:
            return 'late_blight'
        elif 'powdery mildew' in disease_lower:
            return 'powdery_mildew'
        elif 'rust' in disease_lower:
            return 'rust'
        elif 'blast' in disease_lower:
            return 'blast'
        
        return disease_lower.replace(' ', '_')
    
    def _get_database_recommendation(self, crop_name, disease_name):
        """Get recommendation from database"""
        try:
            disease_info = DiseaseDatabase.get_disease_info(crop_name, disease_name)
            
            if disease_info:
                return {
                    'chemical_treatment': disease_info.treatment or 'Consult agricultural expert',
                    'biological_treatment': 'Organic alternatives available',
                    'cultural_practices': 'Follow good agricultural practices',
                    'prevention': disease_info.prevention or 'Practice crop rotation',
                    'fertilizers': disease_info.fertilizers or 'Balanced NPK fertilizer',
                    'source': 'database'
                }
        except Exception as e:
            current_app.logger.error(f"Database lookup error: {str(e)}")
        
        return None
    
    def _generic_recommendations(self, crop_name):
        """Generic recommendations when specific disease not found"""
        return {
            'chemical_treatment': 'Consult local agricultural extension office for specific fungicide recommendations',
            'biological_treatment': 'Neem oil | Bacillus subtilis | Organic fungicides',
            'cultural_practices': 'Remove infected plant parts | Improve air circulation | Proper watering practices',
            'prevention': 'Crop rotation | Use disease-resistant varieties | Maintain plant health | Monitor regularly',
            'fertilizers': 'Balanced NPK fertilizer | Organic compost | Micronutrient supplements as needed',
            'source': 'generic'
        }


def get_treatment_recommendations(disease_name, crop_name, confidence):
    """
    Convenience function to get treatment recommendations
    
    Args:
        disease_name: Detected disease
        crop_name: Crop species
        confidence: Detection confidence
    
    Returns:
        Recommendations dictionary
    """
    engine = RecommendationEngine()
    return engine.generate_recommendations(disease_name, crop_name, confidence)
