"""
Test Google Rank Checker RapidAPI Endpoint
"""

import http.client

RAPIDAPI_KEY = "5c359bb774msh32eed0a33c585c4p1466d6jsn5620b810b2f7"

def test_google_rank_checker(keyword="wordpress", url="https://wordpress.com/", country="us"):
    """Test Google Rank Checker endpoint"""
    try:
        conn = http.client.HTTPSConnection("google-rank-checker-by-keyword.p.rapidapi.com")
        
        payload = "text example!"
        
        headers = {
            'x-rapidapi-key': RAPIDAPI_KEY,
            'x-rapidapi-host': "google-rank-checker-by-keyword.p.rapidapi.com",
            'Content-Type': "text/plain"
        }
        
        endpoint = f"/id?keyword={keyword}&url={url}&country={country}&id=google-serp"
        
        print(f"\n{'='*80}")
        print(f"Testing Google Rank Checker API")
        print(f"Keyword: {keyword}")
        print(f"URL: {url}")
        print(f"Country: {country}")
        print(f"Endpoint: https://google-rank-checker-by-keyword.p.rapidapi.com{endpoint}")
        print(f"{'='*80}")
        
        conn.request("POST", endpoint, payload, headers)
        res = conn.getresponse()
        data = res.read().decode("utf-8")
        
        print(f"Status: {res.status}")
        print(f"Response: {data[:500]}...")
        
        if res.status == 200:
            return {"success": True, "data": data}
        else:
            return {"success": False, "error": data}
            
    except Exception as e:
        print(f"Error: {e}")
        return {"success": False, "error": str(e)}

def main():
    print("="*80)
    print("TESTING GOOGLE RANK CHECKER RAPIDAPI")
    print("="*80)
    
    # Test with example
    test_keyword = "wordpress"
    test_url = "https://wordpress.com/"
    test_country = "us"
    
    result = test_google_rank_checker(test_keyword, test_url, test_country)
    
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    
    if result['success']:
        print("✅ PASS - Google Rank Checker API")
        print(f"\nRank Check Result:")
        print(f"  Keyword: {test_keyword}")
        print(f"  URL: {test_url}")
        print(f"  Country: {test_country}")
        print(f"  Response: {result['data'][:200]}...")
    else:
        print("❌ FAIL - Google Rank Checker API")
        print(f"Error: {result.get('error', 'Unknown')}")
    
    # Save results
    with open("google_rank_checker_results.txt", "w", encoding="utf-8") as f:
        f.write(f"Keyword: {test_keyword}\n")
        f.write(f"URL: {test_url}\n")
        f.write(f"Country: {test_country}\n")
        f.write(f"Success: {result['success']}\n")
        f.write(f"Response: {result.get('data', result.get('error', ''))}\n")
    
    print("\nResults saved to: google_rank_checker_results.txt")

if __name__ == "__main__":
    main()
