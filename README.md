# 🌾 CropCare AI - Crop Disease Detection System

An AI-powered web application that helps farmers detect crop diseases through image analysis and provides comprehensive treatment recommendations.

## 📋 Features

### Core Functionality
- **AI Disease Detection**: Upload crop images for instant disease analysis
- **Detailed Reports**: Get disease name, confidence score, symptoms, causes, and treatments
- **Treatment Recommendations**: Receive step-by-step treatment plans and prevention methods
- **Fertilizer Suggestions**: Get specific fertilizer and pesticide recommendations
- **Scan History**: Track all your previous scans and monitor crop health over time
- **User Dashboard**: View statistics, recent scans, and disease trends

### User Management
- **Authentication System**: Secure registration and login
- **User Profiles**: Personal dashboard with scan history
- **Admin Panel**: Manage users, view all scans, and maintain disease database

### Technical Features
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Modern UI**: Clean agricultural theme with smooth animations
- **RESTful API**: JSON API endpoints for external integrations
- **Secure**: Password hashing, CSRF protection, file validation
- **Lightweight**: Optimized for PythonAnywhere deployment

## 🛠️ Tech Stack

### Backend
- **Python 3.8+**
- **Flask** - Web framework
- **SQLAlchemy** - ORM for database operations
- **Flask-Login** - User session management
- **SQLite** - Database (easily switchable to PostgreSQL/MySQL)

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Modern styling with CSS Grid and Flexbox
- **Vanilla JavaScript** - No framework dependencies

### AI/ML
- **Plant.id API** (optional) - Professional disease detection
- **PlantNet API** (optional) - Alternative detection service
- **Mock Detection** - Built-in fallback for testing without API keys

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/crop-disease-detection.git
cd crop-disease-detection
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your configuration
# At minimum, change the SECRET_KEY
```

### Step 5: Initialize Database
```bash
python run.py
```

The database will be automatically created on first run.

### Step 6: Create Admin User (Optional)
```python
# Open Python shell
python

# Run these commands
from app import create_app, db
from app.models.user import User

app = create_app()
with app.app_context():
    admin = User(username='admin', email='admin@example.com', is_admin=True)
    admin.set_password('your-secure-password')
    db.session.add(admin)
    db.session.commit()
    print("Admin user created!")
```

### Step 7: Run the Application
```bash
python run.py
```

Visit `http://localhost:5000` in your browser.

## 🚀 Deployment to PythonAnywhere

### Step 1: Upload Files
1. Create a PythonAnywhere account (free tier available)
2. Upload your project files via Git or the Files interface

### Step 2: Create Virtual Environment
```bash
mkvirtualenv --python=/usr/bin/python3.8 cropcare
pip install -r requirements.txt
```

### Step 3: Configure WSGI
Create `/var/www/yourusername_pythonanywhere_com_wsgi.py`:

```python
import sys
import os

# Add your project directory to the sys.path
project_home = '/home/yourusername/crop-disease-detection'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set environment variables
os.environ['FLASK_ENV'] = 'production'

# Import Flask app
from app import create_app
application = create_app('production')
```

### Step 4: Configure Static Files
In PythonAnywhere web tab:
- URL: `/static/`
- Directory: `/home/yourusername/crop-disease-detection/app/static/`

### Step 5: Set Environment Variables
Add to WSGI file or use PythonAnywhere environment variables:
```python
os.environ['SECRET_KEY'] = 'your-production-secret-key'
os.environ['PLANT_ID_API_KEY'] = 'your-api-key'
```

### Step 6: Reload Web App
Click "Reload" button in PythonAnywhere web tab.

## 🔑 API Keys

### ⚠️ IMPORTANT: Get Real Disease Detection

The system has **3 detection modes**:

1. **🎭 Mock Mode (Default)** - Returns fake data for testing
2. **✅ Real AI Mode (Recommended)** - Accurate disease detection with Plant.id
3. **🌿 Alternative Mode** - Basic detection with PlantNet

### Get FREE Plant.id API Key (5 Minutes)

**Plant.id is the BEST API for crop disease detection** - it provides:
- ✅ Accurate disease identification
- ✅ Scientific disease names
- ✅ Detailed symptoms and causes
- ✅ Specific treatment recommendations
- ✅ Prevention methods
- ✅ **100 FREE requests per month**

**Quick Setup:**

