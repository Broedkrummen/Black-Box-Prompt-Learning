# 🚀 Streamlit Cloud Deployment - Step by Step

## Prerequisites
- ✅ GitHub account
- ✅ Streamlit Cloud account (free at share.streamlit.io)

---

## Step 1: Prepare Repository for GitHub

### A. Initialize Git Repository (if not already done)

```bash
# Check if git is initialized
git status

# If not initialized, run:
git init
```

### B. Add All Files

```bash
# Add all files to git
git add .

# Check what will be committed
git status
```

### C. Commit Changes

```bash
# Commit with a message
git commit -m "SEO Dashboard - Ready for Streamlit Cloud deployment"
```

---

## Step 2: Create GitHub Repository

### Option A: Using GitHub Website

1. Go to https://github.com/new
2. Repository name: `seo-dashboard` (or your preferred name)
3. Description: "Complete SEO Analysis Dashboard with 37 API integrations"
4. Choose: **Public** (required for free Streamlit Cloud)
5. **DO NOT** initialize with README, .gitignore, or license
6. Click "Create repository"

### Option B: Using GitHub CLI

```bash
# Install GitHub CLI if needed: https://cli.github.com/

# Login
gh auth login

# Create repository
gh repo create seo-dashboard --public --source=. --remote=origin --push
```

---

## Step 3: Push to GitHub

### If you created repo via website:

```bash
# Add remote origin (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/seo-dashboard.git

# Verify remote
git remote -v

# Push to GitHub
git branch -M main
git push -u origin main
```

### Verify on GitHub:
Go to `https://github.com/YOUR_USERNAME/seo-dashboard` and verify all files are there.

---

## Step 4: Deploy on Streamlit Cloud

### A. Go to Streamlit Cloud

1. Visit: https://share.streamlit.io/
2. Click "Sign in" (use your GitHub account)
3. Authorize Streamlit to access your GitHub

### B. Create New App

1. Click "New app" button
2. Fill in the details:
   - **Repository:** `YOUR_USERNAME/seo-dashboard`
   - **Branch:** `main`
   - **Main file path:** `complete_seo_dashboard.py`
   - **App URL:** Choose a custom URL (e.g., `your-seo-dashboard`)

### C. Advanced Settings (IMPORTANT!)

Click "Advanced settings" and add your secrets:

```toml
# Add these in the secrets section:

RAPIDAPI_KEY = "5c359bb774msh32eed0a33c585c4p1466d6jsn5620b810b2f7"
VEBAPI_KEY = "de26a23c-a63c-40d1-8e0d-6803f045035f"

# Optional: If using MongoDB Atlas
MONGODB_URI = "mongodb+srv://username:password@cluster.mongodb.net/"
```

**Note:** Update with your actual API keys!

### D. Deploy

1. Click "Deploy!" button
2. Wait for deployment (usually 2-5 minutes)
3. Watch the logs for any errors

---

## Step 5: Access Your Deployed App

Your app will be live at:
```
https://YOUR_USERNAME-seo-dashboard.streamlit.app
```

Or your custom URL:
```
https://your-custom-name.streamlit.app
```

---

## Step 6: Configure MongoDB (Optional)

### Option A: Use MongoDB Atlas (Recommended for Cloud)

1. Go to https://www.mongodb.com/cloud/atlas/register
2. Create free account
3. Create free cluster (M0)
4. Get connection string
5. Add to Streamlit secrets:
   ```toml
   MONGODB_URI = "mongodb+srv://username:password@cluster.mongodb.net/"
   ```

### Option B: Run Without MongoDB

The app will work without MongoDB using session storage. Users will see a warning message.

---

## Step 7: Update Secrets (If Needed)

1. Go to your app dashboard on Streamlit Cloud
2. Click on your app
3. Click "⚙️ Settings"
4. Click "Secrets"
5. Update secrets
6. Click "Save"
7. App will automatically restart

---

## Step 8: Monitor Your App

### View Logs:
1. Go to your app on Streamlit Cloud
2. Click "Manage app"
3. View logs in real-time

