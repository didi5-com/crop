"""
Confidence filtering service - validates prediction confidence
"""
from flask import current_app


class ConfidenceFilter:
    """Filters and validates AI prediction confidence"""
    
    def __init__(self):
        # Confidence thresholds
        self.STRONG_CONFIDENCE = 90.0
        self.MEDIUM_CONFIDENCE = 75.0
        self.WEAK_CONFIDENCE = 60.0
        self.MINIMUM_ACCEPTABLE = 75.0
    
    def evaluate_confidence(self, confidence, prediction_type='disease'):
        """
        Evaluate prediction confidence
        
        Args:
            confidence: Confidence score (0-100)
            prediction_type: Type of prediction ('disease', 'crop', etc.)
        
        Returns:
            dict: {
                'acceptable': bool,
                'level': str,
                'message': str,
                'recommendation': str
            }
        """
        if confidence >= self.STRONG_CONFIDENCE:
            return {
                'acceptable': True,
                'level': 'strong',
                'message': 'High confidence detection',
                'recommendation': 'Results are highly reliable',
                'color': 'success'
            }
        
        elif confidence >= self.MEDIUM_CONFIDENCE:
            return {
                'acceptable': True,
                'level': 'medium',
                'message': 'Moderate confidence detection',
                'recommendation': 'Results are reliable but consider expert verification',
                'color': 'warning'
            }
        
        elif confidence >= self.WEAK_CONFIDENCE:
            return {
                'acceptable': False,
                'level': 'weak',
                'message': 'Low confidence detection',
                'recommendation': 'Please upload a clearer image for better results',
                'color': 'danger'
            }
        
        else:
            return {
                'acceptable': False,
                'level': 'very_weak',
                'message': 'Very low confidence detection',
                'recommendation': 'Unable to confidently detect. Please upload a better quality image',
                'color': 'danger'
            }
    
    def filter_prediction(self, prediction_data):
        """
        Filter prediction based on confidence
        
        Args:
            prediction_data: Dictionary with prediction results
        
        Returns:
            Filtered prediction data or rejection message
        """
        confidence = prediction_data.get('confidence', 0)
        
        # Evaluate confidence
        evaluation = self.evaluate_confidence(confidence)
        
        # Add evaluation to prediction data
        prediction_data['confidence_evaluation'] = evaluation
        
        # If not acceptable, modify the response
        if not evaluation['acceptable']:
            current_app.logger.warning(
                f"Low confidence prediction rejected: {confidence}%"
            )
            
            prediction_data['disease_name'] = 'Unable to Detect with Confidence'
            prediction_data['symptoms'] = (
                f"The AI model detected a possible disease but with only "
                f"{confidence:.1f}% confidence, which is below our quality threshold. "
                f"{evaluation['recommendation']}"
            )
            prediction_data['treatment'] = (
                "Please upload a clearer, well-lit image of the affected leaf for accurate detection."
            )
            prediction_data['causes'] = 'Insufficient image quality for confident detection'
            prediction_data['prevention'] = (
                "Tips for better images: "
                "1) Use good lighting "
                "2) Focus on affected area "
                "3) Avoid blurry images "
                "4) Ensure leaf is clearly visible"
            )
            prediction_data['low_confidence'] = True
        
        return prediction_data
    
    def validate_multi_predictions(self, predictions):
        """
        Validate multiple predictions and select best one
        
        Args:
            predictions: List of prediction dictionaries
        
        Returns:
            Best prediction or None
        """
        if not predictions:
            return None
        
        # Filter acceptable predictions
        acceptable = [
            p for p in predictions
            if p.get('confidence', 0) >= self.MINIMUM_ACCEPTABLE
        ]
        
        if not acceptable:
            # Return highest confidence even if below threshold
            return max(predictions, key=lambda x: x.get('confidence', 0))
        
        # Return highest confidence from acceptable predictions
        return max(acceptable, key=lambda x: x.get('confidence', 0))


def filter_by_confidence(prediction_data):
    """
    Convenience function to filter prediction by confidence
    
    Args:
        prediction_data: Prediction dictionary
    
    Returns:
        Filtered prediction data
    """
    filter_service = ConfidenceFilter()
    return filter_service.filter_prediction(prediction_data)
