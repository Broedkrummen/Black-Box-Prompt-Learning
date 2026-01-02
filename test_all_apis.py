"""
Comprehensive API Testing Script
Tests all API endpoints used in the SEO Dashboard
"""

import http.client
import json
import time
import hashlib
import hmac
import base64
from urllib.parse import quote

# API Configuration
RAPIDAPI_KEY = "5c359bb774msh32eed0a33c585c4p1466d6jsn5620b810b2f7"
MOZ_ACCESS_ID = "mozscape-c7fe158e8e"
MOZ_SECRET_KEY = "e0c2a5e8e0e44f5e8c7fe158e8e0c2a5"

def test_moz_api(domain):
    """Test Moz API"""
    print("\n" + "="*80)
    print("🧪 TESTING MOZ API")
    print("="*80)
    
    try:
        expires = int(time.time()) + 300
        string_to_sign = f"{MOZ_ACCESS_ID}\n{expires}"
        binary_signature = hmac.new(
            MOZ_SECRET_KEY.encode('utf-8'),
            string_to_sign.encode('utf-8'),
            hashlib.sha1
        ).digest()
        signature = base64.b64encode(binary_signature).decode('utf-8')
        
        conn = http.client.HTTPSConnection("lsapi.seomoz.com")
        url = f"/v2/url_metrics/{quote(domain, safe='')}?AccessID={MOZ_ACCESS_ID}&Expires={expires}&Signature={quote(signature)}"
        
        print(f"📡 Requesting: {url}")
        conn.request("GET", url)
        res = conn.getresponse()
        data = json.loads(res.read().decode("utf-8"))
        
        print(f"📊 Status Code: {res.status}")
        
        if "domain_authority" in data:
            print("✅ SUCCESS - Moz API working!")
            print(f"   Domain Authority: {data.get('domain_authority', 'N/A')}")
            print(f"   Page Authority: {data.get('page_authority', 'N/A')}")
            return True, data
        else:
            print("❌ FAILED - No domain_authority in response")
            print(f"   Response: {json.dumps(data, indent=2)}")
            return False, data
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False, str(e)

def test_ahrefs_api(domain):
    """Test Ahrefs API"""
    print("\n" + "="*80)
    print("🧪 TESTING AHREFS API")
    print("="*80)
    
    try:
        conn = http.client.HTTPSConnection("ahrefs-domain-research.p.rapidapi.com")
        headers = {
            'x-rapidapi-key': RAPIDAPI_KEY,
            'x-rapidapi-host': "ahrefs-domain-research.p.rapidapi.com"
        }
        
        endpoint = f"/domain-rating/?domain={domain}"
        print(f"📡 Requesting: {endpoint}")
        
        conn.request("GET", endpoint, headers=headers)
        res = conn.getresponse()
        data = json.loads(res.read().decode("utf-8"))
        
        print(f"📊 Status Code: {res.status}")
        
        if "domainRating" in data:
            print("✅ SUCCESS - Ahrefs API working!")
            print(f"   Domain Rating: {data.get('domainRating', 'N/A')}")
            return True, data
        else:
            print("❌ FAILED - No domainRating in response")
            print(f"   Response: {json.dumps(data, indent=2)}")
            return False, data
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False, str(e)

def test_similarweb_api(domain):
    """Test SimilarWeb API"""
    print("\n" + "="*80)
    print("🧪 TESTING SIMILARWEB API")
    print("="*80)
    
    try:
        conn = http.client.HTTPSConnection("similarweb-insights.p.rapidapi.com")
        headers = {
            'x-rapidapi-key': RAPIDAPI_KEY,
            'x-rapidapi-host': "similarweb-insights.p.rapidapi.com"
        }
        
        endpoint = f"/traffic/?domain={domain}"
        print(f"📡 Requesting: {endpoint}")
        
        conn.request("GET", endpoint, headers=headers)
        res = conn.getresponse()
        data = json.loads(res.read().decode("utf-8"))
        
        print(f"📊 Status Code: {res.status}")
        
        if "visits" in data:
            print("✅ SUCCESS - SimilarWeb API working!")
            visits = data.get('visits', {})
            if visits:
                latest_month = list(visits.keys())[-1]
                print(f"   Latest Month: {latest_month}")
                print(f"   Visits: {visits[latest_month]:,}")
            return True, data
        else:
            print("❌ FAILED - No visits in response")
            print(f"   Response: {json.dumps(data, indent=2)}")
            return False, data
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False, str(e)

