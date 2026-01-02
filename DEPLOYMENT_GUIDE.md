# 🚀 SEO Dashboard Deployment Guide

Complete guide for deploying the SEO Dashboard to various platforms.

---

## 📋 Pre-Deployment Checklist

- ✅ All dependencies in `requirements_streamlit.txt`
- ✅ Environment variables configured
- ✅ MongoDB connection string (if using cloud MongoDB)
- ✅ API keys secured
- ✅ Test locally before deploying

---

## 🌐 Deployment Options

### 1. Streamlit Cloud (Recommended - Free)
### 2. Heroku
### 3. AWS EC2
### 4. Google Cloud Run
### 5. Azure App Service
### 6. Docker Container

---

## 1️⃣ Streamlit Cloud Deployment (FREE)

### Prerequisites:
- GitHub account
- Streamlit Cloud account (free at share.streamlit.io)

### Steps:

#### A. Prepare Repository:

1. **Create `.streamlit/config.toml`:**
```toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"

[server]
headless = true
port = 8501
enableCORS = false
enableXsrfProtection = true
```

2. **Create `.streamlit/secrets.toml` (local only - DO NOT COMMIT):**
```toml
# API Keys
RAPIDAPI_KEY = "your_rapidapi_key_here"
VEBAPI_KEY = "your_vebapi_key_here"

# MongoDB (if using Atlas)
MONGODB_URI = "mongodb+srv://username:password@cluster.mongodb.net/"
```

3. **Update `.gitignore`:**
```
.streamlit/secrets.toml
*.pyc
__pycache__/
.env
venv/
.vscode/
```

#### B. Push to GitHub:

```bash
git init
git add .
git commit -m "Initial commit - SEO Dashboard"
git branch -M main
git remote add origin https://github.com/yourusername/seo-dashboard.git
git push -u origin main
```

#### C. Deploy on Streamlit Cloud:

1. Go to https://share.streamlit.io/
2. Click "New app"
3. Connect your GitHub repository
4. Select:
   - Repository: `yourusername/seo-dashboard`
   - Branch: `main`
   - Main file: `complete_seo_dashboard.py`
5. Click "Advanced settings"
6. Add secrets from `.streamlit/secrets.toml`
7. Click "Deploy"

**Your app will be live at:** `https://yourusername-seo-dashboard.streamlit.app`

---

## 2️⃣ Heroku Deployment

### Prerequisites:
- Heroku account
- Heroku CLI installed

### Files Needed:

#### A. Create `Procfile`:
```
web: sh setup.sh && streamlit run complete_seo_dashboard.py
```

#### B. Create `setup.sh`:
```bash
mkdir -p ~/.streamlit/

echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml
```

#### C. Create `runtime.txt`:
```
python-3.11.7
```

### Deploy:

```bash
# Login to Heroku
heroku login

# Create app
heroku create seo-dashboard-app

# Set environment variables
heroku config:set RAPIDAPI_KEY=your_key_here
heroku config:set VEBAPI_KEY=your_key_here
heroku config:set MONGODB_URI=your_mongodb_uri

# Deploy
git push heroku main

# Open app
heroku open
```

---

## 3️⃣ AWS EC2 Deployment

### Steps:

1. **Launch EC2 Instance:**
   - Ubuntu Server 22.04 LTS
   - t2.micro (free tier)
   - Open port 8501 in security group

2. **Connect and Setup:**

```bash
# SSH into instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install python3-pip python3-venv -y

# Clone repository
git clone https://github.com/yourusername/seo-dashboard.git
cd seo-dashboard

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements_streamlit.txt

# Create .env file
nano .env
# Add your API keys and MongoDB URI

# Run with nohup
nohup streamlit run complete_seo_dashboard.py --server.port 8501 &
```

3. **Access:** `http://your-ec2-ip:8501`

### Optional: Setup Nginx Reverse Proxy

```bash
sudo apt install nginx -y

# Create Nginx config
sudo nano /etc/nginx/sites-available/seo-dashboard

# Add:
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }
}

# Enable site
sudo ln -s /etc/nginx/sites-available/seo-dashboard /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## 4️⃣ Google Cloud Run Deployment

### Files Needed:

#### A. Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements_streamlit.txt .
RUN pip install --no-cache-dir -r requirements_streamlit.txt

COPY . .

EXPOSE 8080

CMD streamlit run complete_seo_dashboard.py --server.port=8080 --server.address=0.0.0.0
```

#### B. Create `.dockerignore`:
```
__pycache__
*.pyc
.git
.gitignore
venv/
.env
.streamlit/secrets.toml
```

### Deploy:

```bash
# Install Google Cloud SDK
# https://cloud.google.com/sdk/docs/install

# Login
gcloud auth login

# Set project
gcloud config set project your-project-id

# Build and deploy
gcloud run deploy seo-dashboard \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars RAPIDAPI_KEY=your_key,VEBAPI_KEY=your_key,MONGODB_URI=your_uri
```

---

## 5️⃣ Azure App Service Deployment

### Steps:

