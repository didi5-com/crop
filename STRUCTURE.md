# 📁 Project Structure

Complete directory structure of the Crop Disease Detection System.

## Overview

```
crop_disease_system/
├── 📱 Application Code
├── 🎨 Frontend Assets
├── 📄 Templates
├── 🗄️ Database
├── ⚙️ Configuration
├── 📚 Documentation
└── 🛠️ Setup Scripts
```

## Detailed Structure

```
crop_disease_system/
│
├── app/                                    # Main application package
│   ├── __init__.py                        # Flask app factory & extensions
│   │
│   ├── models/                            # Database models (SQLAlchemy)
│   │   ├── __init__.py
│   │   ├── user.py                        # User model (authentication)
│   │   ├── scan.py                        # ScanHistory model (results)
│   │   └── disease.py                     # DiseaseDatabase model (info)
│   │
│   ├── routes/                            # Route handlers (Blueprints)
│   │   ├── __init__.py
│   │   ├── auth.py                        # Authentication routes
│   │   ├── main.py                        # Main pages (home, about)
│   │   ├── scanner.py                     # Scanner functionality
│   │   ├── dashboard.py                   # User dashboard
│   │   ├── admin.py                       # Admin panel
│   │   ├── api.py                         # REST API endpoints
│   │   └── errors.py                      # Error handlers
│   │
│   ├── services/                          # Business logic layer
│   │   ├── __init__.py
│   │   └── disease_detector.py            # AI detection service
│   │
│   ├── utils/                             # Utility functions
│   │   ├── __init__.py
│   │   ├── file_handler.py               # File upload handling
│   │   └── validators.py                 # Form validation
│   │
│   ├── static/                            # Static files (CSS, JS, images)
│   │   ├── css/
│   │   │   └── style.css                 # Main stylesheet
│   │   ├── js/
│   │   │   └── main.js                   # JavaScript functions
│   │   ├── images/                       # Static images
│   │   └── uploads/                      # User uploaded images
│   │       └── .gitkeep                  # Keep folder in git
│   │
│   └── templates/                         # Jinja2 HTML templates
│       ├── base.html                      # Base template (layout)
│       │
│       ├── auth/                          # Authentication pages
│       │   ├── login.html                # Login page
│       │   └── register.html             # Registration page
│       │
│       ├── main/                          # Main pages
│       │   ├── index.html                # Home page
│       │   ├── about.html                # About page
│       │   └── contact.html              # Contact page
│       │
│       ├── scanner/                       # Scanner pages
│       │   ├── upload.html               # Upload interface
│       │   ├── result.html               # Scan results
│       │   └── history.html              # Scan history
│       │
│       ├── dashboard/                     # Dashboard pages
│       │   └── index.html                # User dashboard
│       │
│       ├── admin/                         # Admin pages
│       │   ├── index.html                # Admin dashboard
│       │   ├── users.html                # User management
│       │   ├── scans.html                # All scans
│       │   └── diseases.html             # Disease database
│       │
│       └── errors/                        # Error pages
│           ├── 403.html                  # Forbidden
│           ├── 404.html                  # Not found
│           ├── 413.html                  # File too large
│           └── 500.html                  # Server error
│
├── instance/                              # Instance-specific files
│   └── crop_disease.db                   # SQLite database (created)
│
├── venv/                                  # Virtual environment (created)
│   ├── Scripts/                          # Windows executables
│   ├── bin/                              # Linux/Mac executables
│   └── Lib/                              # Python packages
│
├── .kiro/                                 # Kiro IDE configuration
│   └── specs/                            # Spec files
│       └── crop-disease-detection-system/
│           └── design.md                 # Design document
│
├── config.py                              # Configuration classes
├── run.py                                 # Application entry point
├── init_db.py                             # Database initialization
├── test_installation.py                   # Installation verification
│
├── requirements.txt                       # Python dependencies
├── .env                                   # Environment variables (create)
├── .env.example                           # Environment template
├── .gitignore                             # Git ignore rules
│
├── setup.bat                              # Windows setup script
├── start.bat                              # Windows start script
├── setup.sh                               # Linux/Mac setup script
├── start.sh                               # Linux/Mac start script
│
├── README.md                              # Main documentation
├── QUICKSTART.md                          # Quick start guide
├── DEPLOYMENT.md                          # Deployment guide
├── GETTING_STARTED.md                     # Getting started guide
├── PROJECT_SUMMARY.md                     # Project summary
├── STRUCTURE.md                           # This file
├── CHANGELOG.md                           # Version history
└── LICENSE                                # MIT License
```

## File Descriptions

### Core Application Files

| File | Purpose |
|------|---------|
| `run.py` | Application entry point, starts Flask server |
| `config.py` | Configuration classes for different environments |
| `init_db.py` | Database initialization with sample data |
| `test_installation.py` | Verify installation is correct |

### Configuration Files

| File | Purpose |
|------|---------|
| `.env` | Environment variables (create from .env.example) |
| `.env.example` | Template for environment variables |
| `requirements.txt` | Python package dependencies |
| `.gitignore` | Files to ignore in git |

### Setup Scripts

| File | Purpose |
|------|---------|
| `setup.bat` | Automated setup for Windows |
| `start.bat` | Start application on Windows |
| `setup.sh` | Automated setup for Linux/Mac |
| `start.sh` | Start application on Linux/Mac |

### Documentation Files

