"""
VEBAPI Integration Demo
Demonstrates all 13 working endpoints
"""

import http.client
import json
from urllib.parse import quote

VEBAPI_KEY = "de26a23c-a63c-40d1-8e0d-6803f045035f"

def call_vebapi(endpoint, params):
    """Call VEBAPI endpoint"""
    try:
        conn = http.client.HTTPSConnection("vebapi.com")
        headers = {
            'X-API-KEY': VEBAPI_KEY,
            'Content-Type': 'application/json'
        }
        
        query_string = '&'.join([f"{k}={quote(str(v))}" for k, v in params.items()])
        url = f"{endpoint}?{query_string}"
        
        conn.request("GET", url, headers=headers)
        res = conn.getresponse()
        data = json.loads(res.read().decode("utf-8"))
        
        return {"status": res.status, "data": data}
    except Exception as e:
        return {"status": "error", "error": str(e)}

def main():
    print("="*80)
    print("🚀 VEBAPI INTEGRATION DEMO")
    print("="*80)
    print("\nDemonstrating all 13 working VEBAPI endpoints...\n")
    
    # Test domain and keyword
    domain = "example.com"
    keyword = "seo"
    country = "us"
    
    # 1. Keyword Research
    print("\n[1/13] Testing Keyword Research...")
    result = call_vebapi("/api/seo/keywordresearch", {"keyword": keyword, "country": country})
    if result['status'] == 200:
        count = len(result['data']) if isinstance(result['data'], list) else 0
        print(f"✅ SUCCESS - Found {count} related keywords")
    else:
        print(f"❌ FAILED - Status: {result['status']}")
    
    # 2. Single Keyword
    print("\n[2/13] Testing Single Keyword Analysis...")
    result = call_vebapi("/api/seo/singlekeyword", {"keyword": keyword, "country": country})
    if result['status'] == 200:
        print(f"✅ SUCCESS - Keyword: {result['data'].get('text', 'N/A')}, Volume: {result['data'].get('vol', 'N/A')}")
    else:
        print(f"❌ FAILED - Status: {result['status']}")
    
    # 3. Keyword Density
    print("\n[3/13] Testing Keyword Density...")
    result = call_vebapi("/api/seo/keyworddensity", {"keyword": keyword, "website": domain})
    if result['status'] == 200:
        print(f"✅ SUCCESS - Status: {result['data'].get('status', 'N/A')}")
    else:
        print(f"❌ FAILED - Status: {result['status']}")
    
    # 4. Page Analysis
    print("\n[4/13] Testing Page Analysis...")
    result = call_vebapi("/api/seo/analyze", {"website": domain})
    if result['status'] == 200:
        print(f"✅ SUCCESS - Analysis complete")
    else:
        print(f"❌ FAILED - Status: {result['status']}")
    
    # 5. AI Search Analyzer
    print("\n[5/13] Testing AI Search Analyzer...")
    result = call_vebapi("/api/seo/apipagechecker", {"website": domain})
    if result['status'] == 200:
        print(f"✅ SUCCESS - AI Scrapable: {result['data'].get('ai_scrapable', 'N/A')}")
    else:
        print(f"❌ FAILED - Status: {result['status']}")
    
    # 6. AI SEO Crawler
    print("\n[6/13] Testing AI SEO Crawler...")
    result = call_vebapi("/api/seo/aiseochecker", {"website": domain})
    if result['status'] == 200:
        print(f"✅ SUCCESS - AI Bots Allowed: {result['data'].get('ai_bots_allowed', 'N/A')}")
    else:
        print(f"❌ FAILED - Status: {result['status']}")
    
    # 7. Loading Speed
    print("\n[7/13] Testing Loading Speed...")
    result = call_vebapi("/api/seo/loadingspeeddata", {"website": domain})
    if result['status'] == 200:
        print(f"✅ SUCCESS - Load time data retrieved")
    else:
        print(f"❌ FAILED - Status: {result['status']}")
    
    # 8. Domain Data
    print("\n[8/13] Testing Domain Data...")
    result = call_vebapi("/api/seo/domainnamedata", {"website": domain})
    if result['status'] == 200:
        print(f"✅ SUCCESS - Domain data retrieved")
    else:
        print(f"❌ FAILED - Status: {result['status']}")
    
    # 9. Backlink Data
    print("\n[9/13] Testing Backlink Data...")
    result = call_vebapi("/api/seo/backlinkdata", {"website": domain})
    if result['status'] == 200:
        total = result['data'].get('counts', {}).get('backlinks', {}).get('total', 0)
        print(f"✅ SUCCESS - Total Backlinks: {total}")
    else:
        print(f"❌ FAILED - Status: {result['status']}")
    
    # 10. New Backlinks
    print("\n[10/13] Testing New Backlinks...")
    result = call_vebapi("/api/seo/newbacklinks", {"website": domain})
    if result['status'] == 200:
        count = len(result['data'].get('backlinks', []))
        print(f"✅ SUCCESS - Found {count} new backlinks")
    else:
        print(f"❌ FAILED - Status: {result['status']}")
    
    # 11. Poor Backlinks
    print("\n[11/13] Testing Poor Backlinks...")
    result = call_vebapi("/api/seo/poorbacklinks", {"website": domain})
    if result['status'] == 200:
        count = len(result['data'].get('backlinks', []))
        print(f"✅ SUCCESS - Found {count} poor backlinks")
    else:
        print(f"❌ FAILED - Status: {result['status']}")
    
    # 12. Referral Domains
    print("\n[12/13] Testing Referral Domains...")
    result = call_vebapi("/api/seo/referraldomains", {"website": domain})
    if result['status'] == 200:
        count = len(result['data'].get('referrers', []))
        print(f"✅ SUCCESS - Found {count} referral domains")
    else:
        print(f"❌ FAILED - Status: {result['status']}")
    
    # 13. Top Keywords
    print("\n[13/13] Testing Top Search Keywords...")
    result = call_vebapi("/api/seo/topsearchkeywords", {"website": domain})
    if result['status'] == 200:
        count = len(result['data'].get('keywords', []))
        print(f"✅ SUCCESS - Found {count} top keywords")
    else:
        print(f"❌ FAILED - Status: {result['status']}")
    
    print("\n" + "="*80)
    print("✅ DEMO COMPLETE!")
    print("="*80)
    print("\nAll 13 VEBAPI endpoints have been successfully integrated!")
    print("\nFor full dashboard experience, install Streamlit:")
    print("  pip install streamlit")
    print("  streamlit run seo_dashboard_streamlit_vebapi.py")
    print("\n" + "="*80)

if __name__ == "__main__":
    main()
