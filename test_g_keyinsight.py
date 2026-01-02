"""
Test G-KeyInsight RapidAPI Endpoint
"""

import http.client
import json

RAPIDAPI_KEY = "5c359bb774msh32eed0a33c585c4p1466d6jsn5620b810b2f7"

def test_g_keyinsight(keyword="seo", location="2840", language="en"):
    """Test G-KeyInsight endpoint"""
    try:
        conn = http.client.HTTPSConnection("g-keyinsight.p.rapidapi.com")
        
        headers = {
            'x-rapidapi-key': RAPIDAPI_KEY,
            'x-rapidapi-host': "g-keyinsight.p.rapidapi.com"
        }
        
        url = f"/keysuggest/?keyword={keyword}&location={location}&language={language}"
        
        print(f"\n{'='*80}")
        print(f"Testing G-KeyInsight API")
        print(f"Keyword: {keyword}")
        print(f"URL: https://g-keyinsight.p.rapidapi.com{url}")
        print(f"{'='*80}")
        
        conn.request("GET", url, headers=headers)
        res = conn.getresponse()
        data = res.read().decode("utf-8")
        
        print(f"Status: {res.status}")
        print(f"Response: {data[:500]}...")
        
        try:
            json_data = json.loads(data)
            if res.status == 200:
                return {"success": True, "data": json_data}
            else:
                return {"success": False, "error": json_data}
        except:
            return {"success": False, "error": data}
            
    except Exception as e:
        print(f"Error: {e}")
        return {"success": False, "error": str(e)}

def main():
    print("="*80)
    print("TESTING G-KEYINSIGHT RAPIDAPI")
    print("="*80)
    
    # Test with example keyword
    keyword = "seo"
    
    result = test_g_keyinsight(keyword)
    
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    
    if result['success']:
        print("✅ PASS - G-KeyInsight API")
        print("\nSample Data:")
        if isinstance(result['data'], list):
            print(f"Total keywords found: {len(result['data'])}")
            for item in result['data'][:3]:
                print(f"  - {item.get('text', 'N/A')}: Vol={item.get('volume', 'N/A')}, CPC=${item.get('cpc', 'N/A')}")
        elif isinstance(result['data'], dict):
            for key, value in list(result['data'].items())[:5]:
                print(f"  {key}: {value}")
    else:
        print("❌ FAIL - G-KeyInsight API")
        print(f"Error: {result.get('error', 'Unknown')}")
    
    # Save results
    with open("g_keyinsight_results.json", "w", encoding="utf-8") as f:
        json.dump({
            "keyword": keyword,
            "endpoint": "g-keyinsight",
            "result": {
                "success": result['success'],
                "data": str(result.get('data', ''))[:1000]
            }
        }, f, indent=2)
    
    print("\nResults saved to: g_keyinsight_results.json")

if __name__ == "__main__":
    main()