1. **Sign up:** Go to [https://web.plant.id/](https://web.plant.id/)
2. **Get API key:** From your dashboard after email verification
3. **Add to .env:**
   ```env
   PLANT_ID_API_KEY=your-actual-api-key-here
   ```
4. **Restart app:** Stop and restart the application

**📖 Detailed Guide:** See [API_SETUP_GUIDE.md](API_SETUP_GUIDE.md) for step-by-step instructions with screenshots.

### Alternative: PlantNet API

1. Sign up at [https://my.plantnet.org/](https://my.plantnet.org/)
2. Get your API key
3. Add to `.env`:
   ```env
   PLANTNET_API_KEY=your-api-key-here
   ```
4. Restart the application

### Testing Without API Keys

The system works perfectly without API keys using **mock detection**. This is great for:
- Testing the interface
- Development
- Demonstrations
- Learning how the system works

**Note**: Mock detection returns realistic but fake data. For real crop disease detection, get a Plant.id API key.

## 📁 Project Structure

```
crop_disease_system/
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── models/                  # Database models
│   │   ├── user.py             # User model
│   │   ├── scan.py             # Scan history model
│   │   └── disease.py          # Disease database model
│   ├── routes/                  # Route handlers
│   │   ├── auth.py             # Authentication routes
│   │   ├── main.py             # Main pages
│   │   ├── scanner.py          # Scanner functionality
│   │   ├── dashboard.py        # User dashboard
│   │   ├── admin.py            # Admin panel
│   │   ├── api.py              # REST API endpoints
│   │   └── errors.py           # Error handlers
│   ├── services/                # Business logic
│   │   └── disease_detector.py # AI detection service
│   ├── utils/                   # Utility functions
│   │   ├── file_handler.py    # File upload handling
│   │   └── validators.py      # Form validation
│   ├── static/                  # Static files
│   │   ├── css/
│   │   │   └── style.css       # Main stylesheet
│   │   ├── js/
│   │   │   └── main.js         # JavaScript functions
│   │   ├── uploads/            # User uploaded images
│   │   └── images/             # Static images
│   └── templates/               # HTML templates
│       ├── base.html           # Base template
│       ├── auth/               # Authentication pages
│       ├── main/               # Main pages
│       ├── scanner/            # Scanner pages
│       ├── dashboard/          # Dashboard pages
│       ├── admin/              # Admin pages
│       └── errors/             # Error pages
├── instance/                    # Instance-specific files
├── config.py                    # Configuration settings
├── run.py                       # Application entry point
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variables template
├── .gitignore                   # Git ignore rules
└── README.md                    # This file
```

## 🔒 Security Features

- **Password Hashing**: Werkzeug secure password hashing
- **CSRF Protection**: Flask-WTF CSRF tokens
- **File Validation**: Secure file upload with type and size checks
- **SQL Injection Prevention**: SQLAlchemy ORM parameterized queries
- **Session Security**: Secure cookie configuration
- **Input Validation**: Form validation on client and server side

## 📊 Database Schema

### Users Table
- `id`: Primary key
- `username`: Unique username
- `email`: Unique email address
- `password_hash`: Hashed password
- `is_admin`: Admin flag
- `created_at`: Registration timestamp

### Scan History Table
- `id`: Primary key
- `user_id`: Foreign key to users
- `image_path`: Path to uploaded image
- `crop_name`: Detected crop name
- `disease_name`: Detected disease
- `confidence`: Detection confidence (0-100)
- `symptoms`: Disease symptoms
- `causes`: Disease causes
- `treatment`: Treatment recommendations
- `prevention`: Prevention methods
- `fertilizers`: Fertilizer recommendations
- `timestamp`: Scan timestamp

### Disease Database Table
- `id`: Primary key
- `crop_name`: Crop name
- `disease_name`: Disease name
- `symptoms`: Symptoms description
- `causes`: Causes description
- `treatment`: Treatment information
- `prevention`: Prevention methods
- `fertilizers`: Recommended fertilizers

## 🎨 UI/UX Features

- **Modern Design**: Clean agricultural theme with green/white colors
- **Responsive Layout**: Mobile-first design approach
- **Smooth Animations**: CSS transitions and animations
- **Drag & Drop**: Intuitive image upload interface
- **Loading States**: Visual feedback during processing
- **Flash Messages**: User-friendly notifications
- **Empty States**: Helpful messages when no data exists

## 🔧 Configuration

### Environment Variables
```bash
# Flask Configuration
SECRET_KEY=your-secret-key-here
FLASK_ENV=development

# Database
DATABASE_URL=sqlite:///crop_disease.db

# API Keys
PLANT_ID_API_KEY=your-plant-id-key
PLANTNET_API_KEY=your-plantnet-key

# Upload Settings
MAX_CONTENT_LENGTH=16777216  # 16MB
UPLOAD_FOLDER=app/static/uploads
ALLOWED_EXTENSIONS=png,jpg,jpeg,gif

# Admin Account
ADMIN_EMAIL=admin@example.com
ADMIN_USERNAME=admin
ADMIN_PASSWORD=changeme123
```

## 🧪 Testing

### Manual Testing
1. Register a new user account
2. Login with credentials
3. Upload a crop image
4. View scan results
5. Check scan history
6. Test admin panel (if admin user)

### API Testing
```bash
# Get user scans
curl http://localhost:5000/api/scans

# Get specific scan
curl http://localhost:5000/api/scans/1

# Get user stats
curl http://localhost:5000/api/stats
```

## 🐛 Troubleshooting

### Database Issues
```bash
# Delete database and recreate
rm instance/crop_disease.db
python run.py
```

### Upload Issues
- Check `UPLOAD_FOLDER` exists and is writable
- Verify file size is under `MAX_CONTENT_LENGTH`
- Ensure file extension is in `ALLOWED_EXTENSIONS`

### API Issues
- Verify API keys are correct in `.env`
- Check internet connection
- Review API rate limits
- Use mock detection for testing

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📧 Support

For support and questions:
- Email: support@cropcareai.com
- Issues: GitHub Issues page
- Documentation: See this README

## 🙏 Acknowledgments

- Plant.id for disease detection API
- PlantNet for alternative detection service
- Flask community for excellent documentation
- All contributors and testers

## 📈 Future Enhancements

- [ ] Mobile app (iOS/Android)
- [ ] Offline detection using TensorFlow Lite
- [ ] Multi-language support
- [ ] Weather integration
- [ ] Crop health tracking over time
- [ ] Community forum
- [ ] Expert consultation booking
- [ ] Marketplace for agricultural products

---

**Built with ❤️ for farmers worldwide**
