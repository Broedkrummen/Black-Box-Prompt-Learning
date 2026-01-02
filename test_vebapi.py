"""
Test VebAPI Integration
API Key: de26a23c-a63c-40d1-8e0d-6803f045035f
"""

import http.client
import json
from urllib.parse import quote

VEBAPI_KEY = "de26a23c-a63c-40d1-8e0d-6803f045035f"

def test_vebapi_endpoint(endpoint, params):
    """Test a VebAPI endpoint"""
    try:
        conn = http.client.HTTPSConnection("vebapi.com")
        
        # Build query string from params
        query_params = []
        for key, value in params.items():
            query_params.append(f"{key}={quote(str(value))}")
        
        url = f"{endpoint}?{'&'.join(query_params)}"
        
        # Set headers with API key
        headers = {
            'X-API-KEY': VEBAPI_KEY,
            'Content-Type': 'application/json'
        }
        
        print(f"\n{'='*80}")
        print(f"Testing: {endpoint}")
        print(f"URL: https://vebapi.com{url}")
        print(f"{'='*80}")
        
        conn.request("GET", url, headers=headers)
        res = conn.getresponse()
        data = res.read().decode("utf-8")
        
        print(f"Status: {res.status}")
        print(f"Response: {data[:500]}...")
        
        try:
            json_data = json.loads(data)
            if res.status == 200:
                return True, json_data
            else:
                return False, json_data
        except:
            return False, data
            
    except Exception as e:
        print(f"Error: {e}")
        return False, str(e)

def main():
    domain = "simplybeyond.dk"
    keyword = "hudpleje"
    
    print("="*80)
    print("TESTING VEBAPI ENDPOINTS")
    print("="*80)
    
    results = {}
    
    # Test Keyword Research endpoints
    print("\n" + "="*80)
    print("KEYWORD RESEARCH ENDPOINTS")
    print("="*80)
    
    results['related_keywords'] = test_vebapi_endpoint(
        "/seo/keywordresearch",
        {"keyword": keyword, "country": "dk"}
    )
    
    results['single_keyword'] = test_vebapi_endpoint(
        "/seo/singlekeyword",
        {"keyword": keyword, "country": "dk"}
    )
    
    # Test SEO Analysis endpoints
    print("\n" + "="*80)
    print("SEO ANALYSIS ENDPOINTS")
    print("="*80)

    results['loading_speed'] = test_vebapi_endpoint(
        "/api/seo/loadingspeeddata",
        {"website": domain}
    )

    # Test Backlink endpoints
    print("\n" + "="*80)
    print("BACKLINK ENDPOINTS")
    print("="*80)

    results['backlink_data'] = test_vebapi_endpoint(
        "/api/seo/backlinkdata",
        {"website": domain}
    )

    results['poor_backlinks'] = test_vebapi_endpoint(
        "/api/seo/poorbacklinks",
        {"website": domain}
    )

    results['referral_domains'] = test_vebapi_endpoint(
        "/api/seo/referraldomains",
        {"website": domain}
    )

    # Test Additional endpoints
    print("\n" + "="*80)
    print("ADDITIONAL ENDPOINTS")
    print("="*80)

    results['top_keywords'] = test_vebapi_endpoint(
        "/api/seo/topsearchkeywords",
        {"website": domain}
    )

    results['ai_seo_crawler'] = test_vebapi_endpoint(
        "/api/seo/aiseochecker",
        {"website": domain}
    )
    
    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    
    total = len(results)
    passed = sum(1 for success, _ in results.values() if success)
    
    for name, (success, data) in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {name.replace('_', ' ').title()}")
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    # Save results
    with open("vebapi_test_results.json", "w", encoding="utf-8") as f:
        json.dump({
            "domain": domain,
            "keyword": keyword,
            "total": total,
            "passed": passed,
            "results": {
                name: {"success": success, "data": str(data)[:500]}
                for name, (success, data) in results.items()
            }
        }, f, indent=2)
    
    print("\nResults saved to: vebapi_test_results.json")

if __name__ == "__main__":
    main()
