import urllib.request
import urllib.parse
import json
import time
from html.parser import HTMLParser

class BacklinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.backlinks = []
        self.in_result = False
        
    def handle_starttag(self, tag, attrs):
        if tag == "a":
            attrs_dict = dict(attrs)
            href = attrs_dict.get("href", "")
            if href:
                self.backlinks.append(href)

def check_google_backlinks(domain):
    """
    Use Google search to find pages linking to the domain
    Note: This is limited and may be blocked by Google
    """
    print(f"\n🔍 Searching for backlinks using Google...")
    backlinks = []
    
    try:
        # Search for pages linking to the domain
        query = f"link:{domain}"
        encoded_query = urllib.parse.quote(query)
        url = f"https://www.google.com/search?q={encoded_query}&num=100"
        
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        )
        
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8', errors='ignore')
            
        # Parse results (simplified)
        parser = BacklinkParser()
        parser.feed(html)
        
        print(f"⚠️  Google search operator 'link:' is deprecated and may not return results")
        print(f"   Found {len(parser.backlinks)} potential results (may include false positives)")
        
        return parser.backlinks[:20]  # Return first 20
        
    except Exception as e:
        print(f"❌ Error checking Google backlinks: {e}")
        return []

def check_bing_backlinks(domain):
    """
    Use Bing search to find pages linking to the domain
    """
    print(f"\n🔍 Searching for backlinks using Bing...")
    backlinks = []
    
    try:
        # Bing link: operator
        query = f"link:{domain}"
        encoded_query = urllib.parse.quote(query)
        url = f"https://www.bing.com/search?q={encoded_query}&count=50"
        
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        )
        
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8', errors='ignore')
        
        # Simple parsing to extract URLs
        import re
        urls = re.findall(r'https?://[^\s<>"]+', html)
        
        # Filter for unique domains
        unique_domains = set()
        for url in urls:
            if domain not in url and 'bing.com' not in url and 'microsoft.com' not in url:
                try:
                    parsed = urllib.parse.urlparse(url)
                    if parsed.netloc:
                        unique_domains.add(parsed.netloc)
                except:
                    pass
        
        backlinks = list(unique_domains)[:20]
        print(f"✅ Found {len(backlinks)} potential backlink domains from Bing")
        
        return backlinks
        
    except Exception as e:
        print(f"❌ Error checking Bing backlinks: {e}")
        return []

def check_common_crawl(domain):
    """
    Query Common Crawl index for pages linking to domain
    """
    print(f"\n🔍 Checking Common Crawl index...")
    
    try:
        # Common Crawl Index API
        url = f"https://index.commoncrawl.org/CC-MAIN-2024-10-index?url={domain}&output=json"
        
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=30) as response:
            data = response.read().decode('utf-8')
        
        # Parse JSONL (one JSON per line)
        results = []
        for line in data.strip().split('\n'):
            if line:
                try:
                    results.append(json.loads(line))
                except:
                    pass
        
        print(f"✅ Found {len(results)} records in Common Crawl")
        return results[:50]
        
    except Exception as e:
        print(f"❌ Error checking Common Crawl: {e}")
        return []

def generate_backlink_report(domain, google_results, bing_results, commoncrawl_results):
    """
    Generate a comprehensive backlink report
    """
    report = []
    report.append("=" * 80)
    report.append("BACKLINK ANALYSIS REPORT")
    report.append("=" * 80)
    report.append(f"\nDomain: {domain}")
    report.append(f"Analysis Date: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("")
    
    report.append("\n" + "=" * 80)
    report.append("IMPORTANT NOTES")
    report.append("=" * 80)
    report.append("""
This free backlink checker has limitations:
1. Google's 'link:' operator is deprecated and may not work
2. Bing results are limited and may include false positives
3. Common Crawl data may be outdated (updated quarterly)

For comprehensive backlink data, use:
- Google Search Console (free, most accurate)
- Ahrefs Webmaster Tools (free tier available)
- Bing Webmaster Tools (free)
- Moz Link Explorer (limited free)
""")
    
    report.append("\n" + "=" * 80)
    report.append("BING SEARCH RESULTS")
    report.append("=" * 80)
    if bing_results:
        report.append(f"\nFound {len(bing_results)} potential backlink domains:\n")
        for i, domain in enumerate(bing_results, 1):
            report.append(f"{i}. {domain}")
    else:
        report.append("\nNo results found from Bing search")
    
    report.append("\n" + "=" * 80)
    report.append("COMMON CRAWL RESULTS")
    report.append("=" * 80)
    if commoncrawl_results:
        report.append(f"\nFound {len(commoncrawl_results)} records in Common Crawl:\n")
        for i, record in enumerate(commoncrawl_results[:20], 1):
            url = record.get('url', 'N/A')
            timestamp = record.get('timestamp', 'N/A')
            report.append(f"{i}. {url}")
            report.append(f"   Crawled: {timestamp}")
    else:
        report.append("\nNo results found in Common Crawl")
    
    report.append("\n" + "=" * 80)
    report.append("RECOMMENDATIONS")
    report.append("=" * 80)
    report.append("""
To get accurate backlink data:

1. GOOGLE SEARCH CONSOLE (Recommended - Free)
   - Visit: https://search.google.com/search-console
   - Add and verify your property
   - Go to Links section for complete backlink data
   
2. AHREFS WEBMASTER TOOLS (Free Tier)
   - Visit: https://ahrefs.com/webmaster-tools
   - Sign up for free account
   - Verify domain ownership
   - Access backlink data, broken links, and more
   
3. BING WEBMASTER TOOLS (Free)
   - Visit: https://www.bing.com/webmasters
   - Add and verify your site
   - View inbound links report

4. MOZ LINK EXPLORER (Limited Free)
   - Visit: https://moz.com/link-explorer
   - Enter domain for limited free results
""")
    
    return "\n".join(report)

def main():
    domain = "simplybeyond.dk"
    
    print("=" * 80)
    print("BACKLINK CHECKER")
    print("=" * 80)
    print(f"\nAnalyzing backlinks for: {domain}")
    print("\nNote: Free backlink checking has significant limitations.")
    print("For accurate data, use Google Search Console or Ahrefs Webmaster Tools.")
    print("=" * 80)
    
    # Check different sources
    google_results = check_google_backlinks(domain)
    time.sleep(2)  # Rate limiting
    
    bing_results = check_bing_backlinks(domain)
    time.sleep(2)  # Rate limiting
    
    commoncrawl_results = check_common_crawl(domain)
    
    # Generate report
    report = generate_backlink_report(domain, google_results, bing_results, commoncrawl_results)
    
    # Save report
    with open("backlink_analysis.txt", "w", encoding="utf-8") as f:
        f.write(report)
    
    print("\n" + "=" * 80)
    print("✅ Backlink analysis complete!")
    print("📄 Report saved to: backlink_analysis.txt")
    print("=" * 80)
    
    # Print summary
    print("\nSUMMARY:")
    print(f"- Bing results: {len(bing_results)} potential domains")
    print(f"- Common Crawl: {len(commoncrawl_results)} records")
    print("\n⚠️  For comprehensive backlink data, please use:")
    print("   1. Google Search Console (most accurate)")
    print("   2. Ahrefs Webmaster Tools (free tier)")
    print("   3. Bing Webmaster Tools")

if __name__ == "__main__":
    main()
