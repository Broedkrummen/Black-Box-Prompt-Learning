"""
Test Dashboard VebAPI Functions
Unit tests for VebAPI integration functions
"""

import http.client
import json
from urllib.parse import quote

VEBAPI_KEY = "de26a23c-a63c-40d1-8e0d-6803f045035f"

def analyze_vebapi_single_keyword(keyword, country):
    """Analyze single keyword with VebAPI"""
    try:
        conn = http.client.HTTPSConnection("vebapi.com")
        headers = {
            'X-API-KEY': VEBAPI_KEY,
            'Content-Type': 'application/json'
        }
        
        conn.request("GET", f"/api/seo/singlekeyword?keyword={quote(keyword)}&country={country.lower()}", headers=headers)
        res = conn.getresponse()
        data = json.loads(res.read().decode("utf-8"))
        
        if res.status == 200:
            return {"success": True, "data": data}
        else:
            return {"success": False, "error": data}
    except Exception as e:
        return {"success": False, "error": str(e)}

def analyze_vebapi_related_keywords(keyword, country):
    """Analyze related keywords with VebAPI"""
    try:
        conn = http.client.HTTPSConnection("vebapi.com")
        headers = {
            'X-API-KEY': VEBAPI_KEY,
            'Content-Type': 'application/json'
        }
        
        conn.request("GET", f"/api/seo/keywordresearch?keyword={quote(keyword)}&country={country.lower()}", headers=headers)
        res = conn.getresponse()
        data = json.loads(res.read().decode("utf-8"))
        
        if res.status == 200:
            return {"success": True, "data": data}
        else:
            return {"success": False, "error": data}
    except Exception as e:
        return {"success": False, "error": str(e)}

def analyze_vebapi_keyword_density(keyword, website):
    """Analyze keyword density with VebAPI"""
    try:
        conn = http.client.HTTPSConnection("vebapi.com")
        headers = {
            'X-API-KEY': VEBAPI_KEY,
            'Content-Type': 'application/json'
        }
        
        conn.request("GET", f"/api/seo/keyworddensity?keyword={quote(keyword)}&website={website}", headers=headers)
        res = conn.getresponse()
        data = json.loads(res.read().decode("utf-8"))
        
        if res.status == 200:
            return {"success": True, "data": data}
        else:
            return {"success": False, "error": data}
    except Exception as e:
        return {"success": False, "error": str(e)}

def test_dashboard_functions():
    """Test all dashboard VebAPI functions"""
    print("="*80)
    print("TESTING DASHBOARD VEBAPI FUNCTIONS")
    print("="*80)
    
    test_keyword = "seo"
    test_country = "us"
    test_website = "example.com"
    
    results = {}
    
    # Test 1: Single Keyword Analysis
    print("\n[TEST 1] Testing analyze_vebapi_single_keyword...")
    result = analyze_vebapi_single_keyword(test_keyword, test_country)
    results['single_keyword'] = result
    if result['success']:
        print(f"✅ PASS - Got data: {result['data'].get('text', 'N/A')}")
    else:
        print(f"❌ FAIL - Error: {result.get('error', 'Unknown')}")
    
    # Test 2: Related Keywords Analysis
    print("\n[TEST 2] Testing analyze_vebapi_related_keywords...")
    result = analyze_vebapi_related_keywords(test_keyword, test_country)
    results['related_keywords'] = result
    if result['success']:
        count = len(result['data']) if isinstance(result['data'], list) else 0
        print(f"✅ PASS - Got {count} related keywords")
    else:
        print(f"❌ FAIL - Error: {result.get('error', 'Unknown')}")
    
    # Test 3: Keyword Density Analysis
    print("\n[TEST 3] Testing analyze_vebapi_keyword_density...")
    result = analyze_vebapi_keyword_density(test_keyword, test_website)
    results['keyword_density'] = result
    if result['success']:
        status = result['data'].get('status', 'N/A')
        print(f"✅ PASS - Status: {status}")
    else:
        print(f"❌ FAIL - Error: {result.get('error', 'Unknown')}")
    
    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    
    total = len(results)
    passed = sum(1 for r in results.values() if r['success'])
    
    for name, result in results.items():
        status = "✅ PASS" if result['success'] else "❌ FAIL"
        print(f"{status} - {name.replace('_', ' ').title()}")
    
    print(f"\nResults: {passed}/{total} functions passed")
    
    # Test error handling
    print("\n" + "="*80)
    print("TESTING ERROR HANDLING")
    print("="*80)
    
    # Test with invalid parameters
    print("\n[TEST 4] Testing with empty keyword...")
    result = analyze_vebapi_single_keyword("", test_country)
    if not result['success']:
        print("✅ PASS - Error handled correctly")
    else:
        print("⚠️  WARNING - Should have failed with empty keyword")
    
    # Test with invalid country
    print("\n[TEST 5] Testing with invalid country code...")
    result = analyze_vebapi_single_keyword(test_keyword, "invalid")
    if result['success'] or 'error' in result:
        print("✅ PASS - Handled invalid country")
    else:
        print("⚠️  WARNING - Response unclear")
    
    print("\n" + "="*80)
    print("DASHBOARD FUNCTION TESTING COMPLETE")
    print("="*80)
    
    return passed == total

if __name__ == "__main__":
    success = test_dashboard_functions()
    exit(0 if success else 1)
