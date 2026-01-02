import urllib.request
import urllib.parse
import json
import time
from html.parser import HTMLParser
import re

class AhrefsWebmasterAPI:
    """
    Ahrefs Webmaster Tools API
    Requires domain verification and free API token
    """
    def __init__(self, api_token):
        self.api_token = api_token
        self.base_url = "https://api.ahrefs.com/v3"
    
    def get_backlinks(self, domain, limit=100):
        """Get backlinks from Ahrefs Webmaster Tools API"""
        try:
            print(f"\n🔍 Fetching backlinks from Ahrefs Webmaster Tools API...")
            
            # Backlinks endpoint
            url = f"{self.base_url}/site-explorer/backlinks"
            
            params = {
                'target': domain,
                'mode': 'domain',
                'limit': limit,
                'order_by': 'domain_rating:desc'
            }
            
            query_string = urllib.parse.urlencode(params)
            full_url = f"{url}?{query_string}"
            
            req = urllib.request.Request(
                full_url,
                headers={
                    'Authorization': f'Bearer {self.api_token}',
                    'Accept': 'application/json'
                }
            )
            
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode('utf-8'))
            
            backlinks = result.get('backlinks', [])
            print(f"✅ Successfully fetched {len(backlinks)} backlinks from Ahrefs API")
            return result
            
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8')
            print(f"❌ HTTP Error {e.code}: {error_body}")
            return None
        except Exception as e:
            print(f"❌ Error fetching backlinks: {e}")
            return None
    
    def get_domain_metrics(self, domain):
        """Get domain metrics (DR, backlinks count, etc.)"""
        try:
            print(f"\n🔍 Fetching domain metrics from Ahrefs...")
            
            url = f"{self.base_url}/site-explorer/metrics"
            
            params = {
                'target': domain,
                'mode': 'domain'
            }
            
            query_string = urllib.parse.urlencode(params)
            full_url = f"{url}?{query_string}"
            
            req = urllib.request.Request(
                full_url,
                headers={
                    'Authorization': f'Bearer {self.api_token}',
                    'Accept': 'application/json'
                }
            )
            
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode('utf-8'))
            
            print(f"✅ Successfully fetched domain metrics")
            return result
            
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8')
            print(f"❌ HTTP Error {e.code}: {error_body}")
            return None
        except Exception as e:
            print(f"❌ Error fetching metrics: {e}")
            return None

