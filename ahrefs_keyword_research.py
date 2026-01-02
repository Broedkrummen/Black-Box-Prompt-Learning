"""
Ahrefs Keyword Research Tool
Uses RapidAPI to fetch keyword metrics and opportunities
"""

import http.client
import json
import time
from urllib.parse import quote

class AhrefsKeywordResearch:
    def __init__(self, api_key):
        self.api_key = api_key
        self.headers = {
            'x-rapidapi-key': api_key,
            'x-rapidapi-host': 'ahrefs-keyword-research.p.rapidapi.com'
        }
    
    def get_keyword_metrics(self, keyword, country='dk'):
        """
        Get keyword metrics including volume, difficulty, CPC
        """
        try:
            print(f"\n🔍 Fetching metrics for '{keyword}' in {country.upper()}...")
            
            conn = http.client.HTTPSConnection("ahrefs-keyword-research.p.rapidapi.com")
            encoded_keyword = quote(keyword)
            conn.request("GET", f"/keyword-metrics?keyword={encoded_keyword}&country={country}", headers=self.headers)
            
            res = conn.getresponse()
            data = res.read()
            
            if res.status == 200:
                result = json.loads(data.decode("utf-8"))
                print(f"   ✅ Success! Fetched metrics for '{keyword}'")
                return result
            else:
                print(f"   ❌ HTTP Error: {res.status} - {res.reason}")
                print(f"   Response: {data.decode('utf-8')}")
                return None
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return None
    
    def analyze_keywords(self, keywords, country='dk'):
        """
        Analyze multiple keywords
        """
        results = {}
        for keyword in keywords:
            result = self.get_keyword_metrics(keyword, country)
            if result:
                results[keyword] = result
            time.sleep(1)  # Rate limiting
        return results
    
    def generate_report(self, keyword_data, domain):
        """
        Generate comprehensive keyword research report
        """
        report = []
        report.append("=" * 80)
        report.append("AHREFS KEYWORD RESEARCH REPORT")
        report.append("=" * 80)
        report.append(f"\nDomain: {domain}")
        report.append(f"Analysis Date: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Keywords Analyzed: {len(keyword_data)}")
        report.append("")
        
        if keyword_data:
            # Summary statistics
            total_volume = 0
            avg_difficulty = 0
            avg_cpc = 0
            count = 0
            
            for keyword, data in keyword_data.items():
                if isinstance(data, dict):
                    volume = data.get('volume', 0)
                    difficulty = data.get('difficulty', 0)
                    cpc = data.get('cpc', 0)
                    
                    if volume:
                        total_volume += volume
                    if difficulty:
                        avg_difficulty += difficulty
                        count += 1
                    if cpc:
                        avg_cpc += cpc
            
            if count > 0:
                avg_difficulty = avg_difficulty / count
                avg_cpc = avg_cpc / count
            
            report.append("\n" + "=" * 80)
            report.append("SUMMARY STATISTICS")
            report.append("=" * 80)
            report.append(f"Total Search Volume: {total_volume:,}/month")
            report.append(f"Average Keyword Difficulty: {avg_difficulty:.1f}/100")
            report.append(f"Average CPC: ${avg_cpc:.2f}")
            report.append("")
            
            # Detailed keyword analysis
            report.append("\n" + "=" * 80)
            report.append("DETAILED KEYWORD ANALYSIS")
            report.append("=" * 80)
            
            # Sort by volume
            sorted_keywords = sorted(
                keyword_data.items(),
                key=lambda x: x[1].get('volume', 0) if isinstance(x[1], dict) else 0,
                reverse=True
            )
            
            for keyword, data in sorted_keywords:
                report.append(f"\n{'─' * 80}")
                report.append(f"Keyword: {keyword}")
                report.append(f"{'─' * 80}")
                
                if isinstance(data, dict):
                    volume = data.get('volume', 'N/A')
                    difficulty = data.get('difficulty', 'N/A')
                    cpc = data.get('cpc', 'N/A')
                    clicks = data.get('clicks', 'N/A')
                    ctr = data.get('ctr', 'N/A')
                    
                    report.append(f"Search Volume: {volume:,}/month" if isinstance(volume, int) else f"Search Volume: {volume}")
                    report.append(f"Keyword Difficulty: {difficulty}/100" if isinstance(difficulty, (int, float)) else f"Keyword Difficulty: {difficulty}")
                    report.append(f"CPC: ${cpc:.2f}" if isinstance(cpc, (int, float)) else f"CPC: {cpc}")
                    report.append(f"Estimated Clicks: {clicks:,}" if isinstance(clicks, int) else f"Estimated Clicks: {clicks}")
                    report.append(f"CTR: {ctr:.2%}" if isinstance(ctr, (int, float)) else f"CTR: {ctr}")
                    
                    # Opportunity score
                    if isinstance(volume, int) and isinstance(difficulty, (int, float)):
                        opportunity = volume / (difficulty + 1)
                        report.append(f"Opportunity Score: {opportunity:.0f} (higher is better)")
                    
                    # Recommendation
                    if isinstance(difficulty, (int, float)):
                        if difficulty < 30:
                            report.append("Recommendation: ✅ EASY - Great opportunity!")
                        elif difficulty < 50:
                            report.append("Recommendation: ⚠️ MEDIUM - Achievable with effort")
                        elif difficulty < 70:
                            report.append("Recommendation: 🔶 HARD - Requires strong authority")
                        else:
                            report.append("Recommendation: ❌ VERY HARD - Focus on easier keywords first")
                
                report.append("")
            
            # Raw data
            report.append("\n" + "=" * 80)
            report.append("RAW DATA (JSON)")
            report.append("=" * 80)
            report.append(json.dumps(keyword_data, indent=2))
        
        return "\n".join(report)