### Check Status:
- Green dot = Running
- Red dot = Error (check logs)
- Yellow dot = Starting

---

## Troubleshooting

### Issue: "Module not found"
**Solution:** Check `requirements_streamlit.txt` includes all dependencies

### Issue: "Port already in use"
**Solution:** Streamlit Cloud handles ports automatically, no action needed

### Issue: "API key not found"
**Solution:** 
1. Check secrets are added correctly
2. No quotes around keys in secrets
3. Restart app after adding secrets

### Issue: "MongoDB connection failed"
**Solution:**
1. App works without MongoDB (uses session storage)
2. To use MongoDB, add MongoDB Atlas connection string to secrets
3. Ensure IP whitelist includes 0.0.0.0/0 in MongoDB Atlas

### Issue: "App is slow"
**Solution:**
1. Free tier has resource limits
2. Consider caching with `@st.cache_data`
3. Optimize API calls

---

## Updating Your Deployed App

### Method 1: Push to GitHub (Automatic)

```bash
# Make changes to your code
# Then:
git add .
git commit -m "Update: description of changes"
git push origin main

# Streamlit Cloud will automatically redeploy!
```

### Method 2: Manual Reboot

1. Go to Streamlit Cloud dashboard
2. Click on your app
3. Click "⋮" menu
4. Click "Reboot app"

---

## Custom Domain (Optional)

### Free Subdomain:
- Included: `your-app.streamlit.app`

### Custom Domain:
1. Upgrade to Streamlit Cloud Pro
2. Add your domain in settings
3. Update DNS records

---

## Sharing Your App

### Public Access:
Your app is publicly accessible at the URL

### Share Link:
```
https://YOUR_USERNAME-seo-dashboard.streamlit.app
```

### Embed in Website:
```html
<iframe src="https://YOUR_USERNAME-seo-dashboard.streamlit.app" 
        width="100%" height="800px"></iframe>
```

---

## Security Best Practices

### ✅ DO:
- Use Streamlit secrets for API keys
- Keep repository public (required for free tier)
- Use environment variables
- Enable 2FA on GitHub

### ❌ DON'T:
- Commit API keys to repository
- Share secrets publicly
- Use production keys in public repos
- Expose sensitive data

---

## Monitoring & Analytics

### Built-in Analytics:
1. Go to Streamlit Cloud dashboard
2. Click on your app
3. View:
   - Active users
   - Resource usage
   - Error logs
   - Deployment history

### External Monitoring:
- Google Analytics (add to your app)
- Custom logging
- Error tracking services

---

## Cost

### Free Tier Includes:
- ✅ 1 private app OR unlimited public apps
- ✅ 1 GB RAM
- ✅ 1 CPU core
- ✅ Community support
- ✅ Automatic HTTPS
- ✅ Custom subdomain

### Upgrade Options:
- **Starter:** $20/month - More resources
- **Team:** $250/month - Team features
- **Enterprise:** Custom pricing

---

## Quick Commands Reference

```bash
# Initialize git
git init

# Add files
git add .

# Commit
git commit -m "message"

# Add remote
git remote add origin https://github.com/USERNAME/REPO.git

# Push
git push -u origin main

# Update app (after initial deployment)
git add .
git commit -m "update"
git push
```

---

## Support

- **Streamlit Docs:** https://docs.streamlit.io/
- **Community Forum:** https://discuss.streamlit.io/
- **GitHub Issues:** https://github.com/streamlit/streamlit/issues

---

## ✅ Deployment Checklist

- [ ] Git repository initialized
- [ ] All files committed
- [ ] GitHub repository created
- [ ] Code pushed to GitHub
- [ ] Streamlit Cloud account created
- [ ] New app created on Streamlit Cloud
- [ ] Secrets added (API keys)
- [ ] App deployed successfully
- [ ] App tested and working
- [ ] MongoDB configured (optional)
- [ ] Custom URL set (optional)
- [ ] Shared with team/users

---

**Your app is now live on Streamlit Cloud! 🎉**

**URL:** `https://YOUR_USERNAME-seo-dashboard.streamlit.app`
