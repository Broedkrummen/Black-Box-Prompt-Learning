"""
Test Google Trends RapidAPI Endpoint
"""

import http.client
import json

RAPIDAPI_KEY = "5c359bb774msh32eed0a33c585c4p1466d6jsn5620b810b2f7"

def test_google_trends(keyword="digitalmarketing"):
    """Test Google Trends endpoint"""
    try:
        conn = http.client.HTTPSConnection("google-trends9.p.rapidapi.com")
        
        headers = {
            'x-rapidapi-key': RAPIDAPI_KEY,
            'x-rapidapi-host': "google-trends9.p.rapidapi.com"
        }
        
        endpoint = f"/trend/{keyword}"
        
        print(f"\n{'='*80}")
        print(f"Testing Google Trends API")
        print(f"Keyword: {keyword}")
        print(f"Endpoint: https://google-trends9.p.rapidapi.com{endpoint}")
        print(f"{'='*80}")
        
        conn.request("GET", endpoint, headers=headers)
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
            if res.status == 200:
                return {"success": True, "data": data}
            return {"success": False, "error": data}
            
    except Exception as e:
        print(f"Error: {e}")
        return {"success": False, "error": str(e)}

def main():
    print("="*80)
    print("TESTING GOOGLE TRENDS API RAPIDAPI")
    print("="*80)
    
    # Test with example keyword
    test_keyword = "digitalmarketing"
    
    result = test_google_trends(test_keyword)
    
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    
    if result['success']:
        print("✅ PASS - Google Trends API")
        print(f"\nTrend Data for '{test_keyword}':")
        
        data = result['data']
        if isinstance(data, dict):
            for key, value in list(data.items())[:10]:
                if isinstance(value, (list, dict)):
                    print(f"  {key}: {type(value).__name__} with {len(value)} items")
                else:
                    print(f"  {key}: {value}")
        elif isinstance(data, list):
            print(f"  Total data points: {len(data)}")
            if len(data) > 0:
                print(f"  Sample: {data[0]}")
        else:
            print(f"  Response: {str(data)[:200]}")
    else:
        print("❌ FAIL - Google Trends API")
        print(f"Error: {result.get('error', 'Unknown')}")
    
    # Save results
    with open("google_trends_results.json", "w", encoding="utf-8") as f:
        json.dump({
            "keyword": test_keyword,
            "endpoint": "google-trends",
            "result": {
                "success": result['success'],
                "data": str(result.get('data', ''))[:2000]
            }
        }, f, indent=2)
    
    print("\nResults saved to: google_trends_results.json")

if __name__ == "__main__":
    main()
