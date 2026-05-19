"""
Simple Manual Disease Detector
Analyzes image features (colors, patterns) to detect diseases
Uses OpenCV image analysis to provide varied results based on actual image content
"""
import cv2
import numpy as np
from flask import current_app
from app.data.crop_disease_database import CROP_DISEASES


class SimpleDetector:
    """Manual disease detection using image analysis"""
    
    def __init__(self):
        """Initialize the simple detector"""
        pass
    
    def detect_disease(self, image_path):
        """
        Detect disease by analyzing image features
        
        Args:
            image_path: Path to image file
        
        Returns:
            Detection result dictionary
        """
        try:
            # Read image
            img = cv2.imread(image_path)
            if img is None:
                return None
            
            # Analyze image features
            features = self._analyze_image(img)
            
            # Match features to diseases
            result = self._match_disease(features)
            
            return result
        
        except Exception as e:
            current_app.logger.error(f"Simple detector error: {str(e)}")
            return None

    
    def _analyze_image(self, img):
        """Analyze image to extract disease-relevant features"""
        height, width = img.shape[:2]
        
        # Convert to different color spaces
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Feature 1: Color distribution
        colors = self._analyze_colors(img, hsv)
        
        # Feature 2: Spot/lesion detection
        spots = self._detect_spots(gray)
        
        # Feature 3: Texture analysis
        texture = self._analyze_texture(gray)
        
        # Feature 4: Uniformity
        uniformity = self._analyze_uniformity(hsv)
        
        return {
            'colors': colors,
            'spots': spots,
            'texture': texture,
            'uniformity': uniformity
        }
    
    def _analyze_colors(self, img, hsv):
        """Analyze color distribution in image"""
        # Calculate color percentages
        total_pixels = img.shape[0] * img.shape[1]
        
        # Green (healthy vegetation)
        green_mask = cv2.inRange(hsv, np.array([35, 40, 40]), np.array([85, 255, 255]))
        green_percent = (np.sum(green_mask > 0) / total_pixels) * 100
        
        # Yellow (chlorosis, nutrient deficiency)
        yellow_mask = cv2.inRange(hsv, np.array([20, 40, 40]), np.array([35, 255, 255]))
        yellow_percent = (np.sum(yellow_mask > 0) / total_pixels) * 100
        
        # Brown (necrosis, dead tissue)
        brown_mask = cv2.inRange(hsv, np.array([10, 40, 20]), np.array([20, 255, 200]))
        brown_percent = (np.sum(brown_mask > 0) / total_pixels) * 100
        
        # Red/Orange (rust, severe damage)
        red_mask = cv2.inRange(hsv, np.array([0, 40, 40]), np.array([10, 255, 255]))
        red_percent = (np.sum(red_mask > 0) / total_pixels) * 100
        
        # White/Light (mold, powdery mildew)
        white_mask = cv2.inRange(hsv, np.array([0, 0, 200]), np.array([180, 30, 255]))
        white_percent = (np.sum(white_mask > 0) / total_pixels) * 100
        
        return {
            'green': round(green_percent, 2),
            'yellow': round(yellow_percent, 2),
            'brown': round(brown_percent, 2),
            'red': round(red_percent, 2),
            'white': round(white_percent, 2)
        }

    
    def _detect_spots(self, gray):
        """Detect spots and lesions"""
        # Apply threshold to detect dark spots
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Find contours (spots)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Filter small contours
        significant_spots = [c for c in contours if cv2.contourArea(c) > 50]
        
        # Calculate spot characteristics
        spot_count = len(significant_spots)
        
        if spot_count > 0:
            areas = [cv2.contourArea(c) for c in significant_spots]
            avg_spot_size = np.mean(areas)
            
            # Check for circular spots (target-like patterns)
            circularities = []
            for contour in significant_spots:
                area = cv2.contourArea(contour)
                perimeter = cv2.arcLength(contour, True)
                if perimeter > 0:
                    circularity = 4 * np.pi * area / (perimeter * perimeter)
                    circularities.append(circularity)
            
            avg_circularity = np.mean(circularities) if circularities else 0
        else:
            avg_spot_size = 0
            avg_circularity = 0
        
        return {
            'count': spot_count,
            'avg_size': round(avg_spot_size, 2),
            'circularity': round(avg_circularity, 2)
        }
    
    def _analyze_texture(self, gray):
        """Analyze texture patterns"""
        # Calculate texture using standard deviation
        texture_score = np.std(gray)
        
        # Detect edges (lesion boundaries)
        edges = cv2.Canny(gray, 50, 150)
        edge_density = (np.sum(edges > 0) / edges.size) * 100
        
        return {
            'roughness': round(texture_score, 2),
            'edge_density': round(edge_density, 2)
        }
    
    def _analyze_uniformity(self, hsv):
        """Analyze color uniformity"""
        # Calculate standard deviation of hue and saturation
        hue_std = np.std(hsv[:, :, 0])
        sat_std = np.std(hsv[:, :, 1])
        
        # Lower std = more uniform (healthy)
        # Higher std = less uniform (diseased)
        uniformity_score = 100 - min((hue_std + sat_std) / 2, 100)
        
        return round(uniformity_score, 2)

    
    def _match_disease(self, features):
        """Match image features to disease patterns"""
        colors = features['colors']
        spots = features['spots']
        texture = features['texture']
        uniformity = features['uniformity']
        
        current_app.logger.info(f"Image Analysis - Colors: {colors}")
        current_app.logger.info(f"Image Analysis - Spots: {spots}")
        current_app.logger.info(f"Image Analysis - Texture: {texture}")
        current_app.logger.info(f"Image Analysis - Uniformity: {uniformity}")
        
        # Decision logic based on features
        
        # HEALTHY: High green, low other colors, uniform
        if (colors['green'] > 60 and 
            colors['yellow'] < 10 and 
            colors['brown'] < 10 and
            uniformity > 60):
            return self._create_result('cassava', 'healthy', 92.0)
        
        # CASSAVA MOSAIC: Yellow patches, leaf distortion
        if (colors['yellow'] > 15 and 
            colors['green'] > 30 and
            uniformity < 50):
            return self._create_result('cassava', 'mosaic_disease', 85.0)
        
        # CASSAVA BROWN STREAK: Brown streaks/lesions
        if (colors['brown'] > 15 and 
            spots['count'] > 10 and
            texture['edge_density'] > 5):
            return self._create_result('cassava', 'brown_streak', 88.0)
        
        # CASSAVA BACTERIAL BLIGHT: Water-soaked spots, wilting
        if (colors['brown'] > 10 and 
            colors['yellow'] > 10 and
            spots['count'] > 5 and
            uniformity < 40):
            return self._create_result('cassava', 'bacterial_blight', 82.0)
        
        # CASSAVA GREEN MITE: Yellow spots, curling
        if (colors['yellow'] > 12 and 
            spots['count'] > 15 and
            spots['avg_size'] < 500):
            return self._create_result('cassava', 'green_mite', 80.0)
        
        # TOMATO EARLY BLIGHT: Concentric rings, dark spots
        if (colors['brown'] > 12 and 
            spots['circularity'] > 0.6 and
            spots['count'] > 3):
            return self._create_result('tomato', 'early_blight', 86.0)
        
        # TOMATO LATE BLIGHT: Water-soaked, rapid spread
        if (colors['brown'] > 20 and 
            colors['white'] > 5 and
            texture['edge_density'] > 8):
            return self._create_result('tomato', 'late_blight', 89.0)
        
        # TOMATO BACTERIAL SPOT: Small dark spots with halos
        if (colors['brown'] > 8 and 
            colors['yellow'] > 8 and
            spots['count'] > 20 and
            spots['avg_size'] < 300):
            return self._create_result('tomato', 'bacterial_spot', 83.0)
        
        # TOMATO LEAF MOLD: Olive-green mold
        if (colors['green'] > 40 and 
            colors['brown'] > 10 and
            colors['white'] > 3 and
            uniformity < 45):
            return self._create_result('tomato', 'leaf_mold', 81.0)
        
        # POTATO EARLY BLIGHT: Similar to tomato
        if (colors['brown'] > 10 and 
            spots['circularity'] > 0.5 and
            colors['green'] > 35):
            return self._create_result('potato', 'early_blight', 84.0)
        
        # POTATO LATE BLIGHT: Severe damage
        if (colors['brown'] > 18 and 
            texture['edge_density'] > 7):
            return self._create_result('potato', 'late_blight', 87.0)
        
        # MAIZE COMMON RUST: Orange-red pustules
        if (colors['red'] > 8 and 
            spots['count'] > 10):
            return self._create_result('maize', 'common_rust', 85.0)
        
        # MAIZE NORTHERN LEAF BLIGHT: Long lesions
        if (colors['brown'] > 12 and 
            texture['edge_density'] > 6 and
            spots['avg_size'] > 800):
            return self._create_result('maize', 'northern_leaf_blight', 83.0)
        
        # PEPPER BACTERIAL SPOT: Small spots
        if (colors['brown'] > 8 and 
            colors['yellow'] > 6 and
            spots['count'] > 15):
            return self._create_result('pepper', 'bacterial_spot', 82.0)
        
        # Default: Moderate disease based on color distribution
        if colors['brown'] > 8 or colors['yellow'] > 10:
            # Determine crop based on dominant features
            if colors['yellow'] > colors['brown']:
                return self._create_result('cassava', 'mosaic_disease', 75.0)
            else:
                return self._create_result('tomato', 'early_blight', 75.0)
        
        # Fallback: Healthy
        return self._create_result('cassava', 'healthy', 78.0)

    
    def _create_result(self, crop, disease_key, confidence):
        """Create detection result from database"""
        # Get disease info from database
        disease_info = CROP_DISEASES.get(crop, {}).get(disease_key, {})
        
        if not disease_info:
            # Fallback if not in database
            return {
                'success': True,
                'crop': crop.title(),
                'disease': disease_key.replace('_', ' ').title(),
                'confidence': confidence,
                'is_healthy': 'healthy' in disease_key,
                'source': 'simple_detector'
            }
        
        return {
            'success': True,
            'crop': crop.title(),
            'disease': disease_info['name'],
            'confidence': confidence,
            'is_healthy': 'healthy' in disease_key,
            'symptoms': disease_info['symptoms'],
            'causes': disease_info['causes'],
            'treatment': disease_info['treatment'],
            'prevention': disease_info['prevention'],
            'fertilizers': disease_info['fertilizers'],
            'severity': disease_info['severity'],
            'source': 'simple_detector'
        }


# Global instance
simple_detector = SimpleDetector()
