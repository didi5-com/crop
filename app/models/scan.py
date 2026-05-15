"""
Scan history model for storing crop disease detection results
"""
from datetime import datetime
from app import db


class ScanHistory(db.Model):
    """Model for storing scan history and results"""
    
    __tablename__ = 'scan_history'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    image_path = db.Column(db.String(255), nullable=False)
    crop_name = db.Column(db.String(100))
    disease_name = db.Column(db.String(100))
    confidence = db.Column(db.Float)
    symptoms = db.Column(db.Text)
    causes = db.Column(db.Text)
    treatment = db.Column(db.Text)
    prevention = db.Column(db.Text)
    fertilizers = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def to_dict(self):
        """Convert scan to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'image_path': self.image_path,
            'crop_name': self.crop_name,
            'disease_name': self.disease_name,
            'confidence': self.confidence,
            'symptoms': self.symptoms,
            'causes': self.causes,
            'treatment': self.treatment,
            'prevention': self.prevention,
            'fertilizers': self.fertilizers,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }
    
    def __repr__(self):
        return f'<ScanHistory {self.id}: {self.crop_name} - {self.disease_name}>'