| File | Purpose |
|------|---------|
| `README.md` | Complete project documentation |
| `QUICKSTART.md` | 5-minute quick start guide |
| `DEPLOYMENT.md` | Production deployment guide |
| `GETTING_STARTED.md` | Beginner-friendly guide |
| `PROJECT_SUMMARY.md` | Project overview and features |
| `STRUCTURE.md` | This file - project structure |
| `CHANGELOG.md` | Version history and changes |
| `LICENSE` | MIT License |

## Module Breakdown

### Models (`app/models/`)

**Purpose:** Database schema definitions

- `user.py` - User accounts and authentication
- `scan.py` - Scan history and results
- `disease.py` - Disease information database

### Routes (`app/routes/`)

**Purpose:** URL routing and request handling

- `auth.py` - Login, register, logout
- `main.py` - Home, about, contact pages
- `scanner.py` - Upload, scan, results, history
- `dashboard.py` - User dashboard and statistics
- `admin.py` - Admin panel and management
- `api.py` - REST API endpoints
- `errors.py` - Error page handlers

### Services (`app/services/`)

**Purpose:** Business logic and external integrations

- `disease_detector.py` - AI disease detection logic

### Utils (`app/utils/`)

**Purpose:** Helper functions and utilities

- `file_handler.py` - File upload and image processing
- `validators.py` - Form validation classes

### Templates (`app/templates/`)

**Purpose:** HTML templates with Jinja2

- `base.html` - Base layout template
- `auth/` - Authentication pages
- `main/` - Public pages
- `scanner/` - Scanner functionality
- `dashboard/` - User dashboard
- `admin/` - Admin panel
- `errors/` - Error pages

### Static Files (`app/static/`)

**Purpose:** CSS, JavaScript, and images

- `css/style.css` - Main stylesheet
- `js/main.js` - JavaScript functions
- `images/` - Static images
- `uploads/` - User uploaded images

## Database Structure

### Tables

```
users
├── id (Primary Key)
├── username (Unique)
├── email (Unique)
├── password_hash
├── is_admin
└── created_at

scan_history
├── id (Primary Key)
├── user_id (Foreign Key → users.id)
├── image_path
├── crop_name
├── disease_name
├── confidence
├── symptoms
├── causes
├── treatment
├── prevention
├── fertilizers
└── timestamp

disease_database
├── id (Primary Key)
├── crop_name
├── disease_name
├── symptoms
├── causes
├── treatment
├── prevention
└── fertilizers
```

## URL Structure

### Public Routes
```
/                           # Home page
/about                      # About page
/contact                    # Contact page
/auth/login                 # Login page
/auth/register              # Registration page
/auth/logout                # Logout action
```

### Authenticated Routes
```
/dashboard                  # User dashboard
/scanner                    # Upload page
/scanner/upload             # Upload action
/scanner/result/<id>        # View result
/scanner/history            # Scan history
/scanner/delete/<id>        # Delete scan
```

### API Routes
```
/api/scans                  # Get user scans (JSON)
/api/scans/<id>             # Get scan details (JSON)
/api/diseases               # Get disease info (JSON)
/api/stats                  # Get user stats (JSON)
```

### Admin Routes
```
/admin                      # Admin dashboard
/admin/users                # User management
/admin/scans                # All scans
/admin/diseases             # Disease database
/admin/users/delete/<id>    # Delete user
/admin/users/toggle-admin/<id>  # Toggle admin
```

## Key Directories

### Created During Setup
- `venv/` - Virtual environment
- `instance/` - Database and instance files
- `app/static/uploads/` - User uploaded images

### Ignored by Git
- `venv/` - Virtual environment
- `instance/` - Database files
- `app/static/uploads/*` - Uploaded images
- `.env` - Environment variables
- `__pycache__/` - Python cache
- `*.pyc` - Compiled Python files

## Import Structure

```python
# Application factory
from app import create_app, db

# Models
from app.models.user import User
from app.models.scan import ScanHistory
from app.models.disease import DiseaseDatabase

# Services
from app.services.disease_detector import analyze_crop_image

# Utils
from app.utils.file_handler import save_upload_image
from app.utils.validators import RegistrationForm, LoginForm
```

## Configuration Hierarchy

```
config.py
├── Config (Base)
│   ├── DevelopmentConfig
│   ├── ProductionConfig
│   └── TestingConfig
```

## Template Inheritance

```
base.html (Base template)
├── main/index.html
├── auth/login.html
├── auth/register.html
├── scanner/upload.html
├── scanner/result.html
├── scanner/history.html
├── dashboard/index.html
├── admin/index.html
├── admin/users.html
├── admin/scans.html
├── admin/diseases.html
└── errors/*.html
```

## Static File Organization

```
static/
├── css/
│   └── style.css           # All styles in one file
├── js/
│   └── main.js             # All JavaScript in one file
├── images/
│   └── (static images)
└── uploads/
    └── (user uploads)
```

## Development Workflow

```
1. Edit code in app/
2. Test locally with run.py
3. Check with test_installation.py
4. Commit changes
5. Deploy to production
```

## Production Structure

```
Production Server
├── /home/user/crop-disease-detection/  # Application
├── /var/log/cropcare/                  # Logs
├── /etc/nginx/sites-available/         # Nginx config
└── /etc/supervisor/conf.d/             # Supervisor config
```

---

**This structure follows Flask best practices and is designed for scalability and maintainability.**
