# 🚀 VEBAPI Quick Start Guide

## Getting Started in 5 Minutes

### 1. API Configuration
```python
VEBAPI_KEY = "de26a23c-a63c-40d1-8e0d-6803f045035f"
BASE_URL = "https://vebapi.com/api"
```

### 2. Basic Request Example
```python
import http.client
import json

conn = http.client.HTTPSConnection("vebapi.com")
headers = {
    'X-API-KEY': VEBAPI_KEY,
    'Content-Type': 'application/json'
}

conn.request("GET", "/api/seo/singlekeyword?keyword=seo&country=us", headers=headers)
response = conn.getresponse()
data = json.loads(response.read())
print(data)
```

---

## 📋 Available Endpoints

### Keyword Research
```python
# Get keyword suggestions
GET /api/seo/keywordresearch?keyword={keyword}&country={country}

# Get single keyword metrics
GET /api/seo/singlekeyword?keyword={keyword}&country={country}

# Analyze keyword density
GET /api/seo/keyworddensity?keyword={keyword}&website={domain}
```

### On-Page SEO
```python
# Page analysis
GET /api/seo/analyze?website={domain}

# AI search analyzer
GET /api/seo/apipagechecker?website={domain}

# AI SEO crawler check
GET /api/seo/aiseochecker?website={domain}

# Loading speed
GET /api/seo/loadingspeeddata?website={domain}
```

### Backlink Analysis
```python
# Get all backlinks
GET /api/seo/backlinkdata?website={domain}

# Get new backlinks
GET /api/seo/newbacklinks?website={domain}

# Get poor quality backlinks
GET /api/seo/poorbacklinks?website={domain}

# Get referring domains
GET /api/seo/referraldomains?website={domain}

# Get top ranking keywords
GET /api/seo/topsearchkeywords?website={domain}
```

### Domain Intelligence
```python
# Get domain data
GET /api/seo/domainnamedata?website={domain}
```

---

## 🎯 Common Use Cases

### Use Case 1: Keyword Research
```python
# Find related keywords for content planning
keyword = "digital marketing"
country = "us"

result = analyze_vebapi_related_keywords(keyword, country)
if result['success']:
    keywords = result['data']
    for kw in keywords[:10]:  # Top 10
        print(f"{kw['text']}: Vol={kw['vol']}, CPC=${kw['cpc']}")
```

### Use Case 2: Competitor Backlink Analysis
```python
# Analyze competitor backlinks
domain = "competitor.com"

backlinks = get_backlink_data(domain)
referrers = get_referral_domains(domain)

print(f"Total Backlinks: {backlinks['counts']['backlinks']['total']}")
print(f"Referring Domains: {len(referrers['referrers'])}")
```

### Use Case 3: Site Speed Audit
```python
# Check page load speed
domain = "yoursite.com"

speed_data = get_loading_speed(domain)
load_time = speed_data['data']['total_time']

if load_time < 1.0:
    print("✅ Excellent speed!")
elif load_time < 3.0:
    print("⚠️ Good, but could improve")
else:
    print("❌ Needs optimization")
```

---

## 🧪 Testing Your Integration

### Run Comprehensive Tests
```bash
python test_vebapi.py
```

### Run Dashboard Function Tests
```bash
python test_dashboard_functions.py
```

### Check Test Results
```bash
cat vebapi_test_results.json
```

---

## 📊 Response Examples

### Keyword Research Response
```json
{
  "text": "seo",
  "cpc": "15.20",
  "vol": 450000,
  "v": 450000,
  "competition": "Very high",
  "score": "3.04"
}
```

### Backlink Data Response
```json
{
  "counts": {
    "backlinks": {
      "total": 28,
      "doFollow": 25,
      "toHomePage": 8
    },
    "domains": {
      "total": 13,
      "doFollow": 11
    }
  },
  "backlinks": [...]
}
```

### AI Search Analyzer Response
```json
{
  "url": "https://example.com",
  "ai_scrapable": true,
  "content_quality_score": 100,
  "flags": {
    "title": true,
    "headings": 18,
    "paragraphs": 63,
    "schema_data_found": true
  }
}
```

---

## ⚠️ Error Handling

### Handle API Errors
```python
def safe_api_call(endpoint, params):
    try:
        result = call_vebapi(endpoint, params)
        if result['success']:
            return result['data']
        else:
            print(f"API Error: {result.get('error')}")
            return None
    except Exception as e:
        print(f"Exception: {e}")
        return None
```

### Common Error Codes
- **401:** Invalid API key
- **404:** Endpoint not found
- **429:** Rate limit exceeded
- **500:** Server error

---

## 💡 Best Practices

### 1. Rate Limiting
```python
import time

def batch_analyze(domains):
    results = []
    for domain in domains:
        result = analyze_domain(domain)
        results.append(result)
        time.sleep(1)  # Respect rate limits
    return results
```

### 2. Caching Results
```python
import json
from datetime import datetime, timedelta

cache = {}

def get_cached_or_fetch(domain):
    if domain in cache:
        cached_time, data = cache[domain]
        if datetime.now() - cached_time < timedelta(hours=24):
            return data
    
    data = fetch_from_api(domain)
    cache[domain] = (datetime.now(), data)
    return data
```

### 3. Error Recovery
```python
def fetch_with_retry(endpoint, params, max_retries=3):
    for attempt in range(max_retries):
        try:
            return call_api(endpoint, params)
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)  # Exponential backoff
```

---

## 📈 Performance Tips

1. **Batch Requests:** Group similar requests together
2. **Cache Results:** Store frequently accessed data
3. **Async Calls:** Use async for multiple endpoints
4. **Monitor Usage:** Track API call volume
5. **Optimize Queries:** Only request needed data

---

## 🔗 Useful Links

- **Test Script:** `test_vebapi.py`
- **Dashboard Functions:** `test_dashboard_functions.py`
- **Full Documentation:** `VEBAPI_FINAL_INTEGRATION_REPORT.md`
- **Test Results:** `COMPREHENSIVE_TEST_REPORT.md`
- **API Spec:** `api-1.json`

---

## 🆘 Troubleshooting

### Issue: 401 Unauthorized
**Solution:** Check API key is correct and properly set in headers

### Issue: Empty Response
**Solution:** Verify domain format (no http://, just domain.com)

### Issue: Slow Response
**Solution:** Normal for backlink endpoints (2-3 seconds)

### Issue: Rate Limit
**Solution:** Add delays between requests (1 second minimum)

---

## ✅ Checklist for Production

- [ ] API key stored in environment variables
- [ ] Error handling implemented
- [ ] Rate limiting respected
- [ ] Caching layer added
- [ ] Monitoring set up
- [ ] Logging configured
- [ ] Tests passing
- [ ] Documentation updated

---

**Last Updated:** 2025-01-02  
**Version:** 1.0  
**Status:** Production Ready
