"""
Test Web Scraping API RapidAPI Endpoint
"""

import http.client
import json

RAPIDAPI_KEY = "5c359bb774msh32eed0a33c585c4p1466d6jsn5620b810b2f7"

def test_web_scraping_api(url="https://example.com"):
    """Test Web Scraping API endpoint"""
    try:
        conn = http.client.HTTPSConnection("web-scraping-api1.p.rapidapi.com")
        
        payload = json.dumps({
            "url": url
        })
        
        headers = {
            'x-rapidapi-key': RAPIDAPI_KEY,
            'x-rapidapi-host': "web-scraping-api1.p.rapidapi.com",
            'Content-Type': "application/json"
        }
        
        print(f"\n{'='*80}")
        print(f"Testing Web Scraping API")
        print(f"URL to scrape: {url}")
        print(f"Endpoint: https://web-scraping-api1.p.rapidapi.com/api/web-scraper")
        print(f"{'='*80}")
        
        conn.request("POST", "/api/web-scraper", payload, headers)
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
    print("TESTING WEB SCRAPING API RAPIDAPI")
    print("="*80)
    
    # Test with example URL
    test_url = "https://example.com"
    
    result = test_web_scraping_api(test_url)
    
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    
    if result['success']:
        print("✅ PASS - Web Scraping API")
        print(f"\nScraping Result:")
        print(f"  URL: {test_url}")
        
        data = result['data']
        if isinstance(data, dict):
            print(f"  Response keys: {list(data.keys())[:10]}")
            if 'html' in data:
                print(f"  HTML length: {len(str(data['html']))} characters")
            if 'text' in data:
                print(f"  Text length: {len(str(data['text']))} characters")
            if 'title' in data:
                print(f"  Page title: {data['title']}")
        else:
            print(f"  Response length: {len(str(data))} characters")
    else:
        print("❌ FAIL - Web Scraping API")
        print(f"Error: {result.get('error', 'Unknown')}")
    
    # Save results
    with open("web_scraping_api_results.json", "w", encoding="utf-8") as f:
        json.dump({
            "url": test_url,
            "endpoint": "web-scraping-api",
            "result": {
                "success": result['success'],
                "data": str(result.get('data', ''))[:2000]
            }
        }, f, indent=2)
    
    print("\nResults saved to: web_scraping_api_results.json")

if __name__ == "__main__":
    main()
