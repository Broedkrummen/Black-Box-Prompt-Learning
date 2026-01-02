# 💾 MongoDB Setup Guide for Keyword Tracker

## Overview
The Keyword Tracker page now supports MongoDB for persistent keyword storage. Keywords will automatically save to MongoDB and persist across sessions.

---

## 🚀 Quick Start

### Option 1: Local MongoDB Installation

#### Windows:
1. Download MongoDB Community Server from: https://www.mongodb.com/try/download/community
2. Run the installer (use default settings)
3. MongoDB will start automatically as a Windows service
4. Default connection: `mongodb://localhost:27017/`

#### macOS:
```bash
# Using Homebrew
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb-community
```

#### Linux (Ubuntu/Debian):
```bash
# Import MongoDB public key
wget -qO - https://www.mongodb.org/static/pgp/server-7.0.asc | sudo apt-key add -

# Add MongoDB repository
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list

# Install MongoDB
sudo apt-get update
sudo apt-get install -y mongodb-org

# Start MongoDB
sudo systemctl start mongod
sudo systemctl enable mongod
```

### Option 2: MongoDB Atlas (Cloud - Free Tier)

1. Go to https://www.mongodb.com/cloud/atlas/register
2. Create a free account
3. Create a free cluster (M0)
4. Get your connection string
5. Update `MONGODB_URI` in `pages/1_🔑_Keyword_Tracker.py`:
   ```python
   MONGODB_URI = "mongodb+srv://username:password@cluster.mongodb.net/"
   ```

---

## 📦 Install Python Dependencies

```bash
pip install pymongo
```

Or update from requirements:
```bash
pip install -r requirements_streamlit.txt
```

---

## ✅ Verify MongoDB Connection

### Check if MongoDB is running:

**Windows:**
```cmd
sc query MongoDB
```

**macOS/Linux:**
```bash
brew services list | grep mongodb
# or
sudo systemctl status mongod
```

### Test connection with Python:
```python
from pymongo import MongoClient

try:
    client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
    client.admin.command('ping')
    print("✅ MongoDB connected successfully!")
except Exception as e:
    print(f"❌ MongoDB connection failed: {e}")
```

---

## 🗄️ Database Structure

**Database Name:** `seo_dashboard`
**Collection Name:** `keywords`

**Document Structure:**
```json
{
  "_id": "seo tools_us_2025-01-02 14:30",
  "keyword": "seo tools",
  "country": "us",
  "intent": "Commercial",
  "volume": 12000,
  "cpc": 5.50,
  "competition": "High",
  "notes": "High priority keyword",
  "added_date": "2025-01-02 14:30",
  "status": "Active"
}
```

---

## 🔧 Configuration

### Default Configuration (Local):
```python
MONGODB_URI = "mongodb://localhost:27017/"
DB_NAME = "seo_dashboard"
COLLECTION_NAME = "keywords"
```

### Custom Configuration:
Edit `pages/1_🔑_Keyword_Tracker.py` and update:
```python
# MongoDB Configuration
MONGODB_URI = "your_mongodb_uri_here"
DB_NAME = "your_database_name"
COLLECTION_NAME = "your_collection_name"
```

---

## 📊 Features with MongoDB

### Automatic Persistence:
- ✅ Keywords automatically saved when added
- ✅ Keywords automatically deleted when removed
- ✅ Keywords persist across browser sessions
- ✅ Keywords persist across app restarts
- ✅ Bulk imports saved to database
- ✅ Clear all removes from database

### Fallback Mode:
If MongoDB is not available:
- ⚠️ Keywords stored in session only
- ⚠️ Keywords lost when browser closes
- ⚠️ Use CSV export to save data
- 💡 Dashboard shows warning message

---

## 🛠️ Troubleshooting

### MongoDB not connecting?

1. **Check if MongoDB is running:**
   ```bash
   # Windows
   sc query MongoDB
   
   # macOS
   brew services list
   
   # Linux
   sudo systemctl status mongod
   ```

2. **Start MongoDB:**
   ```bash
   # Windows
   net start MongoDB
   
   # macOS
   brew services start mongodb-community
   
   # Linux
   sudo systemctl start mongod
   ```

3. **Check firewall settings:**
   - Ensure port 27017 is not blocked
   - Allow MongoDB through firewall

4. **Verify connection string:**
   - Default: `mongodb://localhost:27017/`
   - Check for typos in URI

### Import errors?

```bash
# Reinstall pymongo
pip uninstall pymongo
pip install pymongo
```

---

## 📈 Benefits of MongoDB Integration

✅ **Persistent Storage** - Keywords saved permanently
✅ **Multi-User Support** - Share keywords across team
✅ **Backup & Recovery** - Easy database backups
✅ **Scalability** - Handle thousands of keywords
✅ **Query Performance** - Fast keyword lookups
✅ **Data Integrity** - ACID compliance

---

## 🔒 Security Notes

- Default local MongoDB has no authentication
- For production, enable authentication:
  ```bash
  mongod --auth
  ```
- Use MongoDB Atlas for cloud deployment with built-in security
- Never commit MongoDB credentials to version control

---

## 📚 Additional Resources

- MongoDB Documentation: https://docs.mongodb.com/
- MongoDB Atlas: https://www.mongodb.com/cloud/atlas
- PyMongo Documentation: https://pymongo.readthedocs.io/

---

**Last Updated:** 2025-01-02
**Status:** ✅ Production Ready
