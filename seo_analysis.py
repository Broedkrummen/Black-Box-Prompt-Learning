import urllib.request
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
import json
import csv
from collections import Counter
from urllib.parse import urljoin, urlparse

class SEOAnalyzer(HTMLParser):
    def __init__(self, base_url):
        super().__init__()
        self.base_url = base_url
        self.title = ""
        self.meta_description = ""
        self.meta_keywords = ""
        self.h1_tags = []
        self.h2_tags = []
        self.internal_links = []
        self.external_links = []
        self.images = []
        self.in_title = False
        self.in_h1 = False
        self.in_h2 = False

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        
        if tag == "title":
            self.in_title = True
        elif tag == "meta":
            if attrs_dict.get("name") == "description":
                self.meta_description = attrs_dict.get("content", "")
            elif attrs_dict.get("name") == "keywords":
                self.meta_keywords = attrs_dict.get("content", "")
        elif tag == "h1":
            self.in_h1 = True
        elif tag == "h2":
            self.in_h2 = True
        elif tag == "a":
            href = attrs_dict.get("href", "")
            if href:
                full_url = urljoin(self.base_url, href)
                parsed_base = urlparse(self.base_url)
                parsed_link = urlparse(full_url)
                
                if parsed_link.netloc == parsed_base.netloc:
                    self.internal_links.append(full_url)
                elif parsed_link.netloc:
                    self.external_links.append(full_url)
        elif tag == "img":
            src = attrs_dict.get("src", "")
            alt = attrs_dict.get("alt", "")
            if src:
                self.images.append({"src": src, "alt": alt})

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        elif tag == "h1":
            self.in_h1 = False
        elif tag == "h2":
            self.in_h2 = False

    def handle_data(self, data):
        if self.in_title:
            self.title += data
        elif self.in_h1:
            self.h1_tags.append(data.strip())
        elif self.in_h2:
            self.h2_tags.append(data.strip())

def fetch_sitemap_urls(sitemap_url):
    try:
        print(f"Fetching sitemap: {sitemap_url}")
        with urllib.request.urlopen(sitemap_url) as response:
            xml_content = response.read().decode('utf-8')
        root = ET.fromstring(xml_content)
        urls = []
        for url in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
            loc = url.text
            if '.xml' in loc:
                print(f"Found sub-sitemap: {loc}")
                urls.extend(fetch_sitemap_urls(loc))
            else:
                urls.append(loc)
        return urls
    except Exception as e:
        print(f"Error fetching sitemap: {e}")
        return []

def analyze_page(url):
    try:
        import time
        time.sleep(0.5)  # Rate limiting
        
        with urllib.request.urlopen(url) as response:
            html_content = response.read().decode('utf-8', errors='ignore')
        
        parser = SEOAnalyzer(url)
        parser.feed(html_content)
        
        return {
            "url": url,
            "title": parser.title,
            "title_length": len(parser.title),
            "meta_description": parser.meta_description,
            "meta_description_length": len(parser.meta_description),
            "meta_keywords": parser.meta_keywords,
            "h1_tags": parser.h1_tags,
            "h1_count": len(parser.h1_tags),
            "h2_tags": parser.h2_tags,
            "h2_count": len(parser.h2_tags),
            "internal_links": parser.internal_links,
            "internal_links_count": len(parser.internal_links),
            "external_links": parser.external_links,
            "external_links_count": len(parser.external_links),
            "images": parser.images,
            "images_count": len(parser.images),
            "images_without_alt": sum(1 for img in parser.images if not img["alt"])
        }
    except Exception as e:
        print(f"Error analyzing {url}: {e}")
        return None

