import http.client
import json
import time
import hashlib
import hmac
import base64
from urllib.parse import quote, urlparse
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from collections import Counter

class SEODashboard:
    """Interactive SEO Analysis Dashboard"""
    
    def __init__(self):
        self.rapidapi_key = "5c359bb774msh32eed0a33c585c4p1466d6jsn5620b810b2f7"
        self.moz_access_id = "mozscape-c7fe158e8e"
        self.moz_secret_key = "e0c2a5e8e0e44f5e8c7fe158e8e0c2a5"
        
    def display_header(self):
        """Display dashboard header"""
        print("\n" + "=" * 100)
        print(" " * 35 + "SEO ANALYSIS DASHBOARD")
        print("=" * 100)
        print("\n🔍 Comprehensive SEO & Backlink Analysis Tool")
        print("📊 Powered by 6 Data Sources: Google, Ahrefs, Moz, SimilarWeb, SEO API, Custom Crawler")
        print("=" * 100 + "\n")
    
    def get_domain_input(self):
        """Get domain from user"""
        while True:
            domain = input("🌐 Enter domain to analyze (e.g., example.com): ").strip()
            
            # Remove protocol if present
            domain = domain.replace("https://", "").replace("http://", "").replace("www.", "")
            
            # Remove trailing slash
            domain = domain.rstrip("/")
            
            if domain and "." in domain:
                return domain
            else:
                print("❌ Invalid domain. Please enter a valid domain (e.g., example.com)\n")
    
    def get_location_input(self):
        """Get location from user"""
        print("\n📍 Select Location:")
        print("1. Denmark (DK)")
        print("2. United States (US)")
        print("3. United Kingdom (GB)")
        print("4. Germany (DE)")
        print("5. Sweden (SE)")
        print("6. Norway (NO)")
        print("7. Custom")
        
        choice = input("\nEnter choice (1-7) [default: 1]: ").strip() or "1"
        
        locations = {
            "1": "DK",
            "2": "US",
            "3": "GB",
            "4": "DE",
            "5": "SE",
            "6": "NO"
        }
        
        if choice == "7":
            return input("Enter country code (e.g., FR, ES, IT): ").strip().upper()
        
        return locations.get(choice, "DK")
    
    def get_language_input(self):
        """Get language from user"""
        print("\n🗣️ Select Language:")
        print("1. Danish (da)")
        print("2. English (en)")
        print("3. German (de)")
        print("4. Swedish (sv)")
        print("5. Norwegian (no)")
        print("6. Custom")
        
        choice = input("\nEnter choice (1-6) [default: 1]: ").strip() or "1"
        
        languages = {
            "1": "da",
            "2": "en",
            "3": "de",
            "4": "sv",
            "5": "no"
        }
        
        if choice == "6":
            return input("Enter language code (e.g., fr, es, it): ").strip().lower()
        
        return languages.get(choice, "da")
    
    def get_keywords_input(self):
        """Get keywords from user"""
        print("\n🔑 Enter Keywords to Analyze (comma-separated):")
        print("Example: silk pillowcase, sleep mask, hair bonnet")
        
        keywords_input = input("\nKeywords: ").strip()
        
        if keywords_input:
            return [k.strip() for k in keywords_input.split(",") if k.strip()]
        else:
            return []
    
    def crawl_sitemap(self, domain):
        """Crawl sitemap"""
        print(f"\n📊 Crawling sitemap for {domain}...")
        
        try:
            import urllib.request
            sitemap_url = f"https://{domain}/sitemap.xml"
            
            with urllib.request.urlopen(sitemap_url, timeout=10) as response:
                xml_content = response.read().decode('utf-8')
            
            root = ET.fromstring(xml_content)
            urls = []
            
            for url in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
                loc = url.text
                if loc.endswith('.xml'):
                    # Sub-sitemap
                    try:
                        with urllib.request.urlopen(loc, timeout=10) as sub_response:
                            sub_xml = sub_response.read().decode('utf-8')
                        sub_root = ET.fromstring(sub_xml)
                        for sub_url in sub_root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
                            if not sub_url.text.endswith('.xml'):
                                urls.append(sub_url.text)
                    except:
                        pass
                else:
                    urls.append(loc)
            
            print(f"   ✅ Found {len(urls)} pages")
            return {"success": True, "pages": len(urls), "urls": urls[:10]}  # Return first 10
            
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def analyze_moz(self, domain):
        """Analyze with Moz API"""
        print(f"\n📊 Analyzing with Moz API...")
        
        try:
            expires = int(time.time()) + 300
            string_to_sign = f"{self.moz_access_id}\n{expires}"
            binary_signature = hmac.new(
                self.moz_secret_key.encode('utf-8'),
                string_to_sign.encode('utf-8'),
                hashlib.sha1
            ).digest()
            signature = base64.b64encode(binary_signature).decode('utf-8')
            
            conn = http.client.HTTPSConnection("lsapi.seomoz.com")
            url = f"/v2/url_metrics/{quote(domain, safe='')}?AccessID={self.moz_access_id}&Expires={expires}&Signature={quote(signature)}"
            
            conn.request("GET", url)
            res = conn.getresponse()
            data = json.loads(res.read().decode("utf-8"))
            
            if "domain_authority" in data:
                print(f"   ✅ DA: {data.get('domain_authority', 0)}, PA: {data.get('page_authority', 0)}")
                return {"success": True, "data": data}
            else:
                print(f"   ❌ Error: {data}")
                return {"success": False, "error": data}
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def analyze_ahrefs_domain(self, domain):
        """Analyze with Ahrefs Domain API"""
        print(f"\n📊 Analyzing with Ahrefs Domain API...")
        
        try:
            conn = http.client.HTTPSConnection("ahrefs-domain-research.p.rapidapi.com")
            headers = {
                'x-rapidapi-key': self.rapidapi_key,
                'x-rapidapi-host': "ahrefs-domain-research.p.rapidapi.com"
            }
            
            conn.request("GET", f"/domain-rating/?domain={domain}", headers=headers)
            res = conn.getresponse()
            data = json.loads(res.read().decode("utf-8"))
            
            if "domainRating" in data:
                print(f"   ✅ DR: {data.get('domainRating', 0)}, Rank: {data.get('ahRank', 0):,}")
                return {"success": True, "data": data}
            else:
                print(f"   ❌ Error: {data}")
                return {"success": False, "error": data}
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def analyze_similarweb(self, domain):
        """Analyze with SimilarWeb API"""
        print(f"\n📊 Analyzing with SimilarWeb API...")
        
        try:
            conn = http.client.HTTPSConnection("similarweb-insights.p.rapidapi.com")
            headers = {
                'x-rapidapi-key': self.rapidapi_key,
                'x-rapidapi-host': "similarweb-insights.p.rapidapi.com"
            }
            
            conn.request("GET", f"/traffic/?domain={domain}", headers=headers)
            res = conn.getresponse()
            data = json.loads(res.read().decode("utf-8"))
            
            if "visits" in data:
                visits = data.get("visits", {})
                latest_month = list(visits.keys())[-1] if visits else "N/A"
                latest_visits = visits.get(latest_month, 0) if visits else 0
                print(f"   ✅ Visits: {latest_visits:,} ({latest_month})")
                return {"success": True, "data": data}
            else:
                print(f"   ❌ Error: {data}")
                return {"success": False, "error": data}
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def analyze_seo_api(self, domain, location):
        """Analyze with SEO API"""
        print(f"\n📊 Analyzing with SEO API...")
        
        try:
            conn = http.client.HTTPSConnection("seo-api-dr-rd-rank-keywords-backlinks1.p.rapidapi.com")
            headers = {
                'x-rapidapi-key': self.rapidapi_key,
                'x-rapidapi-host': "seo-api-dr-rd-rank-keywords-backlinks1.p.rapidapi.com"
            }
            
            # Get backlinks
            conn.request("GET", f"/backlinks/?domain={domain}&country={location.lower()}", headers=headers)
            res = conn.getresponse()
            data = json.loads(res.read().decode("utf-8"))
            
            if "overview" in data:
                overview = data.get("overview", {})
                print(f"   ✅ Backlinks: {overview.get('backlinks', 0)}, Domains: {overview.get('referringDomains', 0)}")
                return {"success": True, "data": data}
            else:
                print(f"   ❌ Error: {data}")
                return {"success": False, "error": data}
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def analyze_google_keywords(self, domain, keywords, location, language):
        """Analyze with Google Keyword Insight"""
        print(f"\n📊 Analyzing with Google Keyword Insight...")
        
        results = {}
        
        try:
            conn = http.client.HTTPSConnection("google-keyword-insight1.p.rapidapi.com")
            headers = {
                'x-rapidapi-key': self.rapidapi_key,
                'x-rapidapi-host': "google-keyword-insight1.p.rapidapi.com"
            }
            
            # URL keywords
            conn.request("GET", f"/urlkeysuggest/?url={domain}&location={location}&lang={language}", headers=headers)
            res = conn.getresponse()
            url_data = json.loads(res.read().decode("utf-8"))
            
            if isinstance(url_data, list):
                print(f"   ✅ URL Keywords: {len(url_data)}")
                results["url_keywords"] = url_data
            
            time.sleep(1)
            
            # Keyword suggestions
            if keywords:
                for keyword in keywords[:3]:  # Limit to 3 keywords
                    encoded_keyword = quote(keyword)
                    conn.request("GET", f"/keysuggest/?keyword={encoded_keyword}&location={location}&lang={language}", headers=headers)
                    res = conn.getresponse()
                    keyword_data = json.loads(res.read().decode("utf-8"))
                    
                    if isinstance(keyword_data, list):
                        print(f"   ✅ '{keyword}': {len(keyword_data)} suggestions")
                        results[f"keyword_{keyword}"] = keyword_data
                    
                    time.sleep(1)
            
            return {"success": True, "data": results}
            
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def generate_report(self, domain, results):
        """Generate comprehensive report"""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        filename = f"seo_dashboard_report_{domain.replace('.', '_')}.txt"
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write("=" * 100 + "\n")
            f.write(" " * 35 + "SEO ANALYSIS REPORT\n")
            f.write("=" * 100 + "\n\n")
            f.write(f"Domain: {domain}\n")
            f.write(f"Generated: {timestamp}\n")
            f.write("=" * 100 + "\n\n")
            
            # Sitemap
            if "sitemap" in results and results["sitemap"]["success"]:
                f.write("SITEMAP ANALYSIS\n")
                f.write("-" * 100 + "\n")
                f.write(f"Total Pages: {results['sitemap']['pages']}\n\n")
            
            # Moz
            if "moz" in results and results["moz"]["success"]:
                data = results["moz"]["data"]
                f.write("MOZ METRICS\n")
                f.write("-" * 100 + "\n")
                f.write(f"Domain Authority: {data.get('domain_authority', 0)}\n")
                f.write(f"Page Authority: {data.get('page_authority', 0)}\n\n")
            
            # Ahrefs
            if "ahrefs" in results and results["ahrefs"]["success"]:
                data = results["ahrefs"]["data"]
                f.write("AHREFS METRICS\n")
                f.write("-" * 100 + "\n")
                f.write(f"Domain Rating: {data.get('domainRating', 0)}\n")
                f.write(f"Ahrefs Rank: {data.get('ahRank', 0):,}\n\n")
            
            # SimilarWeb
            if "similarweb" in results and results["similarweb"]["success"]:
                data = results["similarweb"]["data"]
                f.write("SIMILARWEB METRICS\n")
                f.write("-" * 100 + "\n")
                visits = data.get("visits", {})
                if visits:
                    for month, count in list(visits.items())[-3:]:
                        f.write(f"{month}: {count:,} visits\n")
                f.write("\n")
            
            # SEO API
            if "seo_api" in results and results["seo_api"]["success"]:
                data = results["seo_api"]["data"]
                overview = data.get("overview", {})
                f.write("BACKLINK PROFILE\n")
                f.write("-" * 100 + "\n")
                f.write(f"Total Backlinks: {overview.get('backlinks', 0)}\n")
                f.write(f"Referring Domains: {overview.get('referringDomains', 0)}\n")
                f.write(f"Domain Rating: {overview.get('domainRating', 0)}\n\n")
            
            # Google Keywords
            if "google" in results and results["google"]["success"]:
                data = results["google"]["data"]
                f.write("KEYWORD ANALYSIS\n")
                f.write("-" * 100 + "\n")
                
                if "url_keywords" in data:
                    f.write(f"URL Keywords: {len(data['url_keywords'])}\n")
                    for kw in data['url_keywords'][:10]:
                        f.write(f"  - {kw.get('text', '')}: {kw.get('volume', 0)} vol, {kw.get('competition_level', 'N/A')} comp\n")
                    f.write("\n")
        
        print(f"\n✅ Report saved: {filename}")
        return filename
    
    def run(self):
        """Run the dashboard"""
        self.display_header()
        
        # Get inputs
        domain = self.get_domain_input()
        location = self.get_location_input()
        language = self.get_language_input()
        keywords = self.get_keywords_input()
        
        print("\n" + "=" * 100)
        print(f"🎯 Analyzing: {domain}")
        print(f"📍 Location: {location}")
        print(f"🗣️ Language: {language}")
        if keywords:
            print(f"🔑 Keywords: {', '.join(keywords)}")
        print("=" * 100)
        
        # Run analyses
        results = {}
        
        results["sitemap"] = self.crawl_sitemap(domain)
        time.sleep(1)
        
        results["moz"] = self.analyze_moz(domain)
        time.sleep(1)
        
        results["ahrefs"] = self.analyze_ahrefs_domain(domain)
        time.sleep(1)
        
        results["similarweb"] = self.analyze_similarweb(domain)
        time.sleep(1)
        
        results["seo_api"] = self.analyze_seo_api(domain, location)
        time.sleep(1)
        
        results["google"] = self.analyze_google_keywords(domain, keywords, location, language)
        
        # Generate report
        print("\n" + "=" * 100)
        print("📄 GENERATING REPORT...")
        print("=" * 100)
        
        report_file = self.generate_report(domain, results)
        
        # Summary
        print("\n" + "=" * 100)
        print(" " * 40 + "SUMMARY")
        print("=" * 100 + "\n")
        
        if results["moz"]["success"]:
            data = results["moz"]["data"]
            print(f"📊 Domain Authority: {data.get('domain_authority', 0)}")
        
        if results["ahrefs"]["success"]:
            data = results["ahrefs"]["data"]
            print(f"📊 Domain Rating: {data.get('domainRating', 0)}")
        
        if results["seo_api"]["success"]:
            data = results["seo_api"]["data"]
            overview = data.get("overview", {})
            print(f"🔗 Backlinks: {overview.get('backlinks', 0)} from {overview.get('referringDomains', 0)} domains")
        
        if results["similarweb"]["success"]:
            data = results["similarweb"]["data"]
            visits = data.get("visits", {})
            if visits:
                latest_month = list(visits.keys())[-1]
                latest_visits = visits[latest_month]
                print(f"👥 Monthly Visits: {latest_visits:,} ({latest_month})")
        
        if results["sitemap"]["success"]:
            print(f"📄 Pages Indexed: {results['sitemap']['pages']}")
        
        print("\n" + "=" * 100)
        print(f"✅ Analysis Complete! Report saved to: {report_file}")
        print("=" * 100 + "\n")

if __name__ == "__main__":
    dashboard = SEODashboard()
    dashboard.run()
