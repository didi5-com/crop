# Render Deployment Plan

## Step 1 — Prepare your project

Ensure `requirements.txt` includes at least:
- Flask
- gunicorn
- requests
- Pillow
- Flask-SQLAlchemy
- python-dotenv

This repository is already configured with:

- `run.py`
```python
from app import create_app

app = create_app()
```

- `wsgi.py`
```python
from run import app

if __name__ == "__main__":
    app.run()
```

## Step 2 — Push to GitHub

```bash
git add .
git commit -m "ready for render deployment"
git push
```

## Step 3 — Deploy on Render

1. Open the Render Dashboard.
2. Click **New → Web Service**.
3. Connect your GitHub repo and select **crop**.

Use these settings:

- **Environment:** Python
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn wsgi:app`

## Step 4 — Environment variables (optional)

If you use `.env` locally, set equivalent variables in Render:

- API keys
- `SECRET_KEY`
- `FLASK_ENV=production` (recommended)

## Step 5 — Deploy

Click **Create Web Service**.

Render will:
- install dependencies
- build the app
- deploy a live URL