def generate_seo_report(data):
    report = []
    report.append("=" * 80)
    report.append("SEO ANALYSIS REPORT")
    report.append("=" * 80)
    report.append("")
    
    # Overall statistics
    report.append("OVERALL STATISTICS")
    report.append("-" * 80)
    report.append(f"Total pages analyzed: {len(data)}")
    
    # Title analysis
    missing_titles = sum(1 for d in data if not d["title"])
    short_titles = sum(1 for d in data if d["title_length"] < 30)
    long_titles = sum(1 for d in data if d["title_length"] > 60)
    
    report.append(f"\nTITLE ANALYSIS:")
    report.append(f"  - Pages without title: {missing_titles}")
    report.append(f"  - Pages with short titles (<30 chars): {short_titles}")
    report.append(f"  - Pages with long titles (>60 chars): {long_titles}")
    
    # Meta description analysis
    missing_desc = sum(1 for d in data if not d["meta_description"])
    short_desc = sum(1 for d in data if d["meta_description_length"] > 0 and d["meta_description_length"] < 120)
    long_desc = sum(1 for d in data if d["meta_description_length"] > 160)
    
    report.append(f"\nMETA DESCRIPTION ANALYSIS:")
    report.append(f"  - Pages without meta description: {missing_desc}")
    report.append(f"  - Pages with short descriptions (<120 chars): {short_desc}")
    report.append(f"  - Pages with long descriptions (>160 chars): {long_desc}")
    
    # H1 analysis
    missing_h1 = sum(1 for d in data if d["h1_count"] == 0)
    multiple_h1 = sum(1 for d in data if d["h1_count"] > 1)
    
    report.append(f"\nH1 TAG ANALYSIS:")
    report.append(f"  - Pages without H1: {missing_h1}")
    report.append(f"  - Pages with multiple H1s: {multiple_h1}")
    
    # Image analysis
    total_images = sum(d["images_count"] for d in data)
    images_without_alt = sum(d["images_without_alt"] for d in data)
    
    report.append(f"\nIMAGE ANALYSIS:")
    report.append(f"  - Total images: {total_images}")
    report.append(f"  - Images without alt text: {images_without_alt}")
    
    # Link analysis
    total_internal = sum(d["internal_links_count"] for d in data)
    total_external = sum(d["external_links_count"] for d in data)
    
    report.append(f"\nLINK ANALYSIS:")
    report.append(f"  - Total internal links: {total_internal}")
    report.append(f"  - Total external links: {total_external}")
    report.append(f"  - Average internal links per page: {total_internal / len(data):.1f}")
    report.append(f"  - Average external links per page: {total_external / len(data):.1f}")
    
    # Top external domains
    all_external = []
    for d in data:
        all_external.extend(d["external_links"])
    
    external_domains = [urlparse(url).netloc for url in all_external]
    domain_counts = Counter(external_domains)
    
    report.append(f"\nTOP 10 EXTERNAL DOMAINS:")
    for domain, count in domain_counts.most_common(10):
        report.append(f"  - {domain}: {count} links")
    
    # Issues to fix
    report.append("\n" + "=" * 80)
    report.append("CRITICAL ISSUES TO FIX")
    report.append("=" * 80)
    
    if missing_titles > 0:
        report.append(f"\n⚠️  {missing_titles} pages are missing titles:")
        for d in data:
            if not d["title"]:
                report.append(f"  - {d['url']}")
    
    if missing_desc > 0:
        report.append(f"\n⚠️  {missing_desc} pages are missing meta descriptions:")
        for d in data:
            if not d["meta_description"]:
                report.append(f"  - {d['url']}")
    
    if missing_h1 > 0:
        report.append(f"\n⚠️  {missing_h1} pages are missing H1 tags:")
        for d in data:
            if d["h1_count"] == 0:
                report.append(f"  - {d['url']}")
    
    return "\n".join(report)

def main():
    sitemap_url = "https://simplybeyond.dk/sitemap.xml"
    print("Starting comprehensive SEO analysis...")
    
    urls = fetch_sitemap_urls(sitemap_url)
    if not urls:
        print("No URLs found in sitemap.")
        return
    
    print(f"Found {len(urls)} URLs to analyze")
    
    seo_data = []
    for i, url in enumerate(urls, 1):
        print(f"Analyzing {i}/{len(urls)}: {url}")
        data = analyze_page(url)
        if data:
            seo_data.append(data)
    
    # Generate text report
    report = generate_seo_report(seo_data)
    with open("seo_analysis_report.txt", "w", encoding="utf-8") as f:
        f.write(report)
    print("\n✅ SEO analysis report saved to seo_analysis_report.txt")
    
    # Save detailed data as JSON
    with open("seo_detailed_data.json", "w", encoding="utf-8") as f:
        json.dump(seo_data, f, indent=2, ensure_ascii=False)
    print("✅ Detailed SEO data saved to seo_detailed_data.json")
    
    # Save as CSV
    with open("seo_data.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "URL", "Title", "Title Length", "Meta Description", 
            "Meta Description Length", "H1 Count", "H2 Count",
            "Internal Links", "External Links", "Images", "Images Without Alt"
        ])
        for d in seo_data:
            writer.writerow([
                d["url"], d["title"], d["title_length"],
                d["meta_description"], d["meta_description_length"],
                d["h1_count"], d["h2_count"],
                d["internal_links_count"], d["external_links_count"],
                d["images_count"], d["images_without_alt"]
            ])
    print("✅ SEO data saved to seo_data.csv")
    
    # Save backlinks data
    with open("backlinks_report.txt", "w", encoding="utf-8") as f:
        f.write("BACKLINKS ANALYSIS\n")
        f.write("=" * 80 + "\n\n")
        for d in seo_data:
            f.write(f"URL: {d['url']}\n")
            f.write(f"Internal Links ({d['internal_links_count']}):\n")
            for link in d["internal_links"][:10]:  # Show first 10
                f.write(f"  - {link}\n")
            if d['internal_links_count'] > 10:
                f.write(f"  ... and {d['internal_links_count'] - 10} more\n")
            
            f.write(f"\nExternal Links ({d['external_links_count']}):\n")
            for link in d["external_links"][:10]:  # Show first 10
                f.write(f"  - {link}\n")
            if d['external_links_count'] > 10:
                f.write(f"  ... and {d['external_links_count'] - 10} more\n")
            f.write("\n" + "-" * 80 + "\n\n")
    print("✅ Backlinks report saved to backlinks_report.txt")
    
    print(f"\n🎉 Analysis complete! Analyzed {len(seo_data)} pages")

if __name__ == "__main__":
    main()
