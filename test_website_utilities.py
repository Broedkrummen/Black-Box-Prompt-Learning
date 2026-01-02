"""
Test Website Utilities RapidAPI Endpoint
"""

import http.client
import json

RAPIDAPI_KEY = "5c359bb774msh32eed0a33c585c4p1466d6jsn5620b810b2f7"

def test_website_ping(url="https://example.com", port="443"):
    """Test Website Utilities ping endpoint"""
    try:
        conn = http.client.HTTPSConnection("website-utilities.p.rapidapi.com")
        
        payload = json.dumps({
            "url": url,
            "port": port
        })
        
        headers = {
            'x-rapidapi-key': RAPIDAPI_KEY,
            'x-rapidapi-host': "website-utilities.p.rapidapi.com",
            'Content-Type': "application/json"
        }
        
        endpoint = f"/ping?url={url}"
        
        print(f"\n{'='*80}")
        print(f"Testing Website Utilities API - Ping")
        print(f"URL: {url}")
        print(f"Port: {port}")
        print(f"Endpoint: https://website-utilities.p.rapidapi.com{endpoint}")
        print(f"{'='*80}")
        
        conn.request("POST", endpoint, payload, headers)
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
    print("TESTING WEBSITE UTILITIES API RAPIDAPI")
    print("="*80)
    
    # Test with example URL
    test_url = "https://example.com"
    test_port = "443"
    
    result = test_website_ping(test_url, test_port)
    
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    
    if result['success']:
        print("✅ PASS - Website Utilities API (Ping)")
        print(f"\nPing Result:")
        print(f"  URL: {test_url}")
        print(f"  Port: {test_port}")
        
        data = result['data']
        if isinstance(data, dict):
            for key, value in list(data.items())[:10]:
                print(f"  {key}: {value}")
        else:
            print(f"  Response: {str(data)[:200]}")
    else:
        print("❌ FAIL - Website Utilities API (Ping)")
        print(f"Error: {result.get('error', 'Unknown')}")
    
    # Save results
    with open("website_utilities_results.json", "w", encoding="utf-8") as f:
        json.dump({
            "url": test_url,
            "port": test_port,
            "endpoint": "website-utilities-ping",
            "result": {
                "success": result['success'],
                "data": str(result.get('data', ''))[:2000]
            }
        }, f, indent=2)
    
    print("\nResults saved to: website_utilities_results.json")

if __name__ == "__main__":
    main()
