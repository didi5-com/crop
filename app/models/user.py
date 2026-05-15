"""
User model for authentication and user management
"""
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db


class User(UserMixin, db.Model):
    """User model for storing user account information"""
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with scan history
    scans = db.relationship('ScanHistory', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set user password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password against hash"""
        return check_password_hash(self.password_hash, password)
    
    def get_scan_count(self):
        """Get total number of scans for this user"""
        return self.scans.count()
    
    def get_recent_scans(self, limit=5):
        """Get recent scans for this user"""
        return self.scans.order_by(ScanHistory.timestamp.desc()).limit(limit).all()
    
    def __repr__(self):
        return f'<User {self.username}>'
