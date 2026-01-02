"""
Test script for new RapidAPI endpoints
Based on the provided API documentation links
"""

import http.client
import json
import time
from urllib.parse import quote

RAPIDAPI_KEY = "5c359bb774msh32eed0a33c585c4p1466d6jsn5620b810b2f7"

def test_seo_api_backlinks(domain):
    """Test SEO API - DR, RD, Rank, Keywords, Backlinks"""
    print("\n" + "="*80)
    print("🧪 TESTING SEO API (Backlinks)")
    print("="*80)
    
    try:
        conn = http.client.HTTPSConnection("seo-api-dr-rd-rank-keywords-backlinks1.p.rapidapi.com")
        headers = {
            'x-rapidapi-key': RAPIDAPI_KEY,
            'x-rapidapi-host': "seo-api-dr-rd-rank-keywords-backlinks1.p.rapidapi.com"
        }
        
        encoded_url = quote(domain, safe='')
        endpoint = f"/backlink-checker?mode=subdomains&url={encoded_url}&limit=100"
        print(f"📡 Endpoint: {endpoint}")
        
        conn.request("GET", endpoint, headers=headers)
        res = conn.getresponse()
        data = json.loads(res.read().decode("utf-8"))
        
        print(f"📊 Status: {res.status}")
        
        if data.get("success"):
            backlinks = data.get("data", {}).get("backlinks", [])
            overview = data.get("data", {}).get("overview", {})
            print("✅ SUCCESS")
            print(f"   Domain Rating: {overview.get('domainRating', 'N/A')}")
            print(f"   Backlinks: {overview.get('backlinks', 'N/A')}")
            print(f"   Referring Domains: {overview.get('referringDomains', 'N/A')}")
            return True, data
        else:
            print("❌ FAILED")
            print(f"   Response: {json.dumps(data, indent=2)[:500]}")
            return False, data
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False, str(e)

def test_ahrefs_domain_research(domain):
    """Test Ahrefs Domain Research API"""
    print("\n" + "="*80)
    print("🧪 TESTING AHREFS DOMAIN RESEARCH API")
    print("="*80)
    
    try:
        conn = http.client.HTTPSConnection("ahrefs-domain-research.p.rapidapi.com")
        headers = {
            'x-rapidapi-key': RAPIDAPI_KEY,
            'x-rapidapi-host': "ahrefs-domain-research.p.rapidapi.com"
        }
        
        endpoint = f"/basic-metrics?url={domain}"
        print(f"📡 Endpoint: {endpoint}")
        
        conn.request("GET", endpoint, headers=headers)
        res = conn.getresponse()
        data = json.loads(res.read().decode("utf-8"))
        
        print(f"📊 Status: {res.status}")
        
        if "domainRating" in data or "ahrefs_rank" in data:
            print("✅ SUCCESS")
            print(f"   Domain Rating: {data.get('domainRating', 'N/A')}")
            print(f"   Ahrefs Rank: {data.get('ahrefs_rank', 'N/A')}")
            print(f"   Backlinks: {data.get('backlinks', 'N/A')}")
            return True, data
        else:
            print("❌ FAILED")
            print(f"   Response: {json.dumps(data, indent=2)[:500]}")
            return False, data
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False, str(e)

def test_semrush_keyword_magic(keyword):
    """Test SEMrush Keyword Magic Tool API"""
    print("\n" + "="*80)
    print("🧪 TESTING SEMRUSH KEYWORD MAGIC TOOL API")
    print("="*80)
    
    try:
        conn = http.client.HTTPSConnection("semrush-keyword-magic-tool.p.rapidapi.com")
        headers = {
            'x-rapidapi-key': RAPIDAPI_KEY,
            'x-rapidapi-host': "semrush-keyword-magic-tool.p.rapidapi.com"
        }
        
        endpoint = f"/keyword-magic-tool?keyword={quote(keyword)}&database=dk"
        print(f"📡 Endpoint: {endpoint}")
        
        conn.request("GET", endpoint, headers=headers)
        res = conn.getresponse()
        data = json.loads(res.read().decode("utf-8"))
        
        print(f"📊 Status: {res.status}")
        
        if isinstance(data, list) and len(data) > 0:
            print("✅ SUCCESS")
            print(f"   Keywords found: {len(data)}")
            print(f"   First keyword: {data[0].get('keyword', 'N/A')}")
            print(f"   Search Volume: {data[0].get('search_volume', 'N/A')}")
            return True, data
        elif isinstance(data, dict) and data.get("keywords"):
            print("✅ SUCCESS")
            keywords = data.get("keywords", [])
            print(f"   Keywords found: {len(keywords)}")
            return True, data
        else:
            print("❌ FAILED")
            print(f"   Response: {json.dumps(data, indent=2)[:500]}")
            return False, data
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False, str(e)