def test_seo_api(domain):
    """Test SEO API (Backlinks)"""
    print("\n" + "="*80)
    print("🧪 TESTING SEO API (BACKLINKS)")
    print("="*80)
    
    try:
        conn = http.client.HTTPSConnection("seo-api-dr-rd-rank-keywords-backlinks1.p.rapidapi.com")
        headers = {
            'x-rapidapi-key': RAPIDAPI_KEY,
            'x-rapidapi-host': "seo-api-dr-rd-rank-keywords-backlinks1.p.rapidapi.com"
        }
        
        # Test backlink-checker endpoint
        encoded_url = quote(domain, safe='')
        endpoint = f"/backlink-checker?mode=subdomains&url={encoded_url}&limit=100"
        print(f"📡 Requesting: {endpoint}")
        
        conn.request("GET", endpoint, headers=headers)
        res = conn.getresponse()
        backlinks_data = json.loads(res.read().decode("utf-8"))
        
        print(f"📊 Status Code: {res.status}")
        print(f"📊 Backlinks Response Type: {type(backlinks_data)}")
        
        # Test basic-metrics endpoint
        conn = http.client.HTTPSConnection("seo-api-dr-rd-rank-keywords-backlinks1.p.rapidapi.com")
        endpoint2 = f"/basic-metrics?url={encoded_url}"
        print(f"📡 Requesting: {endpoint2}")
        
        conn.request("GET", endpoint2, headers=headers)
        res2 = conn.getresponse()
        basic_data = json.loads(res2.read().decode("utf-8"))
        
        print(f"📊 Status Code: {res2.status}")
        
        # Check if we got backlinks
        backlinks = backlinks_data.get("backlinks", []) if isinstance(backlinks_data, dict) else []
        
        if backlinks or basic_data:
            print("✅ SUCCESS - SEO API working!")
            print(f"   Backlinks found: {len(backlinks)}")
            if basic_data:
                print(f"   Basic metrics: {json.dumps(basic_data, indent=2)[:200]}...")
            if backlinks:
                print(f"   First backlink: {json.dumps(backlinks[0], indent=2)[:200]}...")
            return True, {"backlinks": backlinks_data, "basic": basic_data}
        else:
            print("❌ FAILED - No backlinks or basic data")
            print(f"   Backlinks Response: {json.dumps(backlinks_data, indent=2)[:500]}")
            print(f"   Basic Response: {json.dumps(basic_data, indent=2)[:500]}")
            return False, {"backlinks": backlinks_data, "basic": basic_data}
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False, str(e)

def test_google_keywords_api(domain, location="DK", language="da"):
    """Test Google Keywords API"""
    print("\n" + "="*80)
    print("🧪 TESTING GOOGLE KEYWORDS API")
    print("="*80)
    
    try:
        conn = http.client.HTTPSConnection("google-keyword-insight1.p.rapidapi.com")
        headers = {
            'x-rapidapi-key': RAPIDAPI_KEY,
            'x-rapidapi-host': "google-keyword-insight1.p.rapidapi.com"
        }
        
        endpoint = f"/urlkeysuggest/?url={domain}&location={location}&lang={language}"
        print(f"📡 Requesting: {endpoint}")
        
        conn.request("GET", endpoint, headers=headers)
        res = conn.getresponse()
        data = json.loads(res.read().decode("utf-8"))
        
        print(f"📊 Status Code: {res.status}")
        print(f"📊 Response Type: {type(data)}")
        
        if isinstance(data, list) and len(data) > 0:
            print("✅ SUCCESS - Google Keywords API working!")
            print(f"   Keywords found: {len(data)}")
            print(f"   First keyword: {json.dumps(data[0], indent=2)}")
            return True, data
        else:
            print("❌ FAILED - No keywords in response")
            print(f"   Response: {json.dumps(data, indent=2)[:500]}")
            return False, data
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False, str(e)

def main():
    print("="*80)
    print("🧪 COMPREHENSIVE API TESTING")
    print("="*80)
    
    domain = "simplybeyond.dk"
    print(f"\n🎯 Testing domain: {domain}")
    
    results = {}
    
    # Test all APIs
    print("\n" + "="*80)
    print("RUNNING ALL API TESTS")
    print("="*80)
    
    results['moz'] = test_moz_api(domain)
    time.sleep(2)
    
    results['ahrefs'] = test_ahrefs_api(domain)
    time.sleep(2)
    
    results['similarweb'] = test_similarweb_api(domain)
    time.sleep(2)
    
    results['seo_api'] = test_seo_api(domain)
    time.sleep(2)
    
    results['google_keywords'] = test_google_keywords_api(domain)
    
    # Summary
    print("\n" + "="*80)
    print("📊 TEST SUMMARY")
    print("="*80)
    
    total_tests = len(results)
    passed_tests = sum(1 for success, _ in results.values() if success)
    
    for api_name, (success, data) in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {api_name.upper()}")
    
    print("\n" + "="*80)
    print(f"RESULTS: {passed_tests}/{total_tests} tests passed")
    print("="*80)
    
    # Save detailed results
    with open("api_test_results.json", "w", encoding="utf-8") as f:
        json.dump({
            "domain": domain,
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
    
    print("\n📄 Detailed results saved to: api_test_results.json")
    
    return passed_tests == total_tests

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
