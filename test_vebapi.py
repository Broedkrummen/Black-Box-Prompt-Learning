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

        url = f"/api{endpoint}?{'&'.join(query_params)}"

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
    print("COMPREHENSIVE VEBAPI ENDPOINT TESTING")
    print("="*80)
    
    results = {}
    
    # Test Keyword Research endpoints
    print("\n" + "="*80)
    print("1. KEYWORD RESEARCH ENDPOINTS")
    print("="*80)

    results['keyword_research'] = test_vebapi_endpoint(
        "/seo/keywordresearch",
        {"keyword": keyword, "country": "dk"}
    )

    results['single_keyword'] = test_vebapi_endpoint(
        "/seo/singlekeyword",
        {"keyword": keyword, "country": "dk"}
    )

    results['keyword_density'] = test_vebapi_endpoint(
        "/seo/keyworddensity",
        {"keyword": keyword, "website": domain}
    )
    
    # Test On-Page SEO endpoints
    print("\n" + "="*80)
    print("2. ON-PAGE SEO ENDPOINTS")
    print("="*80)
    
    results['page_analysis'] = test_vebapi_endpoint(
        "/seo/analyze",
        {"website": domain}
    )
    
    results['ai_search_analyzer'] = test_vebapi_endpoint(
        "/seo/apipagechecker",
        {"website": domain}
    )
    
    results['ai_seo_crawler'] = test_vebapi_endpoint(
        "/seo/aiseochecker",
        {"website": domain}
    )
    
    results['loading_speed'] = test_vebapi_endpoint(
        "/seo/loadingspeeddata",
        {"website": domain}
    )
    
    # Test Domain Intelligence endpoints
    print("\n" + "="*80)
    print("3. DOMAIN INTELLIGENCE ENDPOINTS")
    print("="*80)
    
    results['domain_data'] = test_vebapi_endpoint(
        "/seo/domainnamedata",
        {"website": domain}
    )
    
    # Test Backlink Analysis endpoints
    print("\n" + "="*80)
    print("4. BACKLINK ANALYSIS ENDPOINTS")
    print("="*80)
    
    results['backlink_data'] = test_vebapi_endpoint(
        "/seo/backlinkdata",
        {"website": domain}
    )
    
    results['new_backlinks'] = test_vebapi_endpoint(
        "/seo/newbacklinks",
        {"website": domain}
    )
    
    results['poor_backlinks'] = test_vebapi_endpoint(
        "/seo/poorbacklinks",
        {"website": domain}
    )
    
    results['referral_domains'] = test_vebapi_endpoint(
        "/seo/referraldomains",
        {"website": domain}
    )
    
    results['top_keywords'] = test_vebapi_endpoint(
        "/seo/topsearchkeywords",
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
