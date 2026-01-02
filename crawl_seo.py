import urllib.request
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
import re
import time

class SEOExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ""
        self.meta_description = ""
        self.meta_keywords = ""
        self.h1_tags = []
        self.in_title = False
        self.in_h1 = False

    def handle_starttag(self, tag, attrs):
        if tag == "title":
            self.in_title = True
        elif tag == "meta":
            attrs_dict = dict(attrs)
            if attrs_dict.get("name") == "description":
                self.meta_description = attrs_dict.get("content", "")
            elif attrs_dict.get("name") == "keywords":
                self.meta_keywords = attrs_dict.get("content", "")
        elif tag == "h1":
            self.in_h1 = True

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        elif tag == "h1":
            self.in_h1 = False

    def handle_data(self, data):
        if self.in_title:
            self.title += data
        elif self.in_h1:
            self.h1_tags.append(data.strip())

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
                # It's a sub-sitemap, fetch URLs from it
                print(f"Found sub-sitemap: {loc}")
                urls.extend(fetch_sitemap_urls(loc))
            else:
                # It's a page URL
                urls.append(loc)
        return urls
    except Exception as e:
        print(f"Error fetching sitemap: {e}")
        return []

def extract_seo_info(url):
    try:
        # Add delay to avoid overwhelming the server
        time.sleep(1)
        with urllib.request.urlopen(url) as response:
            html_content = response.read().decode('utf-8', errors='ignore')
        parser = SEOExtractor()
        parser.feed(html_content)
        return {
            "url": url,
            "title": parser.title,
            "meta_description": parser.meta_description,
            "meta_keywords": parser.meta_keywords,
            "h1_tags": parser.h1_tags
        }
    except Exception as e:
        print(f"Error extracting SEO info from {url}: {e}")
        return None

def main():
    sitemap_url = "https://simplybeyond.dk/sitemap.xml"
    print("Starting sitemap crawl...")
    urls = fetch_sitemap_urls(sitemap_url)
    if not urls:
        print("No URLs found in sitemap.")
        return

    print(f"Found {len(urls)} URLs to process")
    seo_data = []
    for i, url in enumerate(urls, 1):
        print(f"Processing {i}/{len(urls)}: {url}")
        info = extract_seo_info(url)
        if info:
            seo_data.append(info)

    # Save to file
    with open("seo_report.txt", "w", encoding="utf-8") as f:
        for data in seo_data:
            f.write(f"URL: {data['url']}\n")
            f.write(f"Title: {data['title']}\n")
            f.write(f"Meta Description: {data['meta_description']}\n")
            f.write(f"Meta Keywords: {data['meta_keywords']}\n")
            f.write(f"H1 Tags: {', '.join(data['h1_tags'])}\n")
            f.write("\n" + "="*50 + "\n")

    print(f"SEO report saved to seo_report.txt with {len(seo_data)} pages")

if __name__ == "__main__":
    main()
