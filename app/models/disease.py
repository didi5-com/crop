"""
Disease database model for storing crop disease information
"""
from app import db


class DiseaseDatabase(db.Model):
    """Model for storing disease information database"""
    
    __tablename__ = 'disease_database'
    
    id = db.Column(db.Integer, primary_key=True)
    crop_name = db.Column(db.String(100), nullable=False, index=True)
    disease_name = db.Column(db.String(100), nullable=False, index=True)
    symptoms = db.Column(db.Text)
    causes = db.Column(db.Text)
    treatment = db.Column(db.Text)
    prevention = db.Column(db.Text)
    fertilizers = db.Column(db.Text)
    
    # Composite index for faster lookups
    __table_args__ = (
        db.Index('idx_crop_disease', 'crop_name', 'disease_name'),
    )
    
    def to_dict(self):
        """Convert disease info to dictionary"""
        return {
            'id': self.id,
            'crop_name': self.crop_name,
            'disease_name': self.disease_name,
            'symptoms': self.symptoms,
            'causes': self.causes,
            'treatment': self.treatment,
            'prevention': self.prevention,
            'fertilizers': self.fertilizers
        }
    
    @staticmethod
    def get_disease_info(crop_name, disease_name):
        """Get disease information from database"""
        return DiseaseDatabase.query.filter_by(
            crop_name=crop_name,
            disease_name=disease_name
        ).first()
    
    def __repr__(self):
        return f'<DiseaseDatabase {self.crop_name} - {self.disease_name}>'
