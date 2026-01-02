"""
Test SEO Keywords Research RapidAPI Endpoint
"""

import http.client
import json

RAPIDAPI_KEY = "5c359bb774msh32eed0a33c585c4p1466d6jsn5620b810b2f7"

def test_seo_keywords_research(keyword="android diet planner app", country="AU"):
    """Test SEO Keywords Research endpoint"""
    try:
        conn = http.client.HTTPSConnection("seo-keywords-research-api.p.rapidapi.com")
        
        payload = json.dumps({
            "keyword": keyword,
            "country": country
        })
        
        headers = {
            'x-rapidapi-key': RAPIDAPI_KEY,
            'x-rapidapi-host': "seo-keywords-research-api.p.rapidapi.com",
            'Content-Type': "application/json"
        }
        
        print(f"\n{'='*80}")
        print(f"Testing SEO Keywords Research API")
        print(f"Keyword: {keyword}")
        print(f"Country: {country}")
        print(f"Endpoint: https://seo-keywords-research-api.p.rapidapi.com/keywordextraction.php")
        print(f"{'='*80}")
        
        conn.request("POST", "/keywordextraction.php", payload, headers)
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
    print("TESTING SEO KEYWORDS RESEARCH RAPIDAPI")
    print("="*80)
    
    # Test with example keyword
    test_keyword = "android diet planner app"
    test_country = "AU"
    
    result = test_seo_keywords_research(test_keyword, test_country)
    
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    
    if result['success']:
        print("✅ PASS - SEO Keywords Research API")
        print("\nKeyword Research Results:")
        data = result['data']
        
        if isinstance(data, list):
            print(f"Total keywords found: {len(data)}")
            for i, item in enumerate(data[:5], 1):
                if isinstance(item, dict):
                    kw = item.get('keyword', item.get('text', 'N/A'))
                    vol = item.get('volume', item.get('search_volume', 'N/A'))
                    print(f"  {i}. {kw}: Volume={vol}")
                else:
                    print(f"  {i}. {item}")
        elif isinstance(data, dict):
            for key, value in list(data.items())[:5]:
                print(f"  {key}: {value}")
    else:
        print("❌ FAIL - SEO Keywords Research API")
        print(f"Error: {result.get('error', 'Unknown')}")
    
    # Save results
    with open("seo_keywords_research_results.json", "w", encoding="utf-8") as f:
        json.dump({
            "keyword": test_keyword,
            "country": test_country,
            "endpoint": "seo-keywords-research",
            "result": {
                "success": result['success'],
                "data": str(result.get('data', ''))[:2000]
            }
        }, f, indent=2)
    
    print("\nResults saved to: seo_keywords_research_results.json")

if __name__ == "__main__":
    main()
