# 🚀 Deployment Guide

Complete guide for deploying the Crop Disease Detection System to production.

## Table of Contents

1. [PythonAnywhere Deployment](#pythonanywhere-deployment)
2. [Heroku Deployment](#heroku-deployment)
3. [VPS Deployment](#vps-deployment)
4. [Docker Deployment](#docker-deployment)
5. [Production Checklist](#production-checklist)

---

## PythonAnywhere Deployment

PythonAnywhere offers free hosting perfect for Flask applications.

### Step 1: Create Account

1. Go to [https://www.pythonanywhere.com/](https://www.pythonanywhere.com/)
2. Sign up for a free account
3. Verify your email

### Step 2: Upload Code

**Option A: Using Git (Recommended)**

```bash
# In PythonAnywhere Bash console
git clone https://github.com/yourusername/crop-disease-detection.git
cd crop-disease-detection
```

**Option B: Upload Files**

1. Use the "Files" tab
2. Upload your project as a ZIP
3. Extract in your home directory

### Step 3: Create Virtual Environment

```bash
# In PythonAnywhere Bash console
mkvirtualenv --python=/usr/bin/python3.10 cropcare
pip install -r requirements.txt
```

### Step 4: Configure Web App

1. Go to "Web" tab
2. Click "Add a new web app"
3. Choose "Manual configuration"
4. Select Python 3.10

### Step 5: Configure WSGI File

Edit `/var/www/yourusername_pythonanywhere_com_wsgi.py`:

```python
import sys
import os

# Add project directory to path
project_home = '/home/yourusername/crop-disease-detection'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Load environment variables
from dotenv import load_dotenv
project_folder = os.path.expanduser(project_home)
load_dotenv(os.path.join(project_folder, '.env'))

# Set production environment
os.environ['FLASK_ENV'] = 'production'

# Import Flask app
from app import create_app
application = create_app('production')
```

### Step 6: Configure Static Files

In the "Web" tab, add static file mappings:

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/yourusername/crop-disease-detection/app/static/` |

### Step 7: Set Environment Variables

Create `.env` file in project directory:

```bash
# In Bash console
cd ~/crop-disease-detection
nano .env
```

Add production settings:

```env
SECRET_KEY=your-very-secure-random-secret-key-here
FLASK_ENV=production
DATABASE_URL=sqlite:///crop_disease.db
PLANT_ID_API_KEY=your-api-key-if-you-have-one
MAX_CONTENT_LENGTH=16777216
```

### Step 8: Initialize Database

```bash
# In Bash console
cd ~/crop-disease-detection
python init_db.py
```

### Step 9: Reload Web App

1. Go to "Web" tab
2. Click "Reload" button
3. Visit your site: `https://yourusername.pythonanywhere.com`

### Step 10: Change Admin Password

1. Login with default credentials (admin/admin123)
2. Change password immediately

---

## Heroku Deployment

### Prerequisites

- Heroku account
- Heroku CLI installed
- Git installed

### Step 1: Prepare Application

Create `Procfile`:

```
web: gunicorn run:app
```

Create `runtime.txt`:

```
python-3.10.12
```

Update `requirements.txt` to include:

```
gunicorn==21.2.0
psycopg2-binary==2.9.9  # For PostgreSQL
```

### Step 2: Create Heroku App

```bash
heroku login
heroku create your-app-name
```

### Step 3: Add PostgreSQL

```bash
heroku addons:create heroku-postgresql:mini
```

### Step 4: Set Environment Variables

```bash
heroku config:set SECRET_KEY=your-secret-key
heroku config:set FLASK_ENV=production
heroku config:set PLANT_ID_API_KEY=your-api-key
```

### Step 5: Deploy

```bash
git add .
git commit -m "Prepare for Heroku deployment"
git push heroku main
```

### Step 6: Initialize Database

```bash
heroku run python init_db.py
```

### Step 7: Open Application

```bash
heroku open
```

---

## VPS Deployment (Ubuntu/Debian)

### Prerequisites

- VPS with Ubuntu 20.04+ or Debian 10+
- Root or sudo access
- Domain name (optional)

### Step 1: Update System

```bash
sudo apt update
sudo apt upgrade -y
```

### Step 2: Install Dependencies

```bash
sudo apt install python3 python3-pip python3-venv nginx supervisor -y
```

### Step 3: Create Application User

```bash
sudo useradd -m -s /bin/bash cropcare
sudo su - cropcare
```

### Step 4: Clone and Setup

```bash
git clone https://github.com/yourusername/crop-disease-detection.git
cd crop-disease-detection
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

### Step 5: Configure Environment

```bash
cp .env.example .env
nano .env
```

Set production values:

```env
SECRET_KEY=your-secure-secret-key
FLASK_ENV=production
DATABASE_URL=sqlite:///crop_disease.db
```

### Step 6: Initialize Database

```bash
python init_db.py
```

### Step 7: Configure Supervisor

Exit to root user and create `/etc/supervisor/conf.d/cropcare.conf`:

```ini
[program:cropcare]
command=/home/cropcare/crop-disease-detection/venv/bin/gunicorn -w 4 -b 127.0.0.1:8000 run:app
directory=/home/cropcare/crop-disease-detection
user=cropcare
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
stderr_logfile=/var/log/cropcare/error.log
stdout_logfile=/var/log/cropcare/access.log
```

Create log directory:

```bash
sudo mkdir /var/log/cropcare
sudo chown cropcare:cropcare /var/log/cropcare
```

Start supervisor:

```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start cropcare
```

### Step 8: Configure Nginx

Create `/etc/nginx/sites-available/cropcare`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /home/cropcare/crop-disease-detection/app/static;
        expires 30d;
    }

    client_max_body_size 16M;
}
```

Enable site:

```bash
sudo ln -s /etc/nginx/sites-available/cropcare /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Step 9: Setup SSL (Optional but Recommended)

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com
```

---

## Docker Deployment

### Step 1: Create Dockerfile

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create uploads directory
RUN mkdir -p app/static/uploads

# Initialize database
RUN python init_db.py

# Expose port
EXPOSE 5000

# Run application
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "run:app"]
```

### Step 2: Create docker-compose.yml

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - SECRET_KEY=your-secret-key
      - FLASK_ENV=production
      - DATABASE_URL=sqlite:///crop_disease.db
    volumes:
      - ./instance:/app/instance
      - ./app/static/uploads:/app/app/static/uploads
    restart: unless-stopped
```

### Step 3: Build and Run

```bash
docker-compose up -d
```

### Step 4: View Logs

```bash
docker-compose logs -f
```

---

## Production Checklist

### Security

- [ ] Change SECRET_KEY to a strong random value
- [ ] Change admin password from default
- [ ] Set FLASK_ENV=production
- [ ] Enable HTTPS/SSL
- [ ] Set secure cookie flags
- [ ] Disable debug mode
- [ ] Configure firewall
- [ ] Regular security updates

### Performance

- [ ] Use production WSGI server (Gunicorn/uWSGI)
- [ ] Configure proper worker count
- [ ] Enable gzip compression
- [ ] Set up CDN for static files (optional)
- [ ] Configure caching headers
- [ ] Optimize database queries
- [ ] Set up database backups

### Monitoring

- [ ] Set up error logging
- [ ] Configure application monitoring
- [ ] Set up uptime monitoring
- [ ] Configure email alerts
- [ ] Monitor disk space
- [ ] Monitor API usage/limits

### Backup

- [ ] Regular database backups
- [ ] Backup uploaded images
- [ ] Backup configuration files
- [ ] Test restore procedures
- [ ] Off-site backup storage

### Environment Variables

Required for production:

```env
# Required
SECRET_KEY=<strong-random-key>
FLASK_ENV=production

# Database
DATABASE_URL=<your-database-url>

# API Keys (optional)
PLANT_ID_API_KEY=<your-key>
PLANTNET_API_KEY=<your-key>

# Upload Settings
MAX_CONTENT_LENGTH=16777216
UPLOAD_FOLDER=app/static/uploads
ALLOWED_EXTENSIONS=png,jpg,jpeg,gif

# Admin (change these!)
ADMIN_EMAIL=admin@yourdomain.com
ADMIN_USERNAME=admin
ADMIN_PASSWORD=<strong-password>
```

### Post-Deployment

1. **Test all features**:
   - User registration
   - Login/logout
   - Image upload
   - Disease detection
   - History viewing
   - Admin panel

2. **Monitor logs** for errors

3. **Set up regular backups**

4. **Configure monitoring alerts**

5. **Document your deployment**

---

## Troubleshooting

### Application Won't Start

- Check logs for errors
- Verify all dependencies installed
- Check environment variables
- Verify database initialized

### Static Files Not Loading

- Check static file paths
- Verify web server configuration
- Check file permissions
- Clear browser cache

### Database Errors

- Verify database file exists
- Check file permissions
- Ensure database initialized
- Check disk space

### Upload Errors

- Verify uploads directory exists
- Check directory permissions
- Verify MAX_CONTENT_LENGTH setting
- Check disk space

---

## Support

For deployment issues:

1. Check application logs
2. Review this guide
3. Check README.md
4. Search existing issues
5. Create new issue with details

---

**Good luck with your deployment! 🚀**
