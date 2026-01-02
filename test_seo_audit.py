"""
Test SEO Audit RapidAPI Endpoint
"""

import http.client
import json

RAPIDAPI_KEY = "5c359bb774msh32eed0a33c585c4p1466d6jsn5620b810b2f7"

def test_seo_audit(url="https://backlinko.com", results=None):
    """Test SEO Audit endpoint"""
    if results is None:
        results = ["metadata", "links", "images", "content"]
    
    try:
        conn = http.client.HTTPSConnection("seo-audit1.p.rapidapi.com")
        
        payload = json.dumps({
            "url": url,
            "results": results
        })
        
        headers = {
            'x-rapidapi-key': RAPIDAPI_KEY,
            'x-rapidapi-host': "seo-audit1.p.rapidapi.com",
            'Content-Type': "application/json"
        }
        
        print(f"\n{'='*80}")
        print(f"Testing SEO Audit API")
        print(f"URL to audit: {url}")
        print(f"Results requested: {', '.join(results)}")
        print(f"Endpoint: https://seo-audit1.p.rapidapi.com/audit")
        print(f"{'='*80}")
        
        conn.request("POST", "/audit", payload, headers)
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
    print("TESTING SEO AUDIT RAPIDAPI")
    print("="*80)
    
    # Test with example URL
    test_url = "https://backlinko.com"
    
    result = test_seo_audit(test_url)
    
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    
    if result['success']:
        print("✅ PASS - SEO Audit API")
        print("\nAudit Results:")
        data = result['data']
        
        # Display metadata
        if 'metadata' in data:
            metadata = data['metadata']
            print("\n📄 Metadata:")
            print(f"  Title: {metadata.get('title', 'N/A')[:60]}...")
            print(f"  Description: {metadata.get('description', 'N/A')[:60]}...")
            print(f"  Keywords: {metadata.get('keywords', 'N/A')[:60]}...")
        
        # Display links summary
        if 'links' in data:
            links = data['links']
            print(f"\n🔗 Links:")
            print(f"  Total: {links.get('total', 0)}")
            print(f"  Internal: {links.get('internal', 0)}")
            print(f"  External: {links.get('external', 0)}")
        
        # Display images summary
        if 'images' in data:
            images = data['images']
            print(f"\n🖼️ Images:")
            print(f"  Total: {images.get('total', 0)}")
            print(f"  With Alt: {images.get('with_alt', 0)}")
            print(f"  Without Alt: {images.get('without_alt', 0)}")
        
        # Display content summary
        if 'content' in data:
            content = data['content']
            print(f"\n📝 Content:")
            print(f"  Word Count: {content.get('word_count', 0)}")
            print(f"  Headings: {content.get('headings', {}).get('total', 0)}")
    else:
        print("❌ FAIL - SEO Audit API")
        print(f"Error: {result.get('error', 'Unknown')}")
    
    # Save results
    with open("seo_audit_results.json", "w", encoding="utf-8") as f:
        json.dump({
            "url": test_url,
            "endpoint": "seo-audit",
            "result": {
                "success": result['success'],
                "data": str(result.get('data', ''))[:2000]
            }
        }, f, indent=2)
    
    print("\nResults saved to: seo_audit_results.json")

if __name__ == "__main__":
    main()
