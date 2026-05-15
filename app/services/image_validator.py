"""
Image validation service for quality checks before disease detection
"""
import cv2
import numpy as np
from flask import current_app


class ImageValidator:
    """Validates image quality before AI processing"""
    
    def __init__(self):
        self.min_brightness = 30
        self.max_brightness = 250
        self.min_sharpness = 100
        self.min_size = 224
        self.max_size = 4096
    
    def validate_image(self, image_path):
        """
        Comprehensive image validation
        
        Args:
            image_path: Path to image file
        
        Returns:
            dict: {
                'valid': bool,
                'issues': list of issues,
                'quality_score': float (0-100),
                'recommendations': list of recommendations
            }
        """
        try:
            # Read image
            img = cv2.imread(image_path)
            
            if img is None:
                return {
                    'valid': False,
                    'issues': ['Unable to read image file'],
                    'quality_score': 0,
                    'recommendations': ['Upload a valid image file (PNG, JPG, JPEG)']
                }
            
            issues = []
            recommendations = []
            quality_scores = []
            
            # Check 1: Image size
            height, width = img.shape[:2]
            if width < self.min_size or height < self.min_size:
                issues.append(f'Image too small ({width}x{height})')
                recommendations.append(f'Use image at least {self.min_size}x{self.min_size} pixels')
                quality_scores.append(30)
            elif width > self.max_size or height > self.max_size:
                issues.append(f'Image too large ({width}x{height})')
                recommendations.append(f'Resize image to under {self.max_size}x{self.max_size} pixels')
                quality_scores.append(70)
            else:
                quality_scores.append(100)
            
            # Check 2: Brightness
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            brightness = np.mean(gray)
            
            if brightness < self.min_brightness:
                issues.append(f'Image too dark (brightness: {brightness:.1f})')
                recommendations.append('Take photo in better lighting or increase brightness')
                quality_scores.append(40)
            elif brightness > self.max_brightness:
                issues.append(f'Image too bright (brightness: {brightness:.1f})')
                recommendations.append('Reduce exposure or avoid direct sunlight')
                quality_scores.append(60)
            else:
                quality_scores.append(100)
            
            # Check 3: Blur detection (Laplacian variance)
            laplacian = cv2.Laplacian(gray, cv2.CV_64F)
            sharpness = laplacian.var()
            
            if sharpness < self.min_sharpness:
                issues.append(f'Image too blurry (sharpness: {sharpness:.1f})')
                recommendations.append('Hold camera steady and ensure proper focus')
                quality_scores.append(50)
            else:
                quality_scores.append(100)
            
            # Check 4: Color distribution (detect if image is mostly one color)
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            color_std = np.std(hsv[:, :, 1])  # Saturation channel
            
            if color_std < 20:
                issues.append('Low color variation detected')
                recommendations.append('Ensure leaf is clearly visible with good contrast')
                quality_scores.append(60)
            else:
                quality_scores.append(100)
            
            # Check 5: Green content (should have significant green for plant images)
            green_mask = cv2.inRange(hsv, np.array([35, 40, 40]), np.array([85, 255, 255]))
            green_ratio = np.sum(green_mask > 0) / (width * height)
            
            if green_ratio < 0.1:
                issues.append('Very little green content detected')
                recommendations.append('Ensure plant leaf is the main subject')
                quality_scores.append(50)
            elif green_ratio < 0.2:
                quality_scores.append(70)
            else:
                quality_scores.append(100)
            
            # Calculate overall quality score
            overall_quality = np.mean(quality_scores)
            
            # Determine if valid
            is_valid = overall_quality >= 60 and len(issues) <= 2
            
            return {
                'valid': is_valid,
                'issues': issues,
                'quality_score': round(overall_quality, 1),
                'recommendations': recommendations,
                'metrics': {
                    'brightness': round(brightness, 1),
                    'sharpness': round(sharpness, 1),
                    'green_ratio': round(green_ratio * 100, 1),
                    'size': f'{width}x{height}'
                }
            }
        
        except Exception as e:
            current_app.logger.error(f"Error validating image: {str(e)}")
            return {
                'valid': False,
                'issues': [f'Validation error: {str(e)}'],
                'quality_score': 0,
                'recommendations': ['Try uploading a different image']
            }
    
    def preprocess_image(self, image_path, target_size=(224, 224)):
        """
        Preprocess image for AI model
        
        Args:
            image_path: Path to image
            target_size: Target dimensions
        
        Returns:
            Preprocessed numpy array
        """
        try:
            # Read image
            img = cv2.imread(image_path)
            
            # Resize
            img = cv2.resize(img, target_size, interpolation=cv2.INTER_LANCZOS4)
            
            # Enhance sharpness
            kernel = np.array([[-1,-1,-1],
                             [-1, 9,-1],
                             [-1,-1,-1]])
            img = cv2.filter2D(img, -1, kernel)
            
            # Normalize
            img = img.astype(np.float32) / 255.0
            
            # Convert BGR to RGB
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            return img
        
        except Exception as e:
            current_app.logger.error(f"Error preprocessing image: {str(e)}")
            return None


def validate_upload_image(image_path):
    """
    Convenience function to validate uploaded image
    
    Args:
        image_path: Path to image file
    
    Returns:
        Validation result dictionary
    """
    validator = ImageValidator()
    return validator.validate_image(image_path)
