"""
Database initialization script
Creates tables and optionally adds sample data
"""
import os
from app import create_app, db
from app.models.user import User
from app.models.disease import DiseaseDatabase

def init_database():
    """Initialize database with tables and sample data"""
    
    app = create_app(os.getenv('FLASK_ENV', 'development'))
    
    with app.app_context():
        # Create all tables
        print("Creating database tables...")
        db.create_all()
        print("✓ Tables created successfully!")
        
        # Check if admin user exists
        admin = User.query.filter_by(username='admin').first()
        
        if not admin:
            print("\nCreating admin user...")
            admin = User(
                username='admin',
                email='admin@cropcareai.com',
                is_admin=True
            )
            admin.set_password('admin123')  # Change this in production!
            db.session.add(admin)
            db.session.commit()
            print("✓ Admin user created!")
            print("  Username: admin")
            print("  Password: admin123")
            print("  ⚠️  IMPORTANT: Change the admin password after first login!")
        else:
            print("\n✓ Admin user already exists")
        
        # Add sample disease data
        if DiseaseDatabase.query.count() == 0:
            print("\nAdding sample disease data...")
            
            sample_diseases = [
                {
                    'crop_name': 'Tomato',
                    'disease_name': 'Early Blight',
                    'symptoms': 'Dark brown spots with concentric rings on older leaves, yellowing around spots, leaf drop',
                    'causes': 'Fungal infection caused by Alternaria solani, favored by warm humid conditions',
                    'treatment': 'Remove infected leaves | Apply copper-based fungicide | Improve air circulation | Water at base of plant',
                    'prevention': 'Crop rotation | Mulching | Proper spacing | Avoid overhead watering | Remove plant debris',
                    'fertilizers': 'Balanced NPK (10-10-10) | Calcium supplements | Organic compost | Neem oil spray'
                },
                {
                    'crop_name': 'Tomato',
                    'disease_name': 'Late Blight',
                    'symptoms': 'Water-soaked spots on leaves, white mold on undersides, rapid plant death',
                    'causes': 'Phytophthora infestans fungus, spreads rapidly in cool wet conditions',
                    'treatment': 'Remove infected plants immediately | Apply fungicide | Improve drainage',
                    'prevention': 'Resistant varieties | Good air circulation | Avoid overhead irrigation',
                    'fertilizers': 'Potassium-rich fertilizer | Copper fungicide | Organic compost'
                },
                {
                    'crop_name': 'Potato',
                    'disease_name': 'Potato Blight',
                    'symptoms': 'Brown patches on leaves, white fungal growth, tuber rot',
                    'causes': 'Phytophthora infestans, spreads in humid conditions',
                    'treatment': 'Destroy infected plants | Apply copper fungicide | Harvest early if needed',
                    'prevention': 'Plant certified seed | Crop rotation | Hill soil around plants',
                    'fertilizers': 'Balanced NPK | Copper-based fungicide | Potassium sulfate'
                },
                {
                    'crop_name': 'Wheat',
                    'disease_name': 'Rust',
                    'symptoms': 'Orange-red pustules on leaves and stems, reduced yield',
                    'causes': 'Puccinia fungus species, spreads via wind',
                    'treatment': 'Apply fungicide early | Remove infected plants | Use resistant varieties',
                    'prevention': 'Plant resistant varieties | Proper spacing | Timely planting',
                    'fertilizers': 'Nitrogen management | Zinc sulfate | Fungicide application'
                },
                {
                    'crop_name': 'Rice',
                    'disease_name': 'Blast',
                    'symptoms': 'Diamond-shaped lesions on leaves, neck rot, panicle infection',
                    'causes': 'Magnaporthe oryzae fungus, favored by high nitrogen and humidity',
                    'treatment': 'Apply systemic fungicide | Drain field temporarily | Remove infected plants',
                    'prevention': 'Resistant varieties | Balanced fertilization | Proper water management',
                    'fertilizers': 'Balanced NPK | Avoid excess nitrogen | Silica supplements | Tricyclazole fungicide'
                },
                {
                    'crop_name': 'Corn',
                    'disease_name': 'Northern Corn Leaf Blight',
                    'symptoms': 'Long gray-green lesions on leaves, reduced photosynthesis',
                    'causes': 'Exserohilum turcicum fungus, spreads in moderate temperatures',
                    'treatment': 'Apply fungicide | Remove crop residue | Use resistant hybrids',
                    'prevention': 'Crop rotation | Resistant varieties | Tillage to bury residue',
                    'fertilizers': 'Balanced NPK | Potassium for disease resistance | Fungicide spray'
                }
            ]
            
            for disease_data in sample_diseases:
                disease = DiseaseDatabase(**disease_data)
                db.session.add(disease)
            
            db.session.commit()
            print(f"✓ Added {len(sample_diseases)} sample disease records")
        else:
            print("\n✓ Disease database already contains data")
        
        print("\n" + "="*50)
        print("Database initialization complete!")
        print("="*50)
        print("\nYou can now run the application with:")
        print("  python run.py")
        print("\nDefault admin credentials:")
        print("  Username: admin")
        print("  Password: admin123")
        print("\n⚠️  Remember to change the admin password!")

if __name__ == '__main__':
    init_database()
