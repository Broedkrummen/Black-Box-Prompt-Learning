"""
Test SEO Master Scan RapidAPI Endpoint
"""

import http.client
import json

RAPIDAPI_KEY = "5c359bb774msh32eed0a33c585c4p1466d6jsn5620b810b2f7"

def test_seo_master_scan(url="https://example.com", sections=None):
    """Test SEO Master Scan endpoint"""
    if sections is None:
        sections = ["performanceMetrics", "recommendations"]
    
    try:
        conn = http.client.HTTPSConnection("seo-master-scan-website-analysis-performance-reporting.p.rapidapi.com")
        
        payload = json.dumps({
            "url": url,
            "sections": sections
        })
        
        headers = {
            'x-rapidapi-key': RAPIDAPI_KEY,
            'x-rapidapi-host': "seo-master-scan-website-analysis-performance-reporting.p.rapidapi.com",
            'Content-Type': "application/json"
        }
        
        print(f"\n{'='*80}")
        print(f"Testing SEO Master Scan API")
        print(f"URL to scan: {url}")
        print(f"Sections: {', '.join(sections)}")
        print(f"Endpoint: https://seo-master-scan-website-analysis-performance-reporting.p.rapidapi.com/analyze?noqueue=1")
        print(f"{'='*80}")
        
        conn.request("POST", "/analyze?noqueue=1", payload, headers)
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
    print("TESTING SEO MASTER SCAN RAPIDAPI")
    print("="*80)
    
    # Test with example URL
    test_url = "https://example.com"
    
    result = test_seo_master_scan(test_url)
    
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    
    if result['success']:
        print("✅ PASS - SEO Master Scan API")
        print("\nScan Results:")
        data = result['data']
        
        if isinstance(data, dict):
            # Display performance metrics
            if 'performanceMetrics' in data:
                print("\n⚡ Performance Metrics:")
                metrics = data['performanceMetrics']
                for key, value in list(metrics.items())[:5]:
                    print(f"  {key}: {value}")
            
            # Display recommendations
            if 'recommendations' in data:
                print("\n💡 Recommendations:")
                recs = data['recommendations']
                if isinstance(recs, list):
                    for i, rec in enumerate(recs[:3], 1):
                        print(f"  {i}. {rec}")
                elif isinstance(recs, dict):
                    for key, value in list(recs.items())[:3]:
                        print(f"  {key}: {value}")
    else:
        print("❌ FAIL - SEO Master Scan API")
        print(f"Error: {result.get('error', 'Unknown')}")
    
    # Save results
    with open("seo_master_scan_results.json", "w", encoding="utf-8") as f:
        json.dump({
            "url": test_url,
            "endpoint": "seo-master-scan",
            "result": {
                "success": result['success'],
                "data": str(result.get('data', ''))[:2000]
            }
        }, f, indent=2)
    
    print("\nResults saved to: seo_master_scan_results.json")

if __name__ == "__main__":
    main()
