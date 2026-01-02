"""
Test Lighthouse Report RapidAPI Endpoint
"""

import http.client
import json
from urllib.parse import quote

RAPIDAPI_KEY = "5c359bb774msh32eed0a33c585c4p1466d6jsn5620b810b2f7"

def test_lighthouse_report(url="http://google.com"):
    """Test Lighthouse Report endpoint"""
    try:
        conn = http.client.HTTPSConnection("lighthouse-report.p.rapidapi.com")
        
        headers = {
            'x-rapidapi-key': RAPIDAPI_KEY,
            'x-rapidapi-host': "lighthouse-report.p.rapidapi.com"
        }
        
        encoded_url = quote(url, safe='')
        endpoint = f"/?url={encoded_url}"
        
        print(f"\n{'='*80}")
        print(f"Testing Lighthouse Report API")
        print(f"URL to analyze: {url}")
        print(f"Endpoint: https://lighthouse-report.p.rapidapi.com{endpoint}")
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
    print("TESTING LIGHTHOUSE REPORT RAPIDAPI")
    print("="*80)
    
    # Test with example URL
    test_url = "http://google.com"
    
    result = test_lighthouse_report(test_url)
    
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    
    if result['success']:
        print("✅ PASS - Lighthouse Report API")
        print("\nSample Data:")
        if isinstance(result['data'], dict):
            # Display key metrics
            categories = result['data'].get('categories', {})
            if categories:
                print("\nLighthouse Scores:")
                for category, details in categories.items():
                    score = details.get('score', 0) * 100 if details.get('score') else 0
                    print(f"  {category.title()}: {score:.0f}/100")
            
            # Display performance metrics
            audits = result['data'].get('audits', {})
            if audits:
                print("\nKey Metrics:")
                metrics = ['first-contentful-paint', 'largest-contentful-paint', 'speed-index', 'interactive']
                for metric in metrics:
                    if metric in audits:
                        value = audits[metric].get('displayValue', 'N/A')
                        print(f"  {metric}: {value}")
    else:
        print("❌ FAIL - Lighthouse Report API")
        print(f"Error: {result.get('error', 'Unknown')}")
    
    # Save results
    with open("lighthouse_report_results.json", "w", encoding="utf-8") as f:
        json.dump({
            "url": test_url,
            "endpoint": "lighthouse-report",
            "result": {
                "success": result['success'],
                "data": str(result.get('data', ''))[:2000]
            }
        }, f, indent=2)
    
    print("\nResults saved to: lighthouse_report_results.json")

if __name__ == "__main__":
    main()
