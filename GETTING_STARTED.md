# 🚀 Getting Started with Crop Disease Detection System

Welcome! This guide will help you get the system running in just a few minutes.

## 📋 What You Need

- **Python 3.8 or higher** installed on your computer
- **10 minutes** of your time
- **Internet connection** (for installing packages)

## 🎯 Three Ways to Get Started

Choose the method that works best for you:

### Option 1: Automated Setup (Easiest) ⭐

**For Windows:**
```bash
# Just double-click these files:
1. setup.bat      # Sets everything up
2. start.bat      # Starts the application
```

**For Linux/Mac:**
```bash
# Run these commands:
chmod +x setup.sh start.sh
./setup.sh        # Sets everything up
./start.sh        # Starts the application
```

### Option 2: Manual Setup (More Control)

```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate it
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. Install packages
pip install -r requirements.txt

# 4. Setup environment
cp .env.example .env
# Edit .env and change SECRET_KEY

# 5. Initialize database
python init_db.py

# 6. Run application
python run.py
```

### Option 3: Quick Test (No Installation)

```bash
# Just want to see if everything works?
python test_installation.py
```

## 🌐 Access the Application

Once started, open your browser and go to:
```
http://localhost:5000
```

## 🔐 First Login

Use these default credentials:
- **Username:** `admin`
- **Password:** `admin123`

⚠️ **IMPORTANT:** Change this password immediately after logging in!

## 📸 Your First Scan

1. Click **"Scan"** in the navigation menu
2. Upload a crop image (or use any plant image for testing)
3. Wait a few seconds for analysis
4. View the detailed disease report!

## 🎨 What You'll See

### Home Page
- Beautiful landing page with feature overview
- Quick access to login/register

### Dashboard
- Your scan statistics
- Recent scans
- Disease trends
- Quick actions

### Scanner
- Drag-and-drop image upload
- Instant preview
- Real-time analysis
- Detailed results

### History
- All your previous scans
- Filter and search
- Delete old scans
- View detailed reports

### Admin Panel (Admin Only)
- Manage users
- View all scans
- System statistics
- Disease database

## 🔧 Configuration

### Minimum Required (.env file)

```env
SECRET_KEY=change-this-to-a-random-string
FLASK_ENV=development
```

### With AI Detection (Optional)

```env
SECRET_KEY=your-secret-key
FLASK_ENV=development
PLANT_ID_API_KEY=your-plant-id-api-key
```

Get API key from: https://web.plant.id/

## 🧪 Testing Without API Keys

The system works perfectly without API keys! It uses **mock detection** that returns realistic sample data. Perfect for:
- Testing the interface
- Learning how it works
- Demonstrating to others
- Development

## 📱 Features to Try

### As a Regular User
- ✅ Register a new account
- ✅ Upload crop images
- ✅ View disease reports
- ✅ Check your scan history
- ✅ View dashboard statistics
- ✅ Delete old scans

### As an Admin
- ✅ View all users
- ✅ Manage user accounts
- ✅ View all system scans
- ✅ Access disease database
- ✅ Grant/revoke admin access

## 🎓 Learning Path

### Day 1: Basic Usage
1. Register and login
2. Upload your first image
3. Explore the dashboard
4. View scan history

### Day 2: Advanced Features
1. Try different crop images
2. Explore disease information
3. Check statistics
4. Test on mobile device

### Day 3: Administration (If Admin)
1. Access admin panel
2. Manage users
3. View system statistics
4. Explore disease database

## 🐛 Common Issues & Solutions

### "Python not found"
**Solution:** Install Python from https://www.python.org/

### "pip not found"
**Solution:** Python 3.4+ includes pip. Reinstall Python.

### "Port 5000 already in use"
**Solution:** Edit `run.py` and change port to 5001:
```python
app.run(debug=True, port=5001)
```

### "Module not found"
**Solution:** Activate virtual environment and reinstall:
```bash
pip install -r requirements.txt
```

### "Database error"
**Solution:** Delete and recreate database:
```bash
# Windows
del instance\crop_disease.db
# Linux/Mac
rm instance/crop_disease.db

# Then reinitialize
python init_db.py
```

### "Upload failed"
**Solution:** Check that `app/static/uploads` folder exists:
```bash
# Windows
mkdir app\static\uploads
# Linux/Mac
mkdir -p app/static/uploads
```

## 📚 Next Steps

### For Users
1. **Read the full documentation:** `README.md`
2. **Get API keys:** For real disease detection
3. **Customize settings:** Edit `.env` file
4. **Invite team members:** Share the application

### For Developers
1. **Explore the code:** Check `app/` directory
2. **Read API docs:** See `README.md` API section
3. **Customize UI:** Edit `app/static/css/style.css`
4. **Add features:** Follow the modular structure

### For Deployment
1. **Read deployment guide:** `DEPLOYMENT.md`
2. **Choose platform:** PythonAnywhere, Heroku, VPS, Docker
3. **Follow checklist:** Production deployment steps
4. **Set up monitoring:** Logs and alerts

## 🎯 Quick Reference

### Important Files
- `run.py` - Start the application
- `init_db.py` - Initialize database
- `config.py` - Configuration settings
- `.env` - Environment variables
- `requirements.txt` - Python packages

### Important Folders
- `app/` - Main application code
- `app/models/` - Database models
- `app/routes/` - URL routes
- `app/templates/` - HTML templates
- `app/static/` - CSS, JS, images

### Important Commands
```bash
# Start application
python run.py

# Initialize database
python init_db.py

# Test installation
python test_installation.py

# Install packages
pip install -r requirements.txt

# Activate virtual environment
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate
```

## 💡 Pro Tips

1. **Use mock detection first** - Test without API keys
2. **Change admin password** - Security first!
3. **Try mobile view** - It's fully responsive
4. **Check the dashboard** - Great statistics
5. **Read the docs** - Comprehensive guides available

## 🆘 Getting Help

### Documentation
- **Quick Start:** This file
- **Full Documentation:** `README.md`
- **Deployment:** `DEPLOYMENT.md`
- **Project Summary:** `PROJECT_SUMMARY.md`

### Support Channels
- **GitHub Issues:** Report bugs or request features
- **Email:** support@cropcareai.com
- **Documentation:** Check README.md first

### Community
- Share your experience
- Report bugs
- Suggest features
- Contribute code

## ✅ Success Checklist

Before you start using the system:

- [ ] Python 3.8+ installed
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] .env file configured
- [ ] Database initialized
- [ ] Application starts without errors
- [ ] Can access http://localhost:5000
- [ ] Can login with admin credentials
- [ ] Admin password changed
- [ ] First scan completed successfully

## 🎉 You're Ready!

Congratulations! You now have a fully functional crop disease detection system.

### What's Next?

1. **Explore all features**
2. **Upload real crop images**
3. **Get API keys for real detection**
4. **Customize for your needs**
5. **Deploy to production**

---

**Need help? Check README.md or contact support@cropcareai.com**

**Happy farming! 🌾**
