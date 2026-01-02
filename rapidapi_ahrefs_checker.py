"""
RapidAPI Ahrefs Domain Research - Backlink Checker
Uses RapidAPI to fetch Ahrefs backlink data
"""

import http.client
import json
import time

class RapidAPIAhrefsChecker:
    def __init__(self, api_key, domain):
        self.api_key = api_key
        self.domain = domain
        self.headers = {
            'x-rapidapi-key': api_key,
            'x-rapidapi-host': 'ahrefs-domain-research.p.rapidapi.com'
        }
    
    def get_basic_metrics(self):
        """
        Get basic metrics including DR, backlinks, referring domains
        """
        try:
            print(f"\n🔍 Fetching basic metrics for {self.domain}...")
            
            conn = http.client.HTTPSConnection("ahrefs-domain-research.p.rapidapi.com")
            conn.request("GET", f"/basic-metrics?url={self.domain}", headers=self.headers)
            
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
    
    def get_backlinks(self, limit=100, mode="subdomains"):
        """
        Get backlinks for the domain
        """
        try:
            print(f"\n🔍 Fetching backlinks (limit: {limit}, mode: {mode})...")
            
            conn = http.client.HTTPSConnection("ahrefs-domain-research.p.rapidapi.com")
            conn.request("GET", f"/backlinks?url={self.domain}&limit={limit}&mode={mode}", headers=self.headers)
            
            res = conn.getresponse()
            data = res.read()
            
            if res.status == 200:
                result = json.loads(data.decode("utf-8"))
                print(f"   ✅ Success! Fetched {len(result.get('backlinks', []))} backlinks")
                return result
            else:
                print(f"   ❌ HTTP Error: {res.status} - {res.reason}")
                print(f"   Response: {data.decode('utf-8')}")
                return None
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return None
    
    def get_referring_domains(self, limit=100, mode="subdomains"):
        """
        Get referring domains
        """
        try:
            print(f"\n🔍 Fetching referring domains (limit: {limit}, mode: {mode})...")
            
            conn = http.client.HTTPSConnection("ahrefs-domain-research.p.rapidapi.com")
            conn.request("GET", f"/referring-domains?url={self.domain}&limit={limit}&mode={mode}", headers=self.headers)
            
            res = conn.getresponse()
            data = res.read()
            
            if res.status == 200:
                result = json.loads(data.decode("utf-8"))
                print(f"   ✅ Success! Fetched {len(result.get('refdomains', []))} referring domains")
                return result
            else:
                print(f"   ❌ HTTP Error: {res.status} - {res.reason}")
                print(f"   Response: {data.decode('utf-8')}")
                return None
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return None
    
    def get_anchors(self, limit=100, mode="subdomains"):
        """
        Get anchor text distribution
        """
        try:
            print(f"\n🔍 Fetching anchor texts (limit: {limit}, mode: {mode})...")
            
            conn = http.client.HTTPSConnection("ahrefs-domain-research.p.rapidapi.com")
            conn.request("GET", f"/anchors?url={self.domain}&limit={limit}&mode={mode}", headers=self.headers)
            
            res = conn.getresponse()
            data = res.read()
            
            if res.status == 200:
                result = json.loads(data.decode("utf-8"))
                print(f"   ✅ Success! Fetched {len(result.get('anchors', []))} anchor texts")
                return result
            else:
                print(f"   ❌ HTTP Error: {res.status} - {res.reason}")
                print(f"   Response: {data.decode('utf-8')}")
                return None
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return None
    
    def generate_report(self, basic_metrics, backlinks, referring_domains, anchors):
        """
        Generate comprehensive backlink report
        """
        report = []
        report.append("=" * 80)
        report.append("AHREFS BACKLINK ANALYSIS REPORT (via RapidAPI)")
        report.append("=" * 80)
        report.append(f"\nDomain: {self.domain}")
        report.append(f"Analysis Date: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Basic Metrics
        if basic_metrics:
            report.append("\n" + "=" * 80)
            report.append("BASIC METRICS")
            report.append("=" * 80)
            
            metrics = basic_metrics.get('metrics', {})
            if metrics:
                report.append(f"\nDomain Rating (DR): {metrics.get('domain_rating', 'N/A')}")
                report.append(f"URL Rating (UR): {metrics.get('url_rating', 'N/A')}")
                report.append(f"Backlinks: {metrics.get('backlinks', 'N/A'):,}")
                report.append(f"Referring Domains: {metrics.get('refdomains', 'N/A'):,}")
                report.append(f"Organic Traffic: {metrics.get('organic_traffic', 'N/A'):,}")
                report.append(f"Organic Keywords: {metrics.get('organic_keywords', 'N/A'):,}")
            
            report.append("\n\nRaw Data:")
            report.append(json.dumps(basic_metrics, indent=2))
        
        # Backlinks
        if backlinks:
            report.append("\n" + "=" * 80)
            report.append("TOP BACKLINKS")
            report.append("=" * 80)
            
            backlink_list = backlinks.get('backlinks', [])
            if backlink_list:
                report.append(f"\nTotal Backlinks Found: {len(backlink_list)}")
                report.append("\nTop Backlinks:")
                for i, bl in enumerate(backlink_list[:20], 1):
                    report.append(f"\n{i}. Source: {bl.get('url_from', 'N/A')}")
                    report.append(f"   Target: {bl.get('url_to', 'N/A')}")
                    report.append(f"   Anchor: {bl.get('anchor', 'N/A')}")
                    report.append(f"   Domain Rating: {bl.get('domain_rating', 'N/A')}")
                    report.append(f"   Traffic: {bl.get('traffic', 'N/A')}")
            
            report.append("\n\nRaw Data:")
            report.append(json.dumps(backlinks, indent=2))
        
        # Referring Domains
        if referring_domains:
            report.append("\n" + "=" * 80)
            report.append("TOP REFERRING DOMAINS")
            report.append("=" * 80)
            
            refdomain_list = referring_domains.get('refdomains', [])
            if refdomain_list:
                report.append(f"\nTotal Referring Domains: {len(refdomain_list)}")
                report.append("\nTop Referring Domains:")
                for i, rd in enumerate(refdomain_list[:20], 1):
                    report.append(f"\n{i}. Domain: {rd.get('domain', 'N/A')}")
                    report.append(f"   Domain Rating: {rd.get('domain_rating', 'N/A')}")
                    report.append(f"   Backlinks: {rd.get('backlinks', 'N/A')}")
                    report.append(f"   First Seen: {rd.get('first_seen', 'N/A')}")
            
            report.append("\n\nRaw Data:")
            report.append(json.dumps(referring_domains, indent=2))
        
        # Anchors
        if anchors:
            report.append("\n" + "=" * 80)
            report.append("TOP ANCHOR TEXTS")
            report.append("=" * 80)
            
            anchor_list = anchors.get('anchors', [])
            if anchor_list:
                report.append(f"\nTotal Anchor Texts: {len(anchor_list)}")
                report.append("\nTop Anchor Texts:")
                for i, anc in enumerate(anchor_list[:20], 1):
                    report.append(f"\n{i}. Anchor: {anc.get('anchor', 'N/A')}")
                    report.append(f"   Backlinks: {anc.get('backlinks', 'N/A')}")
                    report.append(f"   Referring Domains: {anc.get('refdomains', 'N/A')}")
            
            report.append("\n\nRaw Data:")
            report.append(json.dumps(anchors, indent=2))
        
        return "\n".join(report)

def main():
    print("=" * 80)
    print("RAPIDAPI AHREFS DOMAIN RESEARCH - BACKLINK CHECKER")
    print("=" * 80)
    
    # Configuration
    api_key = "5c359bb774msh32eed0a33c585c4p1466d6jsn5620b810b2f7"
    domain = "simplybeyond.dk"
    
    print(f"\nDomain: {domain}")
    print(f"API: RapidAPI Ahrefs Domain Research")
    
    # Initialize checker
    checker = RapidAPIAhrefsChecker(api_key, domain)
    
    # Fetch data
    basic_metrics = checker.get_basic_metrics()
    time.sleep(1)  # Rate limiting
    
    backlinks = checker.get_backlinks(limit=100, mode="subdomains")
    time.sleep(1)
    
    referring_domains = checker.get_referring_domains(limit=100, mode="subdomains")
    time.sleep(1)
    
    anchors = checker.get_anchors(limit=100, mode="subdomains")
    
    # Generate report
    report = checker.generate_report(basic_metrics, backlinks, referring_domains, anchors)
    
    # Save report
    with open("rapidapi_ahrefs_report.txt", "w", encoding="utf-8") as f:
        f.write(report)
    
    # Save JSON data
    all_data = {
        "domain": domain,
        "timestamp": time.strftime('%Y-%m-%d %H:%M:%S'),
        "basic_metrics": basic_metrics,
        "backlinks": backlinks,
        "referring_domains": referring_domains,
        "anchors": anchors
    }
    
    with open("rapidapi_ahrefs_data.json", "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=2)
    
    print("\n" + "=" * 80)
    print("✅ ANALYSIS COMPLETE!")
    print("=" * 80)
    print("\n📄 Reports saved:")
    print("   - rapidapi_ahrefs_report.txt (detailed report)")
    print("   - rapidapi_ahrefs_data.json (raw JSON data)")
    
    # Print summary
    if basic_metrics:
        print("\n📊 DOMAIN METRICS:")
        metrics = basic_metrics.get('metrics', {})
        if metrics:
            print(f"   Domain Rating (DR): {metrics.get('domain_rating', 'N/A')}")
            print(f"   Backlinks: {metrics.get('backlinks', 'N/A'):,}")
            print(f"   Referring Domains: {metrics.get('refdomains', 'N/A'):,}")
            print(f"   Organic Traffic: {metrics.get('organic_traffic', 'N/A'):,}")
    
    if backlinks:
        print(f"\n🔗 BACKLINKS:")
        print(f"   Data fetched: {len(str(backlinks))} bytes")
    
    if referring_domains:
        print(f"\n🌐 REFERRING DOMAINS:")
        print(f"   Data fetched: {len(str(referring_domains))} bytes")
    
    if anchors:
        print(f"\n⚓ ANCHOR TEXTS:")
        print(f"   Data fetched: {len(str(anchors))} bytes")

if __name__ == "__main__":
    main()