def main():
    print("=" * 80)
    print("AHREFS KEYWORD RESEARCH TOOL")
    print("=" * 80)
    
    # Configuration
    api_key = "5c359bb774msh32eed0a33c585c4p1466d6jsn5620b810b2f7"
    domain = "simplybeyond.dk"
    country = "dk"  # Denmark
    
    # Keywords to analyze (based on SimilarWeb data and product focus)
    keywords = [
        # Current ranking keywords
        "silke",
        "silke bonnet",
        "sove briller",
        
        # Product-related keywords
        "silke sovemaske",
        "silk sleep mask",
        "silk bonnet",
        "hair bonnet",
        
        # Commercial keywords
        "køb silke sovemaske",
        "bedste sovemaske",
        "silke pudebetræk",
        
        # Long-tail keywords
        "sovemaske til bedre søvn",
        "allergivenlig sovemaske",
        "mulberry silke",
    ]
    
    print(f"\nDomain: {domain}")
    print(f"Country: {country.upper()}")
    print(f"Keywords to analyze: {len(keywords)}")
    print(f"API: RapidAPI Ahrefs Keyword Research")
    
    # Initialize research tool
    researcher = AhrefsKeywordResearch(api_key)
    
    # Analyze keywords
    print("\n" + "=" * 80)
    print("ANALYZING KEYWORDS...")
    print("=" * 80)
    
    keyword_data = researcher.analyze_keywords(keywords, country)
    
    # Generate report
    report = researcher.generate_report(keyword_data, domain)
    
    # Save report
    with open("ahrefs_keyword_research_report.txt", "w", encoding="utf-8") as f:
        f.write(report)
    
    # Save JSON data
    all_data = {
        "domain": domain,
        "country": country,
        "timestamp": time.strftime('%Y-%m-%d %H:%M:%S'),
        "keywords_analyzed": len(keywords),
        "keyword_data": keyword_data
    }
    
    with open("ahrefs_keyword_research_data.json", "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=2)
    
    print("\n" + "=" * 80)
    print("✅ ANALYSIS COMPLETE!")
    print("=" * 80)
    print("\n📄 Reports saved:")
    print("   - ahrefs_keyword_research_report.txt (detailed report)")
    print("   - ahrefs_keyword_research_data.json (raw JSON data)")
    
    # Print summary
    print("\n📊 KEYWORD SUMMARY:")
    successful = sum(1 for v in keyword_data.values() if v is not None)
    print(f"   Keywords analyzed: {successful}/{len(keywords)}")
    
    if keyword_data:
        total_volume = sum(
            data.get('volume', 0) 
            for data in keyword_data.values() 
            if isinstance(data, dict)
        )
        print(f"   Total search volume: {total_volume:,}/month")

if __name__ == "__main__":
    main()