def test_website_analyze_seo_audit(domain):
    """Test Website Analyze and SEO Audit Pro API"""
    print("\n" + "="*80)
    print("🧪 TESTING WEBSITE ANALYZE AND SEO AUDIT PRO API")
    print("="*80)
    
    try:
        conn = http.client.HTTPSConnection("website-analyze-and-seo-audit-pro.p.rapidapi.com")
        headers = {
            'x-rapidapi-key': RAPIDAPI_KEY,
            'x-rapidapi-host': "website-analyze-and-seo-audit-pro.p.rapidapi.com"
        }
        
        endpoint = f"/seo-audit?url={domain}"
        print(f"📡 Endpoint: {endpoint}")
        
        conn.request("GET", endpoint, headers=headers)
        res = conn.getresponse()
        data = json.loads(res.read().decode("utf-8"))
        
        print(f"📊 Status: {res.status}")
        
        if data and isinstance(data, dict):
            print("✅ SUCCESS")
            print(f"   Response keys: {list(data.keys())[:5]}")
            return True, data
        else:
            print("❌ FAILED")
            print(f"   Response: {json.dumps(data, indent=2)[:500]}")
            return False, data
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False, str(e)

def test_seo_api2(domain):
    """Test SEO API2"""
    print("\n" + "="*80)
    print("🧪 TESTING SEO API2")
    print("="*80)
    
    try:
        conn = http.client.HTTPSConnection("seo-api2.p.rapidapi.com")
        headers = {
            'x-rapidapi-key': RAPIDAPI_KEY,
            'x-rapidapi-host': "seo-api2.p.rapidapi.com"
        }
        
        endpoint = f"/domain-overview?domain={domain}"
        print(f"📡 Endpoint: {endpoint}")
        
        conn.request("GET", endpoint, headers=headers)
        res = conn.getresponse()
        data = json.loads(res.read().decode("utf-8"))
        
        print(f"📊 Status: {res.status}")
        
        if data and isinstance(data, dict):
            print("✅ SUCCESS")
            print(f"   Response keys: {list(data.keys())[:5]}")
            return True, data
        else:
            print("❌ FAILED")
            print(f"   Response: {json.dumps(data, indent=2)[:500]}")
            return False, data
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False, str(e)

def main():
    print("="*80)
    print("🧪 TESTING NEW RAPIDAPI ENDPOINTS")
    print("="*80)
    
    domain = "simplybeyond.dk"
    keyword = "hudpleje"
    
    results = {}
    
    # Test all APIs
    results['seo_api_backlinks'] = test_seo_api_backlinks(domain)
    time.sleep(2)
    
    results['ahrefs_domain_research'] = test_ahrefs_domain_research(domain)
    time.sleep(2)
    
    results['semrush_keyword_magic'] = test_semrush_keyword_magic(keyword)
    time.sleep(2)
    
    results['website_analyze_seo_audit'] = test_website_analyze_seo_audit(domain)
    time.sleep(2)
    
    results['seo_api2'] = test_seo_api2(domain)
    
    # Summary
    print("\n" + "="*80)
    print("📊 TEST SUMMARY")
    print("="*80)
    
    total_tests = len(results)
    passed_tests = sum(1 for success, _ in results.values() if success)
    
    for api_name, (success, data) in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {api_name.upper().replace('_', ' ')}")
    
    print("\n" + "="*80)
    print(f"RESULTS: {passed_tests}/{total_tests} tests passed")
    print("="*80)
    
    # Save results
    with open("new_api_test_results.json", "w", encoding="utf-8") as f:
        json.dump({
            "domain": domain,
            "keyword": keyword,
            "timestamp": time.strftime('%Y-%m-%d %H:%M:%S'),
            "summary": {
                "total": total_tests,
                "passed": passed_tests,
                "failed": total_tests - passed_tests
            },
            "results": {
                api: {"success": success, "data": str(data)[:1000]}
                for api, (success, data) in results.items()
            }
        }, f, indent=2)
    
    print("\n📄 Results saved to: new_api_test_results.json")
    
    return passed_tests == total_tests

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
