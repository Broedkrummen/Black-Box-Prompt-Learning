"""
Test SEO Analyzer RapidAPI Endpoint
"""

import http.client
import json

RAPIDAPI_KEY = "5c359bb774msh32eed0a33c585c4p1466d6jsn5620b810b2f7"

def test_seo_analyzer(url="https://example.com"):
    """Test SEO Analyzer endpoint"""
    try:
        conn = http.client.HTTPSConnection("seo-analyzer3.p.rapidapi.com")
        
        headers = {
            'x-rapidapi-key': RAPIDAPI_KEY,
            'x-rapidapi-host': "seo-analyzer3.p.rapidapi.com"
        }
        
        endpoint = f"/seo-audit-basic?url={url}"
        
        print(f"\n{'='*80}")
        print(f"Testing SEO Analyzer API")
        print(f"URL to analyze: {url}")
        print(f"Endpoint: https://seo-analyzer3.p.rapidapi.com{endpoint}")
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
            return {"success": False, "error": data}
            
    except Exception as e:
        print(f"Error: {e}")
        return {"success": False, "error": str(e)}

def main():
    print("="*80)
    print("TESTING SEO ANALYZER RAPIDAPI")
    print("="*80)
    
    # Test with example URL
    test_url = "https://example.com"
    
    result = test_seo_analyzer(test_url)
    
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    
    if result['success']:
        print("✅ PASS - SEO Analyzer API")
        print("\nAnalysis Results:")
        data = result['data']
        
        # Display key metrics
        if isinstance(data, dict):
            for key, value in list(data.items())[:10]:
                if isinstance(value, (str, int, float, bool)):
                    print(f"  {key}: {value}")
                elif isinstance(value, dict):
                    print(f"  {key}: {len(value)} items")
                elif isinstance(value, list):
                    print(f"  {key}: {len(value)} items")
    else:
        print("❌ FAIL - SEO Analyzer API")
        print(f"Error: {result.get('error', 'Unknown')}")
    
    # Save results
    with open("seo_analyzer_results.json", "w", encoding="utf-8") as f:
        json.dump({
            "url": test_url,
            "endpoint": "seo-analyzer",
            "result": {
                "success": result['success'],
                "data": str(result.get('data', ''))[:2000]
            }
        }, f, indent=2)
    
    print("\nResults saved to: seo_analyzer_results.json")

if __name__ == "__main__":
    main()
