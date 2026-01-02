"""
Quick test script to verify dashboard functionality
Tests with example.com to conserve API credits
"""

import http.client
import json
import time
import hashlib
import hmac
import base64
from urllib.parse import quote

# API Configuration
RAPIDAPI_KEY = "5c359bb774msh32eed0a33c585c4p1466d6jsn5620b810b2f7"
MOZ_ACCESS_ID = "mozscape-c7fe158e8e"
MOZ_SECRET_KEY = "e0c2a5e8e0e44f5e8c7fe158e8e0c2a5"

def test_moz(domain):
    """Test Moz API"""
    print(f"\n🔍 Testing Moz API with {domain}...")
    try:
        expires = int(time.time()) + 300
        string_to_sign = f"{MOZ_ACCESS_ID}\n{expires}"
        binary_signature = hmac.new(
            MOZ_SECRET_KEY.encode('utf-8'),
            string_to_sign.encode('utf-8'),
            hashlib.sha1
        ).digest()
        signature = base64.b64encode(binary_signature).decode('utf-8')
        
        conn = http.client.HTTPSConnection("lsapi.seomoz.com")
        url = f"/v2/url_metrics/{quote(domain, safe='')}?AccessID={MOZ_ACCESS_ID}&Expires={expires}&Signature={quote(signature)}"
        
        conn.request("GET", url)
        res = conn.getresponse()
        data = json.loads(res.read().decode("utf-8"))
        
        if "domain_authority" in data:
            print(f"✅ Moz API: DA = {data.get('domain_authority', 'N/A')}")
            return True
        else:
            print(f"❌ Moz API Error: {data}")
            return False
    except Exception as e:
        print(f"❌ Moz API Exception: {str(e)}")
        return False

def test_ahrefs(domain):
    """Test Ahrefs API"""
    print(f"\n🔍 Testing Ahrefs API with {domain}...")
    try:
        conn = http.client.HTTPSConnection("ahrefs-domain-research.p.rapidapi.com")
        headers = {
            'x-rapidapi-key': RAPIDAPI_KEY,
            'x-rapidapi-host': "ahrefs-domain-research.p.rapidapi.com"
        }
        
        conn.request("GET", f"/domain-rating/?domain={domain}", headers=headers)
        res = conn.getresponse()
        data = json.loads(res.read().decode("utf-8"))
        
        if "domainRating" in data:
            print(f"✅ Ahrefs API: DR = {data.get('domainRating', 'N/A')}")
            return True
        else:
            print(f"❌ Ahrefs API Error: {data}")
            return False
    except Exception as e:
        print(f"❌ Ahrefs API Exception: {str(e)}")
        return False

def test_similarweb(domain):
    """Test SimilarWeb API"""
    print(f"\n🔍 Testing SimilarWeb API with {domain}...")
    try:
        conn = http.client.HTTPSConnection("similarweb-insights.p.rapidapi.com")
        headers = {
            'x-rapidapi-key': RAPIDAPI_KEY,
            'x-rapidapi-host': "similarweb-insights.p.rapidapi.com"
        }
        
        conn.request("GET", f"/traffic/?domain={domain}", headers=headers)
        res = conn.getresponse()
        data = json.loads(res.read().decode("utf-8"))
        
        if "visits" in data:
            visits = list(data['visits'].values())[-1] if data['visits'] else 0
            print(f"✅ SimilarWeb API: Visits = {visits:,}")
            return True
        else:
            print(f"❌ SimilarWeb API Error: {data}")
            return False
    except Exception as e:
        print(f"❌ SimilarWeb API Exception: {str(e)}")
        return False

def main():
    print("=" * 60)
    print("🧪 TESTING SEO DASHBOARD APIs")
    print("=" * 60)
    print("\nTesting with example.com to conserve API credits...")
    
    domain = "example.com"
    results = {
        'moz': False,
        'ahrefs': False,
        'similarweb': False
    }
    
    # Test each API
    results['moz'] = test_moz(domain)
    time.sleep(1)
    
    results['ahrefs'] = test_ahrefs(domain)
    time.sleep(1)
    
    results['similarweb'] = test_similarweb(domain)
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(results.values())
    total = len(results)
    
    for api, status in results.items():
        status_icon = "✅" if status else "❌"
        print(f"{status_icon} {api.upper()}: {'PASSED' if status else 'FAILED'}")
    
    print(f"\n🎯 Result: {passed}/{total} APIs working")
    
    if passed == total:
        print("\n✅ ALL APIS WORKING! Dashboards are ready to use!")
    elif passed > 0:
        print(f"\n⚠️ {total - passed} API(s) failed. Dashboards will work with partial data.")
    else:
        print("\n❌ All APIs failed. Please check API keys and network connection.")
    
    print("\n" + "=" * 60)
    print("📝 NEXT STEPS:")
    print("=" * 60)
    print("1. Streamlit is running at: http://localhost:8501")
    print("2. Open the URL in your browser")
    print("3. Enter 'example.com' to test")
    print("4. Click 'Analyze' and view results")
    print("\nOr test other dashboards:")
    print("- Dash: python seo_dashboard_dash.py (port 8050)")
    print("- Flask: python seo_dashboard_flask.py (port 5000)")
    print("- Tkinter: python seo_dashboard_tkinter.py (desktop)")

if __name__ == "__main__":
    main()
