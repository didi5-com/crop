"""
Installation verification script
Tests that all components are properly installed and configured
"""
import sys
import os

def test_python_version():
    """Check Python version"""
    print("Testing Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro} (OK)")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor}.{version.micro} (Need 3.8+)")
        return False

def test_imports():
    """Test required package imports"""
    print("\nTesting package imports...")
    packages = [
        ('flask', 'Flask'),
        ('flask_sqlalchemy', 'Flask-SQLAlchemy'),
        ('flask_login', 'Flask-Login'),
        ('flask_wtf', 'Flask-WTF'),
        ('dotenv', 'python-dotenv'),
        ('PIL', 'Pillow'),
        ('werkzeug', 'Werkzeug'),
    ]
    
    all_ok = True
    for module, name in packages:
        try:
            __import__(module)
            print(f"✓ {name}")
        except ImportError:
            print(f"✗ {name} (Not installed)")
            all_ok = False
    
    return all_ok

def test_directory_structure():
    """Check if required directories exist"""
    print("\nTesting directory structure...")
    required_dirs = [
        'app',
        'app/models',
        'app/routes',
        'app/services',
        'app/utils',
        'app/static',
        'app/static/css',
        'app/static/js',
        'app/static/uploads',
        'app/templates',
    ]
    
    all_ok = True
    for directory in required_dirs:
        if os.path.exists(directory):
            print(f"✓ {directory}/")
        else:
            print(f"✗ {directory}/ (Missing)")
            all_ok = False
    
    return all_ok

def test_required_files():
    """Check if required files exist"""
    print("\nTesting required files...")
    required_files = [
        'run.py',
        'config.py',
        'requirements.txt',
        '.env.example',
        'app/__init__.py',
        'app/models/user.py',
        'app/models/scan.py',
        'app/models/disease.py',
        'app/routes/auth.py',
        'app/routes/main.py',
        'app/routes/scanner.py',
        'app/static/css/style.css',
        'app/static/js/main.js',
        'app/templates/base.html',
    ]
    
    all_ok = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file}")
        else:
            print(f"✗ {file} (Missing)")
            all_ok = False
    
    return all_ok

def test_env_file():
    """Check if .env file exists"""
    print("\nTesting environment configuration...")
    if os.path.exists('.env'):
        print("✓ .env file exists")
        
        # Check for required variables
        from dotenv import load_dotenv
        load_dotenv()
        
        secret_key = os.getenv('SECRET_KEY')
        if secret_key and secret_key != 'your-secret-key-here-change-in-production':
            print("✓ SECRET_KEY is configured")
        else:
            print("⚠ SECRET_KEY needs to be changed in .env")
        
        return True
    else:
        print("⚠ .env file not found (copy from .env.example)")
        return False

def test_flask_app():
    """Test if Flask app can be created"""
    print("\nTesting Flask application...")
    try:
        from app import create_app
        app = create_app('development')
        print("✓ Flask app created successfully")
        return True
    except Exception as e:
        print(f"✗ Failed to create Flask app: {str(e)}")
        return False

def test_database_models():
    """Test if database models can be imported"""
    print("\nTesting database models...")
    try:
        from app.models.user import User
        from app.models.scan import ScanHistory
        from app.models.disease import DiseaseDatabase
        print("✓ User model")
        print("✓ ScanHistory model")
        print("✓ DiseaseDatabase model")
        return True
    except Exception as e:
        print(f"✗ Failed to import models: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("="*60)
    print("Crop Disease Detection System - Installation Test")
    print("="*60)
    
    results = []
    
    results.append(("Python Version", test_python_version()))
    results.append(("Package Imports", test_imports()))
    results.append(("Directory Structure", test_directory_structure()))
    results.append(("Required Files", test_required_files()))
    results.append(("Environment Config", test_env_file()))
    results.append(("Flask Application", test_flask_app()))
    results.append(("Database Models", test_database_models()))
    
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{test_name:.<40} {status}")
    
    print("="*60)
    print(f"Results: {passed}/{total} tests passed")
    print("="*60)
    
    if passed == total:
        print("\n✓ All tests passed! Your installation is ready.")
        print("\nNext steps:")
        print("1. Copy .env.example to .env (if not done)")
        print("2. Edit .env and set SECRET_KEY")
        print("3. Run: python init_db.py")
        print("4. Run: python run.py")
        print("5. Visit: http://localhost:5000")
    else:
        print("\n⚠ Some tests failed. Please fix the issues above.")
        print("\nCommon fixes:")
        print("- Install missing packages: pip install -r requirements.txt")
        print("- Create missing directories manually")
        print("- Copy .env.example to .env")
        print("- Check file permissions")
    
    return passed == total

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
