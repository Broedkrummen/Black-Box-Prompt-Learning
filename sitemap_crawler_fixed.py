"""
Sitemap Crawler for SEO Analysis
--------------------------------
This script crawls a website's sitemap and extracts SEO-relevant information
from each page, including meta tags, headings, and content analysis.
"""

import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
from urllib.parse import urlparse
import os
from collections import Counter

class SitemapCrawler:
    def __init__(self, sitemap_url):
        self.sitemap_url = sitemap_url
        self.urls = []
        self.results = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def fetch_sitemap(self):
        """Fetch and parse the sitemap XML"""
        try:
            response = requests.get(self.sitemap_url, headers=self.headers)
            response.raise_for_status()
            
            # Parse the XML
            root = ET.fromstring(response.content)
            
            # Extract URLs from sitemap
            namespaces = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
            
            # Check if this is a sitemap index (contains other sitemaps)
            sitemap_tags = root.findall('.//ns:sitemap', namespaces)
            if sitemap_tags:
                print(f"Found sitemap index with {len(sitemap_tags)} sitemaps")
                for sitemap in sitemap_tags:
                    loc = sitemap.find('./ns:loc', namespaces)
                    if loc is not None and loc.text:
                        sub_crawler = SitemapCrawler(loc.text)
                        sub_crawler.fetch_sitemap()
                        self.urls.extend(sub_crawler.urls)
            else:
                # It's a regular sitemap with URLs
                url_tags = root.findall('.//ns:url', namespaces)
                for url in url_tags:
                    loc = url.find('./ns:loc', namespaces)
                    if loc is not None and loc.text:
                        self.urls.append(loc.text)
                
                print(f"Found {len(self.urls)} URLs in sitemap")
            
            return True
        except Exception as e:
            print(f"Error fetching sitemap: {e}")
            return False
    
    def analyze_page(self, url):
        """Analyze a single page for SEO elements"""
        try:
            print(f"Analyzing: {url}")
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Basic page info
            title = soup.title.text.strip() if soup.title else ""
            
            # Meta tags
            meta_description = ""
            meta_keywords = ""
            for meta in soup.find_all('meta'):
                if meta.get('name') == 'description':
                    meta_description = meta.get('content', '')
                elif meta.get('name') == 'keywords':
                    meta_keywords = meta.get('content', '')
            
            # Headings
            h1_tags = [h1.text.strip() for h1 in soup.find_all('h1')]
            h2_tags = [h2.text.strip() for h2 in soup.find_all('h2')]
            
            # Content analysis
            paragraphs = [p.text.strip() for p in soup.find_all('p')]
            content_text = ' '.join(paragraphs)
            word_count = len(content_text.split())
            
            # Image analysis
            images = soup.find_all('img')
            images_with_alt = sum(1 for img in images if img.get('alt'))
            images_without_alt = len(images) - images_with_alt
            
            # Link analysis
            internal_links = []
            external_links = []
            domain = urlparse(url).netloc
            
            for link in soup.find_all('a', href=True):
                href = link['href']
                if href.startswith('#') or not href:
                    continue
                    
                if domain in href or href.startswith('/'):
                    internal_links.append(href)
                else:
                    external_links.append(href)
            
            # Structured data
            structured_data = bool(soup.find_all('script', {'type': 'application/ld+json'}))
            
            # Canonical URL
            canonical = ""
            canonical_tag = soup.find('link', {'rel': 'canonical'})
            if canonical_tag:
                canonical = canonical_tag.get('href', '')
            
            # Mobile friendliness indicators
            viewport_tag = bool(soup.find('meta', {'name': 'viewport'}))
            
            # Page result
            result = {
                'url': url,
                'title': title,
                'title_length': len(title),
                'meta_description': meta_description,
                'meta_description_length': len(meta_description),
                'meta_keywords': meta_keywords,
                'h1_tags': h1_tags,
                'h1_count': len(h1_tags),
                'h2_count': len(h2_tags),
                'word_count': word_count,
                'image_count': len(images),
                'images_with_alt': images_with_alt,
                'images_without_alt': images_without_alt,
                'internal_links': len(internal_links),
                'external_links': len(external_links),
                'has_structured_data': structured_data,
                'canonical_url': canonical,
                'has_viewport_meta': viewport_tag
            }
            
            self.results.append(result)
            return result
            
        except Exception as e:
            print(f"Error analyzing {url}: {e}")
            return None
    
    def crawl(self, limit=None):
        """Crawl all URLs from the sitemap"""
        if not self.urls:
            success = self.fetch_sitemap()
            if not success:
                return False
        
        urls_to_crawl = self.urls[:limit] if limit else self.urls
        
        for url in urls_to_crawl:
            self.analyze_page(url)
            time.sleep(1)  # Be nice to the server
        
        return True
    
    def generate_report(self):
        """Generate a comprehensive SEO report"""
        if not self.results:
            print("No results to generate report from")
            return
        
        # Convert results to DataFrame
        df = pd.DataFrame(self.results)
        
        # Save raw data
        df.to_csv('seo_raw_data.csv', index=False)
        
        # Generate summary report
        with open('seo_summary_report.md', 'w', encoding='utf-8') as f:
            f.write(f"# SEO Analysis Report for {urlparse(self.sitemap_url).netloc}\n\n")
            
            f.write("## Overview\n\n")
            f.write(f"- Total pages analyzed: {len(self.results)}\n")
            f.write(f"- Average word count: {df['word_count'].mean():.1f}\n")
            f.write(f"- Average title length: {df['title_length'].mean():.1f} characters\n")
            f.write(f"- Average meta description length: {df['meta_description_length'].mean():.1f} characters\n\n")
            
            f.write("## Title Tag Analysis\n\n")
            missing_titles = df[df['title_length'] == 0].shape[0]
            short_titles = df[(df['title_length'] > 0) & (df['title_length'] < 30)].shape[0]
            good_titles = df[(df['title_length'] >= 30) & (df['title_length'] <= 60)].shape[0]
            long_titles = df[df['title_length'] > 60].shape[0]
            
            f.write(f"- Missing titles: {missing_titles} ({missing_titles/len(df)*100:.1f}%)\n")
            f.write(f"- Short titles (<30 chars): {short_titles} ({short_titles/len(df)*100:.1f}%)\n")
            f.write(f"- Optimal titles (30-60 chars): {good_titles} ({good_titles/len(df)*100:.1f}%)\n")
            f.write(f"- Long titles (>60 chars): {long_titles} ({long_titles/len(df)*100:.1f}%)\n\n")
            
            f.write("## Meta Description Analysis\n\n")
            missing_desc = df[df['meta_description_length'] == 0].shape[0]
            short_desc = df[(df['meta_description_length'] > 0) & (df['meta_description_length'] < 120)].shape[0]
            good_desc = df[(df['meta_description_length'] >= 120) & (df['meta_description_length'] <= 160)].shape[0]
            long_desc = df[df['meta_description_length'] > 160].shape[0]
            
            f.write(f"- Missing descriptions: {missing_desc} ({missing_desc/len(df)*100:.1f}%)\n")
            f.write(f"- Short descriptions (<120 chars): {short_desc} ({short_desc/len(df)*100:.1f}%)\n")
            f.write(f"- Optimal descriptions (120-160 chars): {good_desc} ({good_desc/len(df)*100:.1f}%)\n")
            f.write(f"- Long descriptions (>160 chars): {long_desc} ({long_desc/len(df)*100:.1f}%)\n\n")
            
            f.write("## Heading Structure\n\n")
            missing_h1 = df[df['h1_count'] == 0].shape[0]
            multiple_h1 = df[df['h1_count'] > 1].shape[0]
            
            f.write(f"- Pages missing H1: {missing_h1} ({missing_h1/len(df)*100:.1f}%)\n")
            f.write(f"- Pages with multiple H1s: {multiple_h1} ({multiple_h1/len(df)*100:.1f}%)\n\n")
            
            f.write("## Image Optimization\n\n")
            total_images = df['image_count'].sum()
            total_with_alt = df['images_with_alt'].sum()
            
            if total_images > 0:
                alt_percentage = total_with_alt / total_images * 100
            else:
                alt_percentage = 0
                
            f.write(f"- Total images: {total_images}\n")
            f.write(f"- Images with alt text: {total_with_alt} ({alt_percentage:.1f}%)\n")
            f.write(f"- Images missing alt text: {total_images - total_with_alt} ({100 - alt_percentage:.1f}%)\n\n")
            
            f.write("## Mobile Friendliness\n\n")
            viewport_count = df['has_viewport_meta'].sum()
            f.write(f"- Pages with viewport meta tag: {viewport_count} ({viewport_count/len(df)*100:.1f}%)\n\n")
            
            f.write("## Link Analysis\n\n")
            total_internal = df['internal_links'].sum()
            total_external = df['external_links'].sum()
            
            f.write(f"- Total internal links: {total_internal}\n")
            f.write(f"- Total external links: {total_external}\n")
            f.write(f"- Average internal links per page: {total_internal/len(df):.1f}\n")
            f.write(f"- Average external links per page: {total_external/len(df):.1f}\n\n")
            
            f.write("## Content Analysis\n\n")
            thin_content = df[df['word_count'] < 300].shape[0]
            medium_content = df[(df['word_count'] >= 300) & (df['word_count'] < 600)].shape[0]
            good_content = df[(df['word_count'] >= 600) & (df['word_count'] < 1000)].shape[0]
            excellent_content = df[df['word_count'] >= 1000].shape[0]
            
            f.write(f"- Thin content (<300 words): {thin_content} ({thin_content/len(df)*100:.1f}%)\n")
            f.write(f"- Medium content (300-599 words): {medium_content} ({medium_content/len(df)*100:.1f}%)\n")
            f.write(f"- Good content (600-999 words): {good_content} ({good_content/len(df)*100:.1f}%)\n")
            f.write(f"- Excellent content (1000+ words): {excellent_content} ({excellent_content/len(df)*100:.1f}%)\n\n")
            
            f.write("## Technical SEO\n\n")
            structured_data_count = df['has_structured_data'].sum()
            canonical_count = df[df['canonical_url'] != ''].shape[0]
            
            f.write(f"- Pages with structured data: {structured_data_count} ({structured_data_count/len(df)*100:.1f}%)\n")
            f.write(f"- Pages with canonical tags: {canonical_count} ({canonical_count/len(df)*100:.1f}%)\n\n")
            
            f.write("## Issues and Recommendations\n\n")
            
            # Title issues
            if missing_titles > 0:
                f.write("### Missing Title Tags\n\n")
                for idx, row in df[df['title_length'] == 0].iterrows():
                    f.write(f"- {row['url']}\n")
                f.write("\n")
            
            # Description issues
            if missing_desc > 0:
                f.write("### Missing Meta Descriptions\n\n")
                for idx, row in df[df['meta_description_length'] == 0].head(10).iterrows():
                    f.write(f"- {row['url']}\n")
                if missing_desc > 10:
                    f.write(f"- ... and {missing_desc - 10} more\n")
                f.write("\n")
            
            # H1 issues
            if missing_h1 > 0:
                f.write("### Missing H1 Tags\n\n")
                for idx, row in df[df['h1_count'] == 0].head(10).iterrows():
                    f.write(f"- {row['url']}\n")
                if missing_h1 > 10:
                    f.write(f"- ... and {missing_h1 - 10} more\n")
                f.write("\n")
            
            # Multiple H1 issues
            if multiple_h1 > 0:
                f.write("### Multiple H1 Tags\n\n")
                for idx, row in df[df['h1_count'] > 1].head(10).iterrows():
                    f.write(f"- {row['url']} ({row['h1_count']} H1 tags)\n")
                if multiple_h1 > 10:
                    f.write(f"- ... and {multiple_h1 - 10} more\n")
                f.write("\n")
            
            print(f"Report generated: seo_summary_report.md")
            
        return 'seo_summary_report.md'

def main():
    sitemap_url = "https://simplybeyond.dk/sitemap.xml"
    crawler = SitemapCrawler(sitemap_url)
    
    print(f"Starting crawl of {sitemap_url}")
    crawler.crawl(limit=20)  # Limit to 20 pages for demonstration
    
    print("Generating report...")
    report_path = crawler.generate_report()
    
    print(f"Analysis complete. Report saved to {report_path}")
    print("Raw data saved to seo_raw_data.csv")

if __name__ == "__main__":
    main()
