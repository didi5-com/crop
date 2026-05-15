"""
Crop identification service - identifies plant species before disease detection
"""
import requests
import base64
from flask import current_app


class CropIdentifier:
    """Identifies crop species using Plant.id API"""
    
    def __init__(self):
        self.plant_id_key = current_app.config.get('PLANT_ID_API_KEY')
        self.identify_url = "https://plant.id/api/v3/identification"
        
        # Common crop categories
        self.crop_categories = {
            'tomato': ['Solanum lycopersicum', 'tomato'],
            'potato': ['Solanum tuberosum', 'potato'],
            'corn': ['Zea mays', 'corn', 'maize'],
            'wheat': ['Triticum', 'wheat'],
            'rice': ['Oryza sativa', 'rice'],
            'cassava': ['Manihot esculenta', 'cassava'],
            'pepper': ['Capsicum', 'pepper', 'chili'],
            'bean': ['Phaseolus', 'bean'],
            'soybean': ['Glycine max', 'soybean'],
            'cotton': ['Gossypium', 'cotton']
        }
    
    def identify_crop(self, image_path):
        """
        Identify crop species from image
        
        Args:
            image_path: Path to image file
        
        Returns:
            dict: {
                'crop_name': str,
                'scientific_name': str,
                'confidence': float,
                'category': str,
                'is_crop': bool
            }
        """
        try:
            if not self.plant_id_key:
                current_app.logger.warning("No Plant.id API key. Using generic identification.")
                return self._generic_crop_detection(image_path)
            
            # Read and encode image
            with open(image_path, 'rb') as image_file:
                image_data = base64.b64encode(image_file.read()).decode('ascii')
            
            # Prepare request
            payload = {
                "images": [image_data],
                "similar_images": True
            }
            
            headers = {
                "Api-Key": self.plant_id_key,
                "Content-Type": "application/json"
            }
            
            # Make API request
            current_app.logger.info("Identifying crop species...")
            response = requests.post(
                self.identify_url,
                json=payload,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                return self._parse_identification_response(response.json())
            else:
                current_app.logger.error(f"Crop identification failed: {response.status_code}")
                return self._generic_crop_detection(image_path)
        
        except Exception as e:
            current_app.logger.error(f"Error identifying crop: {str(e)}")
            return self._generic_crop_detection(image_path)
    
    def _parse_identification_response(self, data):
        """Parse Plant.id identification response"""
        try:
            result = data.get('result', {})
            classification = result.get('classification', {})
            suggestions = classification.get('suggestions', [])
            
            if not suggestions:
                return self._generic_crop_detection(None)
            
            # Get top suggestion
            top_match = suggestions[0]
            plant_name = top_match.get('name', 'Unknown Plant')
            probability = top_match.get('probability', 0) * 100
            
            # Determine crop category
            category = self._categorize_crop(plant_name)
            is_crop = category != 'unknown'
            
            # Get scientific name
            details = top_match.get('details', {})
            scientific_name = details.get('scientific_name', plant_name)
            
            return {
                'crop_name': plant_name,
                'scientific_name': scientific_name,
                'confidence': round(probability, 2),
                'category': category,
                'is_crop': is_crop,
                'common_names': details.get('common_names', [])
            }
        
        except Exception as e:
            current_app.logger.error(f"Error parsing identification: {str(e)}")
            return self._generic_crop_detection(None)
    
    def _categorize_crop(self, plant_name):
        """Categorize plant into crop type"""
        plant_name_lower = plant_name.lower()
        
        for category, keywords in self.crop_categories.items():
            for keyword in keywords:
                if keyword.lower() in plant_name_lower:
                    return category
        
        return 'unknown'
    
    def _generic_crop_detection(self, image_path):
        """Fallback generic crop detection"""
        return {
            'crop_name': 'Crop Plant',
            'scientific_name': 'Unknown',
            'confidence': 50.0,
            'category': 'unknown',
            'is_crop': True,
            'common_names': []
        }


def identify_plant_species(image_path):
    """
    Convenience function to identify plant species
    
    Args:
        image_path: Path to image file
    
    Returns:
        Identification result dictionary
    """
    identifier = CropIdentifier()
    return identifier.identify_crop(image_path)
