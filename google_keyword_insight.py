import http.client
import json
import time
from urllib.parse import quote

def google_keyword_insight_analysis():
    """
    Comprehensive Google Keyword Insight analysis for simplybeyond.dk
    Using Danish location (DK) and language (da)
    """
    
    conn = http.client.HTTPSConnection("google-keyword-insight1.p.rapidapi.com")
    
    headers = {
        'x-rapidapi-key': "5c359bb774msh32eed0a33c585c4p1466d6jsn5620b810b2f7",
        'x-rapidapi-host': "google-keyword-insight1.p.rapidapi.com"
    }
    
    results = {
        "domain": "simplybeyond.dk",
        "location": "DK",
        "language": "da",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "analyses": {}
    }
    
    # Keywords to analyze (Danish silk-related keywords)
    keywords = [
        "silke pudebetræk",
        "silke sovemaske",
        "silke bonnet",
        "heatless curls",
        "silke",
        "mulberry silke",
        "silke sengetøj"
    ]
    
    print("=" * 80)
    print("GOOGLE KEYWORD INSIGHT ANALYSIS")
    print("Domain: simplybeyond.dk")
    print("Location: Denmark (DK)")
    print("Language: Danish (da)")
    print("=" * 80)
    print()
    
    # 1. Keyword Suggestions for each keyword
    print("📊 ANALYZING KEYWORD SUGGESTIONS...")
    print("-" * 80)
    
    for keyword in keywords:
        print(f"\n🔍 Analyzing: {keyword}")
        try:
            encoded_keyword = quote(keyword)
            conn.request("GET", f"/keysuggest/?keyword={encoded_keyword}&location=DK&lang=da", headers=headers)
            res = conn.getresponse()
            data = res.read()
            
            if res.status == 200:
                keyword_data = json.loads(data.decode("utf-8"))
                results["analyses"][f"keyword_suggestions_{keyword}"] = keyword_data
                
                # Display summary
                if isinstance(keyword_data, dict) and "suggestions" in keyword_data:
                    print(f"   ✅ Found {len(keyword_data.get('suggestions', []))} suggestions")
                elif isinstance(keyword_data, list):
                    print(f"   ✅ Found {len(keyword_data)} suggestions")
                else:
                    print(f"   ✅ Data received: {len(str(keyword_data))} bytes")
            else:
                print(f"   ❌ Error: Status {res.status}")
                results["analyses"][f"keyword_suggestions_{keyword}"] = {"error": f"Status {res.status}"}
            
            time.sleep(1)  # Rate limiting
            
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            results["analyses"][f"keyword_suggestions_{keyword}"] = {"error": str(e)}
    
    # 2. URL Keyword Suggestions
    print("\n\n📊 ANALYZING URL KEYWORDS...")
    print("-" * 80)
    print("\n🔍 Analyzing: simplybeyond.dk")
    
    try:
        conn.request("GET", "/urlkeysuggest/?url=simplybeyond.dk&location=DK&lang=da", headers=headers)
        res = conn.getresponse()
        data = res.read()
        
        if res.status == 200:
            url_data = json.loads(data.decode("utf-8"))
            results["analyses"]["url_keywords"] = url_data
            
            if isinstance(url_data, dict) and "keywords" in url_data:
                print(f"   ✅ Found {len(url_data.get('keywords', []))} keywords")
            elif isinstance(url_data, list):
                print(f"   ✅ Found {len(url_data)} keywords")
            else:
                print(f"   ✅ Data received: {len(str(url_data))} bytes")
        else:
            print(f"   ❌ Error: Status {res.status}")
            results["analyses"]["url_keywords"] = {"error": f"Status {res.status}"}
        
        time.sleep(1)
        
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        results["analyses"]["url_keywords"] = {"error": str(e)}
    
    # 3. Global Keyword Data
    print("\n\n📊 ANALYZING GLOBAL KEYWORD DATA...")
    print("-" * 80)
    
    for keyword in keywords[:3]:  # Analyze top 3 keywords globally
        print(f"\n🌍 Global analysis: {keyword}")
        try:
            encoded_keyword = quote(keyword)
            conn.request("GET", f"/globalkey/?keyword={encoded_keyword}&lang=da", headers=headers)
            res = conn.getresponse()
            data = res.read()
            
            if res.status == 200:
                global_data = json.loads(data.decode("utf-8"))
                results["analyses"][f"global_keyword_{keyword}"] = global_data
                print(f"   ✅ Global data received: {len(str(global_data))} bytes")
            else:
                print(f"   ❌ Error: Status {res.status}")
                results["analyses"][f"global_keyword_{keyword}"] = {"error": f"Status {res.status}"}
            
            time.sleep(1)
            
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            results["analyses"][f"global_keyword_{keyword}"] = {"error": str(e)}
    
    # 4. Global URL Data
    print("\n\n📊 ANALYZING GLOBAL URL DATA...")
    print("-" * 80)
    print("\n🌍 Global analysis: simplybeyond.dk")
    
    try:
        conn.request("GET", "/globalurl/?url=simplybeyond.dk&lang=da", headers=headers)
        res = conn.getresponse()
        data = res.read()
        
        if res.status == 200:
            global_url_data = json.loads(data.decode("utf-8"))
            results["analyses"]["global_url"] = global_url_data
            print(f"   ✅ Global URL data received: {len(str(global_url_data))} bytes")
        else:
            print(f"   ❌ Error: Status {res.status}")
            results["analyses"]["global_url"] = {"error": f"Status {res.status}"}
        
        time.sleep(1)
        
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        results["analyses"]["global_url"] = {"error": str(e)}
    
    # 5. Top Keywords
    print("\n\n📊 ANALYZING TOP KEYWORDS...")
    print("-" * 80)
    
    for keyword in keywords[:3]:  # Analyze top 3 keywords
        print(f"\n🔝 Top keywords for: {keyword}")
        try:
            encoded_keyword = quote(keyword)
            conn.request("GET", f"/topkeys/?keyword={encoded_keyword}&location=DK&lang=da", headers=headers)
            res = conn.getresponse()
            data = res.read()
            
            if res.status == 200:
                top_data = json.loads(data.decode("utf-8"))
                results["analyses"][f"top_keywords_{keyword}"] = top_data
                
                if isinstance(top_data, dict) and "keywords" in top_data:
                    print(f"   ✅ Found {len(top_data.get('keywords', []))} top keywords")
                elif isinstance(top_data, list):
                    print(f"   ✅ Found {len(top_data)} top keywords")
                else:
                    print(f"   ✅ Data received: {len(str(top_data))} bytes")
            else:
                print(f"   ❌ Error: Status {res.status}")
                results["analyses"][f"top_keywords_{keyword}"] = {"error": f"Status {res.status}"}
            
            time.sleep(1)
            
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            results["analyses"][f"top_keywords_{keyword}"] = {"error": str(e)}
    
    # 6. Get Available Locations
    print("\n\n📊 FETCHING AVAILABLE LOCATIONS...")
    print("-" * 80)
    
    try:
        conn.request("GET", "/locations/", headers=headers)
        res = conn.getresponse()
        data = res.read()
        
        if res.status == 200:
            locations_data = json.loads(data.decode("utf-8"))
            results["analyses"]["available_locations"] = locations_data
            
            if isinstance(locations_data, list):
                print(f"   ✅ Found {len(locations_data)} available locations")
            else:
                print(f"   ✅ Locations data received: {len(str(locations_data))} bytes")
        else:
            print(f"   ❌ Error: Status {res.status}")
            results["analyses"]["available_locations"] = {"error": f"Status {res.status}"}
        
        time.sleep(1)
        
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        results["analyses"]["available_locations"] = {"error": str(e)}
    
    # 7. Get Available Languages
    print("\n\n📊 FETCHING AVAILABLE LANGUAGES...")
    print("-" * 80)
    
    try:
        conn.request("GET", "/languages/", headers=headers)
        res = conn.getresponse()
        data = res.read()
        
        if res.status == 200:
            languages_data = json.loads(data.decode("utf-8"))
            results["analyses"]["available_languages"] = languages_data
            
            if isinstance(languages_data, list):
                print(f"   ✅ Found {len(languages_data)} available languages")
            else:
                print(f"   ✅ Languages data received: {len(str(languages_data))} bytes")
        else:
            print(f"   ❌ Error: Status {res.status}")
            results["analyses"]["available_languages"] = {"error": f"Status {res.status}"}
        
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        results["analyses"]["available_languages"] = {"error": str(e)}
    
    # Save results
    print("\n\n" + "=" * 80)
    print("💾 SAVING RESULTS...")
    print("=" * 80)
    
    # Save JSON
    with open("google_keyword_insight_data.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print("   ✅ Saved: google_keyword_insight_data.json")
    
    # Save detailed report
    with open("google_keyword_insight_report.txt", "w", encoding="utf-8") as f:
        f.write("=" * 80 + "\n")
        f.write("GOOGLE KEYWORD INSIGHT ANALYSIS REPORT\n")
        f.write("Domain: simplybeyond.dk\n")
        f.write("Location: Denmark (DK)\n")
        f.write("Language: Danish (da)\n")
        f.write(f"Generated: {results['timestamp']}\n")
        f.write("=" * 80 + "\n\n")
        
        # Summary
        f.write("ANALYSIS SUMMARY\n")
        f.write("-" * 80 + "\n")
        f.write(f"Total Analyses Performed: {len(results['analyses'])}\n")
        
        successful = sum(1 for v in results['analyses'].values() if not isinstance(v, dict) or 'error' not in v)
        failed = len(results['analyses']) - successful
        
        f.write(f"Successful: {successful}\n")
        f.write(f"Failed: {failed}\n\n")
        
        # Keywords analyzed
        f.write("KEYWORDS ANALYZED\n")
        f.write("-" * 80 + "\n")
        for i, keyword in enumerate(keywords, 1):
            f.write(f"{i}. {keyword}\n")
        f.write("\n")
        
        # Detailed results
        f.write("DETAILED RESULTS\n")
        f.write("-" * 80 + "\n\n")
        
        for analysis_name, analysis_data in results['analyses'].items():
            f.write(f"\n{'=' * 80}\n")
            f.write(f"Analysis: {analysis_name}\n")
            f.write(f"{'=' * 80}\n\n")
            
            if isinstance(analysis_data, dict) and 'error' in analysis_data:
                f.write(f"❌ Error: {analysis_data['error']}\n")
            else:
                f.write(json.dumps(analysis_data, indent=2, ensure_ascii=False))
                f.write("\n")
    
    print("   ✅ Saved: google_keyword_insight_report.txt")
    
    print("\n" + "=" * 80)
    print("✅ ANALYSIS COMPLETE!")
    print("=" * 80)
    print(f"\n📊 Total Analyses: {len(results['analyses'])}")
    print(f"✅ Successful: {successful}")
    print(f"❌ Failed: {failed}")
    print("\n📄 Reports saved:")
    print("   - google_keyword_insight_data.json")
    print("   - google_keyword_insight_report.txt")
    print()

if __name__ == "__main__":
    google_keyword_insight_analysis()
