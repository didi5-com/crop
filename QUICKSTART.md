# 🚀 Quick Start Guide

Get your Crop Disease Detection System up and running in 5 minutes!

## Prerequisites

- Python 3.8+ installed
- pip package manager
- Basic command line knowledge

## Installation Steps

### 1. Clone or Download the Project

```bash
git clone <repository-url>
cd crop-disease-detection
```

### 2. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

```bash
# Copy the example file
cp .env.example .env

# Edit .env and change SECRET_KEY (minimum requirement)
# You can use any text editor
```

**Minimum .env configuration:**
```
SECRET_KEY=your-random-secret-key-here-change-this
FLASK_ENV=development
```

### 5. Initialize Database

```bash
python init_db.py
```

This will:
- Create all database tables
- Create an admin user (username: `admin`, password: `admin123`)
- Add sample disease data

### 6. Run the Application

```bash
python run.py
```

### 7. Access the Application

Open your browser and go to:
```
http://localhost:5000
```

## First Steps

### 1. Login as Admin
- Username: `admin`
- Password: `admin123`
- **Important:** Change this password immediately!

### 2. Create a Regular User Account
- Click "Register" in the navigation
- Fill in your details
- Login with your new account

### 3. Upload Your First Image
- Click "Scan" in the navigation
- Upload a crop image (or use a sample image)
- View the disease detection results

### 4. Explore Features
- **Dashboard**: View your statistics
- **History**: See all your previous scans
- **Admin Panel**: Manage users and view all scans (admin only)

## Testing Without API Keys

The system works out of the box with **mock detection** for testing purposes. You'll get sample disease detection results without needing any API keys.

## Adding Real AI Detection (Optional)

To use real AI-powered detection:

### Option 1: Plant.id API (Recommended)

1. Sign up at [https://web.plant.id/](https://web.plant.id/)
2. Get your API key
3. Add to `.env`:
   ```
   PLANT_ID_API_KEY=your-api-key-here
   ```
4. Restart the application

### Option 2: PlantNet API

1. Sign up at [https://my.plantnet.org/](https://my.plantnet.org/)
2. Get your API key
3. Add to `.env`:
   ```
   PLANTNET_API_KEY=your-api-key-here
   ```
4. Restart the application

## Common Issues

### Port Already in Use

If port 5000 is already in use, edit `run.py` and change:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Changed to 5001
```

### Module Not Found Error

Make sure your virtual environment is activated:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

Then reinstall dependencies:
```bash
pip install -r requirements.txt
```

### Database Errors

Delete the database and reinitialize:
```bash
# Windows
del instance\crop_disease.db

# Linux/Mac
rm instance/crop_disease.db

# Then reinitialize
python init_db.py
```

### Upload Folder Errors

Create the uploads folder manually:
```bash
# Windows
mkdir app\static\uploads

# Linux/Mac
mkdir -p app/static/uploads
```

## Default Credentials

**Admin Account:**
- Username: `admin`
- Password: `admin123`

**⚠️ Security Warning:** Change the admin password immediately after first login!

## Next Steps

1. **Change Admin Password**: Login as admin and change the password
2. **Customize Settings**: Edit `.env` file for your needs
3. **Add API Keys**: For real disease detection
4. **Explore Admin Panel**: Manage users and view system statistics
5. **Read Full Documentation**: Check `README.md` for detailed information

## Getting Help

- **Documentation**: See `README.md`
- **Deployment Guide**: See `DEPLOYMENT.md`
- **Issues**: Check the troubleshooting section in README

## Production Deployment

For production deployment to PythonAnywhere or other platforms, see `DEPLOYMENT.md`.

---

**Happy Farming! 🌾**
