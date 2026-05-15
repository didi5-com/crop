"""
Main entry point for the Crop Disease Detection System
"""
import os
from app import create_app, db
from app.models.user import User
from app.models.scan import ScanHistory
from app.models.disease import DiseaseDatabase

# Create Flask application
app = create_app(os.getenv('FLASK_ENV', 'development'))

# Shell context for flask shell command
@app.shell_context_processor
def make_shell_context():
    """Make database models available in flask shell"""
    return {
        'db': db,
        'User': User,
        'ScanHistory': ScanHistory,
        'DiseaseDatabase': DiseaseDatabase
    }

# Create database tables
with app.app_context():
    db.create_all()
    print("Database tables created successfully!")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
