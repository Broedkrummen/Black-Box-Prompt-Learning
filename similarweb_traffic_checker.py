"""
SimilarWeb Insights - Traffic & Engagement Checker
Uses RapidAPI to fetch SimilarWeb traffic data
"""

import http.client
import json
import time

class SimilarWebChecker:
    def __init__(self, api_key, domain):
        self.api_key = api_key
        self.domain = domain
        self.headers = {
            'x-rapidapi-key': api_key,
            'x-rapidapi-host': 'similarweb-insights.p.rapidapi.com'
        }
    
    def get_traffic_data(self):
        """
        Get traffic and engagement metrics
        """
        try:
            print(f"\n🔍 Fetching traffic data for {self.domain}...")
            
            conn = http.client.HTTPSConnection("similarweb-insights.p.rapidapi.com")
            conn.request("GET", f"/traffic?domain={self.domain}", headers=self.headers)
            
            res = conn.getresponse()
            data = res.read()
            
            if res.status == 200:
                result = json.loads(data.decode("utf-8"))
                print(f"   ✅ Success! Fetched traffic data")
                return result
            else:
                print(f"   ❌ HTTP Error: {res.status} - {res.reason}")
                print(f"   Response: {data.decode('utf-8')}")
                return None
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return None
    
    def get_website_details(self):
        """
        Get website details
        """
        try:
            print(f"\n🔍 Fetching website details for {self.domain}...")
            
            conn = http.client.HTTPSConnection("similarweb-insights.p.rapidapi.com")
            conn.request("GET", f"/website-details?domain={self.domain}", headers=self.headers)
            
            res = conn.getresponse()
            data = res.read()
            
            if res.status == 200:
                result = json.loads(data.decode("utf-8"))
                print(f"   ✅ Success! Fetched website details")
                return result
            else:
                print(f"   ❌ HTTP Error: {res.status} - {res.reason}")
                print(f"   Response: {data.decode('utf-8')}")
                return None
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return None
    
    def get_all_insights(self):
        """
        Get all insights
        """
        try:
            print(f"\n🔍 Fetching all insights for {self.domain}...")
            
            conn = http.client.HTTPSConnection("similarweb-insights.p.rapidapi.com")
            conn.request("GET", f"/all-insights?domain={self.domain}", headers=self.headers)
            
            res = conn.getresponse()
            data = res.read()
            
            if res.status == 200:
                result = json.loads(data.decode("utf-8"))
                print(f"   ✅ Success! Fetched all insights")
                return result
            else:
                print(f"   ❌ HTTP Error: {res.status} - {res.reason}")
                print(f"   Response: {data.decode('utf-8')}")
                return None
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return None
    
    def get_rank(self):
        """
        Get rank data
        """
        try:
            print(f"\n🔍 Fetching rank data for {self.domain}...")
            
            conn = http.client.HTTPSConnection("similarweb-insights.p.rapidapi.com")
            conn.request("GET", f"/rank?domain={self.domain}", headers=self.headers)
            
            res = conn.getresponse()
            data = res.read()
            
            if res.status == 200:
                result = json.loads(data.decode("utf-8"))
                print(f"   ✅ Success! Fetched rank data")
                return result
            else:
                print(f"   ❌ HTTP Error: {res.status} - {res.reason}")
                print(f"   Response: {data.decode('utf-8')}")
                return None
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return None
    
    def get_seo_data(self):
        """
        Get SEO data
        """
        try:
            print(f"\n🔍 Fetching SEO data for {self.domain}...")
            
            conn = http.client.HTTPSConnection("similarweb-insights.p.rapidapi.com")
            conn.request("GET", f"/seo?domain={self.domain}", headers=self.headers)
            
            res = conn.getresponse()
            data = res.read()
            
            if res.status == 200:
                result = json.loads(data.decode("utf-8"))
                print(f"   ✅ Success! Fetched SEO data")
                return result
            else:
                print(f"   ❌ HTTP Error: {res.status} - {res.reason}")
                print(f"   Response: {data.decode('utf-8')}")
                return None
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return None
    
    def get_similar_sites(self):
        """
        Get similar sites
        """
        try:
            print(f"\n🔍 Fetching similar sites for {self.domain}...")
            
            conn = http.client.HTTPSConnection("similarweb-insights.p.rapidapi.com")
            conn.request("GET", f"/similar-sites?domain={self.domain}", headers=self.headers)
            
            res = conn.getresponse()
            data = res.read()
            
            if res.status == 200:
                result = json.loads(data.decode("utf-8"))
                print(f"   ✅ Success! Fetched similar sites")
                return result
            else:
                print(f"   ❌ HTTP Error: {res.status} - {res.reason}")
                print(f"   Response: {data.decode('utf-8')}")
                return None
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return None
    
    def generate_report(self, traffic_data, website_details, all_insights, rank_data, seo_data, similar_sites):
        """
        Generate comprehensive traffic report
        """
        report = []
        report.append("=" * 80)
        report.append("SIMILARWEB COMPREHENSIVE ANALYSIS REPORT")
        report.append("=" * 80)
        report.append(f"\nDomain: {self.domain}")
        report.append(f"Analysis Date: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Traffic Data
        if traffic_data:
            report.append("\n" + "=" * 80)
            report.append("TRAFFIC METRICS")
            report.append("=" * 80)
            report.append(json.dumps(traffic_data, indent=2))
        
        # Website Details
        if website_details:
            report.append("\n" + "=" * 80)
            report.append("WEBSITE DETAILS")
            report.append("=" * 80)
            report.append(json.dumps(website_details, indent=2))
        
        # All Insights
        if all_insights:
            report.append("\n" + "=" * 80)
            report.append("ALL INSIGHTS")
            report.append("=" * 80)
            report.append(json.dumps(all_insights, indent=2))
        
        # Rank Data
        if rank_data:
            report.append("\n" + "=" * 80)
            report.append("RANK DATA")
            report.append("=" * 80)
            report.append(json.dumps(rank_data, indent=2))
        
        # SEO Data
        if seo_data:
            report.append("\n" + "=" * 80)
            report.append("SEO DATA")
            report.append("=" * 80)
            report.append(json.dumps(seo_data, indent=2))
        
        # Similar Sites
        if similar_sites:
            report.append("\n" + "=" * 80)
            report.append("SIMILAR SITES")
            report.append("=" * 80)
            report.append(json.dumps(similar_sites, indent=2))
        
        return "\n".join(report)

def main():
    print("=" * 80)
    print("SIMILARWEB TRAFFIC & ENGAGEMENT CHECKER")
    print("=" * 80)
    
    # Configuration
    api_key = "5c359bb774msh32eed0a33c585c4p1466d6jsn5620b810b2f7"
    domain = "simplybeyond.dk"
    
    print(f"\nDomain: {domain}")
    print(f"API: RapidAPI SimilarWeb Insights")
    
    # Initialize checker
    checker = SimilarWebChecker(api_key, domain)
    
    # Fetch all data
    traffic_data = checker.get_traffic_data()
    time.sleep(1)
    
    website_details = checker.get_website_details()
    time.sleep(1)
    
    all_insights = checker.get_all_insights()
    time.sleep(1)
    
    rank_data = checker.get_rank()
    time.sleep(1)
    
    seo_data = checker.get_seo_data()
    time.sleep(1)
    
    similar_sites = checker.get_similar_sites()
    
    # Generate report
    report = checker.generate_report(traffic_data, website_details, all_insights, rank_data, seo_data, similar_sites)
    
    # Save report
    with open("similarweb_traffic_report.txt", "w", encoding="utf-8") as f:
        f.write(report)
    
    # Save JSON data
    all_data = {
        "domain": domain,
        "timestamp": time.strftime('%Y-%m-%d %H:%M:%S'),
        "traffic_data": traffic_data,
        "website_details": website_details,
        "all_insights": all_insights,
        "rank_data": rank_data,
        "seo_data": seo_data,
        "similar_sites": similar_sites
    }
    
    with open("similarweb_traffic_data.json", "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=2)
    
    print("\n" + "=" * 80)
    print("✅ ANALYSIS COMPLETE!")
    print("=" * 80)
    print("\n📄 Reports saved:")
    print("   - similarweb_traffic_report.txt (detailed report)")
    print("   - similarweb_traffic_data.json (raw JSON data)")
    
    # Print summary
    print("\n📊 DATA COLLECTED:")
    if traffic_data:
        print(f"   ✅ Traffic Data: {len(str(traffic_data))} bytes")
    if website_details:
        print(f"   ✅ Website Details: {len(str(website_details))} bytes")
    if all_insights:
        print(f"   ✅ All Insights: {len(str(all_insights))} bytes")
    if rank_data:
        print(f"   ✅ Rank Data: {len(str(rank_data))} bytes")
    if seo_data:
        print(f"   ✅ SEO Data: {len(str(seo_data))} bytes")
    if similar_sites:
        print(f"   ✅ Similar Sites: {len(str(similar_sites))} bytes")

if __name__ == "__main__":
    main()
