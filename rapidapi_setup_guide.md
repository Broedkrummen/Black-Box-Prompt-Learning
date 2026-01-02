# RapidAPI Ahrefs Setup Guide

## Current Status
❌ **Error**: "You are not subscribed to this API"

Your RapidAPI key is valid, but you need to subscribe to the Ahrefs Domain Research API.

## How to Subscribe

### Step 1: Visit RapidAPI
Go to: https://rapidapi.com/apimaker/api/ahrefs-domain-research

### Step 2: Subscribe to a Plan
Choose one of these plans:

#### Free Plan (BASIC)
- **Cost**: FREE
- **Requests**: 100 requests/month
- **Rate Limit**: 1 request/second
- **Features**: 
  - Domain overview
  - Backlinks (limited)
  - Referring domains
  - Anchor texts

#### Pro Plan
- **Cost**: $9.99/month
- **Requests**: 1,000 requests/month
- **Rate Limit**: 10 requests/second
- **Features**: All features + more data

#### Ultra Plan
- **Cost**: $49.99/month
- **Requests**: 10,000 requests/month
- **Rate Limit**: 100 requests/second
- **Features**: All features + maximum data

### Step 3: Subscribe
1. Click "Subscribe to Test" button
2. Select your plan (start with FREE)
3. Confirm subscription
4. Your existing API key will work automatically

### Step 4: Test the API
After subscribing, run:
```bash
python rapidapi_ahrefs_checker.py
```

## Alternative: Use Ahrefs Webmaster Tools (100% Free)

If you don't want to use RapidAPI, you can get the same data for FREE:

### Option 1: Ahrefs Webmaster Tools
1. Go to: https://ahrefs.com/webmaster-tools
2. Sign up for free account
3. Add your domain
4. Verify ownership (add meta tag or DNS record)
5. Get complete backlink data including:
   - Domain Rating (DR)
   - URL Rating (UR)
   - Backlinks
   - Referring domains
   - Anchor texts
   - Traffic estimates
   - Historical data

### Option 2: Google Search Console (Most Accurate)
1. Go to: https://search.google.com/search-console
2. Add property
3. Verify ownership
4. Navigate to: Links > External links
5. Export complete backlink data
6. Benefits:
   - Most accurate (Google's own data)
   - Shows all backlinks Google knows
   - Free and unlimited
   - No API limits

## API Endpoints Available

Once subscribed, you can use these endpoints:

### 1. Domain Overview
```
GET /domain-overview?domain=simplybeyond.dk
```
Returns: DR, backlinks count, referring domains, organic traffic

### 2. Backlinks
```
GET /backlinks?domain=simplybeyond.dk&limit=100
```
Returns: List of backlinks with source URL, anchor text, DR

### 3. Referring Domains
```
GET /referring-domains?domain=simplybeyond.dk&limit=100
```
Returns: List of domains linking to you

### 4. Anchor Texts
```
GET /anchors?domain=simplybeyond.dk&limit=100
```
Returns: Anchor text distribution

### 5. Top Pages
```
GET /top-pages?domain=simplybeyond.dk&limit=100
```
Returns: Most linked pages on your site

## Recommendation

**For simplybeyond.dk backlink analysis:**

1. **Best Option**: Use Ahrefs Webmaster Tools (Free)
   - Complete data
   - No API limits
   - Historical tracking
   - Broken link detection

2. **Second Best**: Google Search Console (Free)
   - Most accurate
   - Direct from Google
   - Export to CSV

3. **Third Option**: RapidAPI (Free tier available)
   - Good for automation
   - 100 requests/month free
   - Programmatic access

## Current Script Status

The script `rapidapi_ahrefs_checker.py` is ready to use once you:
1. Subscribe to the API on RapidAPI
2. Run the script again

Your API key is already configured in the script.

## Questions?

If you need help:
1. Check RapidAPI documentation: https://rapidapi.com/apimaker/api/ahrefs-domain-research
2. Review Ahrefs Webmaster Tools: https://ahrefs.com/webmaster-tools
3. Set up Google Search Console: https://search.google.com/search-console