def scrape_ahrefs_free_checker(domain):
    """
    Scrape Ahrefs free backlink checker
    Note: This may be blocked or rate-limited
    """
    try:
        print(f"\n🔍 Checking Ahrefs free backlink checker...")
        print("⚠️  Note: Free checker shows limited results (top 100 backlinks)")
        
        # Ahrefs free backlink checker URL
        url = f"https://ahrefs.com/backlink-checker"
        
        # This would require browser automation or API access
        # The free checker requires JavaScript and CAPTCHA
        print("❌ Direct scraping of Ahrefs free checker is not possible")
        print("   Reason: Requires JavaScript, CAPTCHA, and violates ToS")
        print("\n💡 Alternative: Use Ahrefs Webmaster Tools (free with domain verification)")
        print("   1. Sign up at: https://ahrefs.com/webmaster-tools")
        print("   2. Verify your domain")
        print("   3. Get your API token")
        print("   4. Run this script with your API token")
        
        return None
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def generate_ahrefs_report(domain, metrics, backlinks):
    """Generate comprehensive Ahrefs backlink report"""
    report = []
    report.append("=" * 80)
    report.append("AHREFS BACKLINK ANALYSIS REPORT")
    report.append("=" * 80)
    report.append(f"\nDomain: {domain}")
    report.append(f"Analysis Date: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("")
    
    # Domain Metrics
    if metrics:
        report.append("\n" + "=" * 80)
        report.append("DOMAIN METRICS")
        report.append("=" * 80)
        
        domain_data = metrics.get('domain', {}) or metrics.get('metrics', {})
        
        report.append(f"\nDomain Rating (DR): {domain_data.get('domain_rating', 'N/A')}")
        report.append(f"Ahrefs Rank: {domain_data.get('ahrefs_rank', 'N/A')}")
        report.append(f"Total Backlinks: {domain_data.get('backlinks', 'N/A')}")
        report.append(f"Referring Domains: {domain_data.get('refdomains', 'N/A')}")
        report.append(f"Organic Traffic: {domain_data.get('organic_traffic', 'N/A')}")
        report.append(f"Organic Keywords: {domain_data.get('organic_keywords', 'N/A')}")
    
    # Backlinks
    if backlinks:
        links = backlinks.get('backlinks', [])
        report.append("\n" + "=" * 80)
        report.append(f"BACKLINKS ({len(links)} found)")
        report.append("=" * 80)
        
        for i, link in enumerate(links[:100], 1):  # Show first 100
            report.append(f"\n{i}. Source URL: {link.get('url_from', 'N/A')}")
            report.append(f"   Target URL: {link.get('url_to', 'N/A')}")
            report.append(f"   Anchor Text: {link.get('anchor', 'N/A')}")
            report.append(f"   Domain Rating: {link.get('domain_rating', 'N/A')}")
            report.append(f"   URL Rating: {link.get('url_rating', 'N/A')}")
            report.append(f"   Link Type: {link.get('link_type', 'N/A')}")
            report.append(f"   First Seen: {link.get('first_seen', 'N/A')}")
            report.append(f"   Last Seen: {link.get('last_seen', 'N/A')}")
        
        if len(links) > 100:
            report.append(f"\n... and {len(links) - 100} more backlinks")
    
    return "\n".join(report)

def main():
    print("=" * 80)
    print("AHREFS BACKLINK CHECKER")
    print("=" * 80)
    
    print("\n📋 AHREFS OPTIONS:")
    print("1. Use Ahrefs Webmaster Tools API (Recommended - Free)")
    print("2. Manual check using Ahrefs Free Backlink Checker")
    print("3. Skip Ahrefs and use existing SEO analysis")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    domain = "simplybeyond.dk"
    
    if choice == "1":
        print("\n" + "=" * 80)
        print("AHREFS WEBMASTER TOOLS API")
        print("=" * 80)
        print("\nTo use Ahrefs Webmaster Tools API:")
        print("1. Sign up at: https://ahrefs.com/webmaster-tools")
        print("2. Verify your domain (add meta tag or DNS record)")
        print("3. Get your API token from Settings > API")
        
        api_token = input("\nEnter your Ahrefs API token (or press Enter to skip): ").strip()
        
        if api_token:
            ahrefs = AhrefsWebmasterAPI(api_token)
            
            print("\n" + "=" * 80)
            print("FETCHING DATA FROM AHREFS API")
            print("=" * 80)
            
            metrics = ahrefs.get_domain_metrics(domain)
            time.sleep(1)
            
            backlinks = ahrefs.get_backlinks(domain, limit=100)
            
            if metrics or backlinks:
                report = generate_ahrefs_report(domain, metrics, backlinks)
                
                # Save report
                with open("ahrefs_backlink_report.txt", "w", encoding="utf-8") as f:
                    f.write(report)
                
                # Save raw JSON
                with open("ahrefs_backlink_data.json", "w", encoding="utf-8") as f:
                    json.dump({
                        "metrics": metrics,
                        "backlinks": backlinks
                    }, f, indent=2)
                
                print("\n" + "=" * 80)
                print("✅ AHREFS BACKLINK ANALYSIS COMPLETE!")
                print("=" * 80)
                print("\n📄 Reports saved:")
                print("   - ahrefs_backlink_report.txt")
                print("   - ahrefs_backlink_data.json")
                
                if metrics:
                    domain_data = metrics.get('domain', {}) or metrics.get('metrics', {})
                    print("\n📊 Quick Summary:")
                    print(f"   Domain Rating: {domain_data.get('domain_rating', 'N/A')}")
                    print(f"   Total Backlinks: {domain_data.get('backlinks', 'N/A')}")
                    print(f"   Referring Domains: {domain_data.get('refdomains', 'N/A')}")
            else:
                print("\n❌ Failed to fetch data from Ahrefs API")
        else:
            print("\n⚠️  No API token provided. Skipping Ahrefs API.")
    
    elif choice == "2":
        print("\n" + "=" * 80)
        print("AHREFS FREE BACKLINK CHECKER")
        print("=" * 80)
        print("\n📝 Manual Steps:")
        print("1. Visit: https://ahrefs.com/backlink-checker")
        print(f"2. Enter domain: {domain}")
        print("3. View top 100 backlinks for free")
        print("4. Export or copy the data manually")
        print("\n💡 For automated access, use Ahrefs Webmaster Tools API (Option 1)")
        
        scrape_ahrefs_free_checker(domain)
    
    else:
        print("\n✅ Using existing SEO analysis data")
        print("📄 Check these files for comprehensive SEO data:")
        print("   - seo_analysis_report.txt")
        print("   - seo_detailed_data.json")
        print("   - seo_data.csv")
        print("   - moz_backlink_report.txt")

if __name__ == "__main__":
    main()
