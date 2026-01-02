"""
Test RapidAPI SEO Tools - Historical Website Traffic
"""

import http.client
import json

RAPIDAPI_KEY = "5c359bb774msh32eed0a33c585c4p1466d6jsn5620b810b2f7"

def test_historical_traffic(domain, location="2840", language="en"):
    """Test Historical Website Traffic endpoint"""
    try:
        conn = http.client.HTTPSConnection("seo-tools-historical-website-traffic.p.rapidapi.com")
        
        headers = {
            'x-rapidapi-key': RAPIDAPI_KEY,
            'x-rapidapi-host': "seo-tools-historical-website-traffic.p.rapidapi.com"
        }
        
        url = f"/?domain={domain}&location={location}&language={language}"
        
        print(f"\n{'='*80}")
        print(f"Testing Historical Website Traffic")
        print(f"Domain: {domain}")
        print(f"URL: https://seo-tools-historical-website-traffic.p.rapidapi.com{url}")
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
    print("TESTING RAPIDAPI SEO TOOLS - HISTORICAL WEBSITE TRAFFIC")
    print("="*80)
    
    # Test with example domain
    domain = "awario.com"
    
    result = test_historical_traffic(domain)
    
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    
    if result['success']:
        print("✅ PASS - Historical Website Traffic")
        print("\nSample Data:")
        if isinstance(result['data'], dict):
            for key, value in list(result['data'].items())[:5]:
                print(f"  {key}: {value}")
    else:
        print("❌ FAIL - Historical Website Traffic")
        print(f"Error: {result.get('error', 'Unknown')}")
    
    # Save results
    with open("rapidapi_seo_tools_results.json", "w", encoding="utf-8") as f:
        json.dump({
            "domain": domain,
            "endpoint": "historical-website-traffic",
            "result": {
                "success": result['success'],
                "data": str(result.get('data', ''))[:1000]
            }
        }, f, indent=2)
    
    print("\nResults saved to: rapidapi_seo_tools_results.json")

if __name__ == "__main__":
    main()
