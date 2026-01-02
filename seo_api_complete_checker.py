"""
SEO API Complete Checker
Comprehensive SEO tool with DR, RD, Rank, Keywords, and Backlinks
"""

import http.client
import json
import time
from urllib.parse import quote

class SEOAPIChecker:
    def __init__(self, api_key):
        self.api_key = api_key
        self.headers = {
            'x-rapidapi-key': api_key,
            'x-rapidapi-host': 'seo-api-dr-rd-rank-keywords-backlinks1.p.rapidapi.com'
        }
    
    def get_basic_metrics(self, url):
        """Get basic SEO metrics (DR, RD, Rank)"""
        try:
            print(f"\n🔍 Fetching basic metrics for {url}...")
            
            conn = http.client.HTTPSConnection("seo-api-dr-rd-rank-keywords-backlinks1.p.rapidapi.com")
            encoded_url = quote(url, safe='')
            conn.request("GET", f"/basic-metrics?url={encoded_url}", headers=self.headers)
            
            res = conn.getresponse()
            data = res.read()
            
            if res.status == 200:
                result = json.loads(data.decode("utf-8"))
                print(f"   ✅ Success! Fetched basic metrics")
                return result
            else:
                print(f"   ❌ HTTP Error: {res.status} - {res.reason}")
                print(f"   Response: {data.decode('utf-8')}")
                return None
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return None
    
    def get_url_metrics(self, url):
        """Get detailed URL metrics"""
        try:
            print(f"\n🔍 Fetching URL metrics for {url}...")
            
            conn = http.client.HTTPSConnection("seo-api-dr-rd-rank-keywords-backlinks1.p.rapidapi.com")
            encoded_url = quote(url, safe='')
            conn.request("GET", f"/url-metrics?url={encoded_url}", headers=self.headers)
            
            res = conn.getresponse()
            data = res.read()
            
            if res.status == 200:
                result = json.loads(data.decode("utf-8"))
                print(f"   ✅ Success! Fetched URL metrics")
                return result
            else:
                print(f"   ❌ HTTP Error: {res.status} - {res.reason}")
                print(f"   Response: {data.decode('utf-8')}")
                return None
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return None
    
    def get_backlinks(self, url, mode='subdomains', limit=100):
        """Get backlinks for URL"""
        try:
            print(f"\n🔍 Fetching backlinks for {url} (mode: {mode}, limit: {limit})...")
            
            conn = http.client.HTTPSConnection("seo-api-dr-rd-rank-keywords-backlinks1.p.rapidapi.com")
            encoded_url = quote(url, safe='')
            conn.request("GET", f"/backlink-checker?mode={mode}&url={encoded_url}&limit={limit}", headers=self.headers)
            
            res = conn.getresponse()
            data = res.read()
            
            if res.status == 200:
                result = json.loads(data.decode("utf-8"))
                print(f"   ✅ Success! Fetched backlinks")
                return result
            else:
                print(f"   ❌ HTTP Error: {res.status} - {res.reason}")
                print(f"   Response: {data.decode('utf-8')}")
                return None
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return None
    
    def get_keyword_metrics(self, keyword, country='dk'):
        """Get keyword metrics"""
        try:
            print(f"\n🔍 Fetching keyword metrics for '{keyword}' in {country.upper()}...")
            
            conn = http.client.HTTPSConnection("seo-api-dr-rd-rank-keywords-backlinks1.p.rapidapi.com")
            encoded_keyword = quote(keyword)
            conn.request("GET", f"/keyword-metrics?keyword={encoded_keyword}&country={country}", headers=self.headers)
            
            res = conn.getresponse()
            data = res.read()
            
            if res.status == 200:
                result = json.loads(data.decode("utf-8"))
                print(f"   ✅ Success! Fetched keyword metrics")
                return result
            else:
                print(f"   ❌ HTTP Error: {res.status} - {res.reason}")
                print(f"   Response: {data.decode('utf-8')}")
                return None
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return None
    
    def get_keyword_suggestions(self, keyword, country='dk', limit=50):
        """Get keyword suggestions"""
        try:
            print(f"\n🔍 Fetching keyword suggestions for '{keyword}' in {country.upper()}...")
            
            conn = http.client.HTTPSConnection("seo-api-dr-rd-rank-keywords-backlinks1.p.rapidapi.com")
            encoded_keyword = quote(keyword)
            conn.request("GET", f"/keyword-generator?keyword={encoded_keyword}&country={country}&limit={limit}", headers=self.headers)
            
            res = conn.getresponse()
            data = res.read()
            
            if res.status == 200:
                result = json.loads(data.decode("utf-8"))
                print(f"   ✅ Success! Fetched keyword suggestions")
                return result
            else:
                print(f"   ❌ HTTP Error: {res.status} - {res.reason}")
                print(f"   Response: {data.decode('utf-8')}")
                return None
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return None
    
    def generate_report(self, domain, basic_metrics, url_metrics, backlinks, keyword_data, keyword_suggestions):
        """Generate comprehensive SEO report"""
        report = []
        report.append("=" * 80)
        report.append("COMPLETE SEO API ANALYSIS REPORT")
        report.append("=" * 80)
        report.append(f"\nDomain: {domain}")
        report.append(f"Analysis Date: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Basic Metrics
        if basic_metrics:
            report.append("\n" + "=" * 80)
            report.append("BASIC METRICS (DR, RD, RANK)")
            report.append("=" * 80)
            report.append(json.dumps(basic_metrics, indent=2))
        
        # URL Metrics
        if url_metrics:
            report.append("\n" + "=" * 80)
            report.append("URL METRICS")
            report.append("=" * 80)
            report.append(json.dumps(url_metrics, indent=2))
        
        # Backlinks
        if backlinks:
            report.append("\n" + "=" * 80)
            report.append("BACKLINKS")
            report.append("=" * 80)
            report.append(json.dumps(backlinks, indent=2))
        
        # Keyword Data
        if keyword_data:
            report.append("\n" + "=" * 80)
            report.append("KEYWORD METRICS")
            report.append("=" * 80)
            report.append(json.dumps(keyword_data, indent=2))
        
        # Keyword Suggestions
        if keyword_suggestions:
            report.append("\n" + "=" * 80)
            report.append("KEYWORD SUGGESTIONS")
            report.append("=" * 80)
            report.append(json.dumps(keyword_suggestions, indent=2))
        
        return "\n".join(report)

def main():
    print("=" * 80)
    print("COMPLETE SEO API CHECKER")
    print("=" * 80)
    
    # Configuration
    api_key = "5c359bb774msh32eed0a33c585c4p1466d6jsn5620b810b2f7"
    domain = "simplybeyond.dk"
    country = "dk"
    
    print(f"\nDomain: {domain}")
    print(f"Country: {country.upper()}")
    print(f"API: SEO API (DR, RD, Rank, Keywords, Backlinks)")
    
    # Initialize checker
    checker = SEOAPIChecker(api_key)
    
    # Fetch all data
    print("\n" + "=" * 80)
    print("FETCHING DATA...")
    print("=" * 80)
    
    basic_metrics = checker.get_basic_metrics(domain)
    time.sleep(1)
    
    url_metrics = checker.get_url_metrics(domain)
    time.sleep(1)
    
    backlinks = checker.get_backlinks(domain, mode='subdomains', limit=100)
    time.sleep(1)
    
    # Test with primary keyword
    keyword_data = checker.get_keyword_metrics("silke sovemaske", country)
    time.sleep(1)
    
    keyword_suggestions = checker.get_keyword_suggestions("silke", country, limit=50)
    
    # Generate report
    report = checker.generate_report(
        domain, 
        basic_metrics, 
        url_metrics, 
        backlinks, 
        keyword_data, 
        keyword_suggestions
    )
    
    # Save report
    with open("seo_api_complete_report.txt", "w", encoding="utf-8") as f:
        f.write(report)
    
    # Save JSON data
    all_data = {
        "domain": domain,
        "country": country,
        "timestamp": time.strftime('%Y-%m-%d %H:%M:%S'),
        "basic_metrics": basic_metrics,
        "url_metrics": url_metrics,
        "backlinks": backlinks,
        "keyword_data": keyword_data,
        "keyword_suggestions": keyword_suggestions
    }
    
    with open("seo_api_complete_data.json", "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=2)
    
    print("\n" + "=" * 80)
    print("✅ ANALYSIS COMPLETE!")
    print("=" * 80)
    print("\n📄 Reports saved:")
    print("   - seo_api_complete_report.txt (detailed report)")
    print("   - seo_api_complete_data.json (raw JSON data)")
    
    # Print summary
    print("\n📊 DATA COLLECTED:")
    if basic_metrics:
        print(f"   ✅ Basic Metrics: {len(str(basic_metrics))} bytes")
    if url_metrics:
        print(f"   ✅ URL Metrics: {len(str(url_metrics))} bytes")
    if backlinks:
        print(f"   ✅ Backlinks: {len(str(backlinks))} bytes")
    if keyword_data:
        print(f"   ✅ Keyword Data: {len(str(keyword_data))} bytes")
    if keyword_suggestions:
        print(f"   ✅ Keyword Suggestions: {len(str(keyword_suggestions))} bytes")

if __name__ == "__main__":
    main()