```bash
# Install Azure CLI
# https://docs.microsoft.com/en-us/cli/azure/install-azure-cli

# Login
az login

# Create resource group
az group create --name seo-dashboard-rg --location eastus

# Create App Service plan
az appservice plan create --name seo-dashboard-plan --resource-group seo-dashboard-rg --sku B1 --is-linux

# Create web app
az webapp create --resource-group seo-dashboard-rg --plan seo-dashboard-plan --name seo-dashboard-app --runtime "PYTHON:3.11"

# Configure startup command
az webapp config set --resource-group seo-dashboard-rg --name seo-dashboard-app --startup-file "streamlit run complete_seo_dashboard.py --server.port=8000 --server.address=0.0.0.0"

# Set environment variables
az webapp config appsettings set --resource-group seo-dashboard-rg --name seo-dashboard-app --settings RAPIDAPI_KEY=your_key VEBAPI_KEY=your_key MONGODB_URI=your_uri

# Deploy
az webapp up --name seo-dashboard-app --resource-group seo-dashboard-rg
```

---

## 6️⃣ Docker Container Deployment

### Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements_streamlit.txt .
RUN pip install --no-cache-dir -r requirements_streamlit.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run application
CMD ["streamlit", "run", "complete_seo_dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  seo-dashboard:
    build: .
    ports:
      - "8501:8501"
    environment:
      - RAPIDAPI_KEY=${RAPIDAPI_KEY}
      - VEBAPI_KEY=${VEBAPI_KEY}
      - MONGODB_URI=${MONGODB_URI}
    volumes:
      - ./data:/app/data
    restart: unless-stopped

  mongodb:
    image: mongo:7.0
    ports:
      - "27017:27017"
    volumes:
      - mongodb_data:/data/db
    restart: unless-stopped

volumes:
  mongodb_data:
```

### Deploy:

```bash
# Build image
docker build -t seo-dashboard .

# Run container
docker run -d -p 8501:8501 \
  -e RAPIDAPI_KEY=your_key \
  -e VEBAPI_KEY=your_key \
  -e MONGODB_URI=mongodb://mongodb:27017/ \
  --name seo-dashboard \
  seo-dashboard

# Or use docker-compose
docker-compose up -d
```

---

## 🔒 Security Best Practices

### 1. Environment Variables:
```python
import os
from dotenv import load_dotenv

load_dotenv()

RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY')
VEBAPI_KEY = os.getenv('VEBAPI_KEY')
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
```

### 2. Secrets Management:
- Use platform-specific secrets (Streamlit Cloud, Heroku Config Vars, etc.)
- Never commit API keys to Git
- Use `.env` files locally (add to `.gitignore`)

### 3. MongoDB Security:
- Enable authentication
- Use MongoDB Atlas with IP whitelist
- Use strong passwords
- Enable SSL/TLS

### 4. HTTPS:
- Use SSL certificates (Let's Encrypt for free)
- Enable HTTPS on all platforms
- Redirect HTTP to HTTPS

---

## 📊 Monitoring & Maintenance

### Streamlit Cloud:
- Built-in analytics
- View logs in dashboard
- Auto-restart on crashes

### Custom Deployments:
```bash
# View logs
docker logs seo-dashboard

# Heroku logs
heroku logs --tail

# AWS CloudWatch
# Google Cloud Logging
# Azure Monitor
```

### Health Checks:
```python
# Add to your app
import streamlit as st

@st.cache_resource
def health_check():
    return {"status": "healthy", "timestamp": datetime.now()}
```

---

## 🔄 CI/CD Pipeline

### GitHub Actions (`.github/workflows/deploy.yml`):

```yaml
name: Deploy to Streamlit Cloud

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r requirements_streamlit.txt
      
      - name: Run tests
        run: |
          python -m pytest tests/
      
      - name: Deploy to Streamlit Cloud
        # Streamlit Cloud auto-deploys on push
        run: echo "Deployed!"
```

---

## 📈 Performance Optimization

### 1. Caching:
```python
@st.cache_data(ttl=3600)
def fetch_data():
    # Expensive operation
    pass

@st.cache_resource
def init_connection():
    # Database connection
    pass
```

### 2. Lazy Loading:
- Load data on demand
- Use pagination
- Implement infinite scroll

### 3. CDN:
- Use CDN for static assets
- Enable browser caching
- Compress images

---

## 🆘 Troubleshooting

### Common Issues:

1. **Port Already in Use:**
```bash
# Kill process on port 8501
lsof -ti:8501 | xargs kill -9
```

2. **Module Not Found:**
```bash
pip install -r requirements_streamlit.txt --upgrade
```

3. **MongoDB Connection Failed:**
- Check MongoDB is running
- Verify connection string
- Check firewall rules

4. **Memory Issues:**
- Increase instance size
- Optimize caching
- Reduce concurrent users

---

## 📞 Support

- Streamlit Docs: https://docs.streamlit.io/
- Streamlit Forum: https://discuss.streamlit.io/
- GitHub Issues: Create issue in your repository

---

**Last Updated:** 2025-01-02
**Status:** ✅ Production Ready
