"""
SEO Analysis Dashboard - Tkinter Version
Desktop GUI application for SEO analysis
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import http.client
import json
import time
import hashlib
import hmac
import base64
from urllib.parse import quote
import xml.etree.ElementTree as ET
import threading

# API Configuration
RAPIDAPI_KEY = "5c359bb774msh32eed0a33c585c4p1466d6jsn5620b810b2f7"
MOZ_ACCESS_ID = "mozscape-c7fe158e8e"
MOZ_SECRET_KEY = "e0c2a5e8e0e44f5e8c7fe158e8e0c2a5"

class SEODashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("SEO Analysis Dashboard")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # Variables
        self.domain_var = tk.StringVar()
        self.location_var = tk.StringVar(value="DK")
        self.language_var = tk.StringVar(value="da")
        self.analyzing = False
        
        self.create_widgets()
    
    def create_widgets(self):
        # Header
        header_frame = tk.Frame(self.root, bg='#1f77b4', height=100)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="🔍 SEO Analysis Dashboard",
            font=('Arial', 24, 'bold'),
            bg='#1f77b4',
            fg='white'
        )
        title_label.pack(pady=20)
        
        subtitle_label = tk.Label(
            header_frame,
            text="Comprehensive SEO & Backlink Analysis Tool",
            font=('Arial', 12),
            bg='#1f77b4',
            fg='white'
        )
        subtitle_label.pack()
        
        # Input Frame
        input_frame = tk.Frame(self.root, bg='white', padx=20, pady=20)
        input_frame.pack(fill='x', padx=20, pady=20)
        
        # Domain Input
        tk.Label(input_frame, text="🌐 Domain:", font=('Arial', 10, 'bold'), bg='white').grid(row=0, column=0, sticky='w', padx=5, pady=5)
        domain_entry = tk.Entry(input_frame, textvariable=self.domain_var, width=30, font=('Arial', 10))
        domain_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Location Dropdown
        tk.Label(input_frame, text="📍 Location:", font=('Arial', 10, 'bold'), bg='white').grid(row=0, column=2, sticky='w', padx=5, pady=5)
        location_combo = ttk.Combobox(
            input_frame,
            textvariable=self.location_var,
            values=['DK', 'US', 'GB', 'DE', 'SE', 'NO'],
            width=10,
            state='readonly'
        )
        location_combo.grid(row=0, column=3, padx=5, pady=5)
        
        # Language Dropdown
        tk.Label(input_frame, text="🗣️ Language:", font=('Arial', 10, 'bold'), bg='white').grid(row=0, column=4, sticky='w', padx=5, pady=5)
        language_combo = ttk.Combobox(
            input_frame,
            textvariable=self.language_var,
            values=['da', 'en', 'de', 'sv', 'no'],
            width=10,
            state='readonly'
        )
        language_combo.grid(row=0, column=5, padx=5, pady=5)
        
        # Analyze Button
        self.analyze_btn = tk.Button(
            input_frame,
            text="🔍 Analyze",
            command=self.start_analysis,
            bg='#1f77b4',
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=20,
            pady=5,
            cursor='hand2'
        )
        self.analyze_btn.grid(row=0, column=6, padx=10, pady=5)
        
        # Progress Bar
        self.progress = ttk.Progressbar(input_frame, length=400, mode='indeterminate')
        self.progress.grid(row=1, column=0, columnspan=7, pady=10)
        
        # Status Label
        self.status_label = tk.Label(input_frame, text="", font=('Arial', 9), bg='white', fg='#666')
        self.status_label.grid(row=2, column=0, columnspan=7)
        
        # Results Frame
        results_frame = tk.Frame(self.root, bg='#f0f0f0')
        results_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Metrics Frame
        metrics_frame = tk.Frame(results_frame, bg='#f0f0f0')
        metrics_frame.pack(fill='x', pady=10)
        
        # Metric Cards
        self.da_card = self.create_metric_card(metrics_frame, "Domain Authority", "N/A")
        self.da_card.pack(side='left', padx=5, fill='both', expand=True)
        
        self.dr_card = self.create_metric_card(metrics_frame, "Domain Rating", "N/A")
        self.dr_card.pack(side='left', padx=5, fill='both', expand=True)
        
        self.visits_card = self.create_metric_card(metrics_frame, "Monthly Visits", "N/A")
        self.visits_card.pack(side='left', padx=5, fill='both', expand=True)
        
        self.pages_card = self.create_metric_card(metrics_frame, "Pages Indexed", "N/A")
        self.pages_card.pack(side='left', padx=5, fill='both', expand=True)
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(results_frame)
        self.notebook.pack(fill='both', expand=True, pady=10)
        
        # Overview Tab
        overview_tab = tk.Frame(self.notebook, bg='white')
        self.notebook.add(overview_tab, text='📊 Overview')
        
        self.overview_text = scrolledtext.ScrolledText(
            overview_tab,
            wrap=tk.WORD,
            width=100,
            height=20,
            font=('Courier', 9)
        )
        self.overview_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Backlinks Tab
        backlinks_tab = tk.Frame(self.notebook, bg='white')
        self.notebook.add(backlinks_tab, text='🔗 Backlinks')
        
        self.backlinks_text = scrolledtext.ScrolledText(
            backlinks_tab,
            wrap=tk.WORD,
            width=100,
            height=20,
            font=('Courier', 9)
        )
        self.backlinks_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Keywords Tab
        keywords_tab = tk.Frame(self.notebook, bg='white')
        self.notebook.add(keywords_tab, text='🔑 Keywords')
        
        self.keywords_text = scrolledtext.ScrolledText(
            keywords_tab,
            wrap=tk.WORD,
            width=100,
            height=20,
            font=('Courier', 9)
        )
        self.keywords_text.pack(fill='both', expand=True, padx=10, pady=10)
    
    def create_metric_card(self, parent, title, value):
        card = tk.Frame(parent, bg='#1f77b4', relief='raised', borderwidth=2)
        
        value_label = tk.Label(
            card,
            text=value,
            font=('Arial', 24, 'bold'),
            bg='#1f77b4',
            fg='white'
        )
        value_label.pack(pady=(20, 5))
        
        title_label = tk.Label(
            card,
            text=title,
            font=('Arial', 10),
            bg='#1f77b4',
            fg='white'
        )
        title_label.pack(pady=(0, 20))
        
        card.value_label = value_label
        return card
    
    def update_metric_card(self, card, value):
        card.value_label.config(text=str(value))
    
    def start_analysis(self):
        domain = self.domain_var.get().strip()
        
        if not domain:
            messagebox.showwarning("Input Required", "Please enter a domain")
            return
        
        if self.analyzing:
            messagebox.showinfo("Analysis in Progress", "Please wait for the current analysis to complete")
            return
        
        # Clean domain
        domain = domain.replace("https://", "").replace("http://", "").replace("www.", "").rstrip("/")
        
        # Start analysis in separate thread
        self.analyzing = True
        self.analyze_btn.config(state='disabled')
        self.progress.start()
        self.status_label.config(text="Starting analysis...")
        
        thread = threading.Thread(target=self.run_analysis, args=(domain,))
        thread.daemon = True
        thread.start()
    
    def run_analysis(self, domain):
        try:
            location = self.location_var.get()
            language = self.language_var.get()
            
            results = {}
            
            # Sitemap
            self.update_status("🔍 Crawling sitemap...")
            results['sitemap'] = self.crawl_sitemap(domain)
            time.sleep(0.5)
            
            # Moz
            self.update_status("📊 Analyzing with Moz...")
            results['moz'] = self.analyze_moz(domain)
            time.sleep(1)
            
            # Ahrefs
            self.update_status("📊 Analyzing with Ahrefs...")
            results['ahrefs'] = self.analyze_ahrefs(domain)
            time.sleep(1)
            
            # SimilarWeb
            self.update_status("📊 Analyzing with SimilarWeb...")
            results['similarweb'] = self.analyze_similarweb(domain)
            time.sleep(1)
            
            # SEO API
            self.update_status("📊 Analyzing backlinks...")
            results['seo_api'] = self.analyze_seo_api(domain, location)
            time.sleep(1)
            
            # Google Keywords
            self.update_status("📊 Analyzing keywords...")
            results['google'] = self.analyze_google_keywords(domain, location, language)
            
            # Update UI
            self.root.after(0, self.display_results, results)
            
        except Exception as e:
            self.root.after(0, messagebox.showerror, "Error", f"Analysis failed: {str(e)}")
        finally:
            self.root.after(0, self.finish_analysis)
    
    def update_status(self, message):
        self.root.after(0, self.status_label.config, {'text': message})
    
    def finish_analysis(self):
        self.analyzing = False
        self.analyze_btn.config(state='normal')
        self.progress.stop()
        self.status_label.config(text="✅ Analysis complete!")
    
    def display_results(self, results):
        # Update metric cards
        if results['moz']['success']:
            self.update_metric_card(self.da_card, results['moz']['data'].get('domain_authority', 'N/A'))
        
        if results['ahrefs']['success']:
            self.update_metric_card(self.dr_card, results['ahrefs']['data'].get('domainRating', 'N/A'))
        
        if results['similarweb']['success'] and results['similarweb']['data'].get('visits'):
            visits = list(results['similarweb']['data']['visits'].values())[-1]
            self.update_metric_card(self.visits_card, f"{visits:,}")
        
        if results['sitemap']['success']:
            self.update_metric_card(self.pages_card, results['sitemap']['pages'])
        
        # Update overview
        self.overview_text.delete('1.0', tk.END)
        overview = f"""
ANALYSIS RESULTS
{'=' * 80}

AUTHORITY METRICS:
  Domain Authority (Moz): {results['moz']['data'].get('domain_authority', 'N/A') if results['moz']['success'] else 'N/A'}
  Domain Rating (Ahrefs): {results['ahrefs']['data'].get('domainRating', 'N/A') if results['ahrefs']['success'] else 'N/A'}
  Ahrefs Rank: {results['ahrefs']['data'].get('ahRank', 'N/A') if results['ahrefs']['success'] else 'N/A'}

BACKLINK PROFILE:
"""
        if results['seo_api']['success']:
            overview += f"""  Total Backlinks: {results['seo_api']['data'].get('overview', {}).get('backlinks', 0):,}
  Referring Domains: {results['seo_api']['data'].get('overview', {}).get('referringDomains', 0):,}
  Dofollow: {results['seo_api']['data'].get('overview', {}).get('dofollowBacklinks', {}).get('percentage', 0)}%
"""
        
        overview += f"""
TRAFFIC:
"""
        if results['similarweb']['success'] and results['similarweb']['data'].get('visits'):
            for month, count in list(results['similarweb']['data']['visits'].items())[-3:]:
                overview += f"  {month}: {count:,} visits\n"
        
        overview += f"""
TECHNICAL:
  Pages Indexed: {results['sitemap']['pages'] if results['sitemap']['success'] else 'N/A'}
"""
        
        self.overview_text.insert('1.0', overview)
        
        # Update backlinks
        self.backlinks_text.delete('1.0', tk.END)
        if results['seo_api']['success'] and results['seo_api']['data'].get('backlinks'):
            backlinks_text = "TOP BACKLINKS\n" + "=" * 80 + "\n\n"
            for i, bl in enumerate(results['seo_api']['data']['backlinks'][:20], 1):
                backlinks_text += f"{i}. {bl.get('anchor', 'N/A')[:50]}\n"
                backlinks_text += f"   DR: {bl.get('domainRating', 0)}\n"
                backlinks_text += f"   From: {bl.get('urlFrom', 'N/A')[:70]}\n"
                backlinks_text += f"   To: {bl.get('urlTo', 'N/A')[:70]}\n\n"
            self.backlinks_text.insert('1.0', backlinks_text)
        
        # Update keywords
        self.keywords_text.delete('1.0', tk.END)
        if results['google']['success'] and results['google']['data']:
            keywords_text = "TOP KEYWORDS\n" + "=" * 80 + "\n\n"
            for i, kw in enumerate(results['google']['data'][:30], 1):
                keywords_text += f"{i}. {kw.get('text', 'N/A')}\n"
                keywords_text += f"   Volume: {kw.get('volume', 0):,}\n"
                keywords_text += f"   Competition: {kw.get('competition_level', 'N/A')}\n"
                keywords_text += f"   CPC: ${kw.get('low_bid', 0):.2f} - ${kw.get('high_bid', 0):.2f}\n\n"
            self.keywords_text.insert('1.0', keywords_text)
    
    # Analysis functions (same as other versions)
    def crawl_sitemap(self, domain):
        try:
            import urllib.request
            sitemap_url = f"https://{domain}/sitemap.xml"
            
            with urllib.request.urlopen(sitemap_url, timeout=10) as response:
                xml_content = response.read().decode('utf-8')
            
            root = ET.fromstring(xml_content)
            urls = []
            
            for url in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
                loc = url.text
                if not loc.endswith('.xml'):
                    urls.append(loc)
            
            return {"success": True, "pages": len(urls)}
        except Exception as e:
            return {"success": False, "error": str(e), "pages": 0}
    
    def analyze_moz(self, domain):
        try:
            expires = int(time.time()) + 300
            string_to_sign = f"{MOZ_ACCESS_ID}\n{expires}"
            binary_signature = hmac.new(
                MOZ_SECRET_KEY.encode('utf-8'),
                string_to_sign.encode('utf-8'),
                hashlib.sha1
            ).digest()
            signature = base64.b64encode(binary_signature).decode('utf-8')
            
            conn = http.client.HTTPSConnection("lsapi.seomoz.com")
            url = f"/v2/url_metrics/{quote(domain, safe='')}?AccessID={MOZ_ACCESS_ID}&Expires={expires}&Signature={quote(signature)}"
            
            conn.request("GET", url)
            res = conn.getresponse()
            data = json.loads(res.read().decode("utf-8"))
            
            if "domain_authority" in data:
                return {"success": True, "data": data}
            else:
                return {"success": False, "error": data}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def analyze_ahrefs(self, domain):
        try:
            conn = http.client.HTTPSConnection("ahrefs-domain-research.p.rapidapi.com")
            headers = {
                'x-rapidapi-key': RAPIDAPI_KEY,
                'x-rapidapi-host': "ahrefs-domain-research.p.rapidapi.com"
            }
            
            conn.request("GET", f"/domain-rating/?domain={domain}", headers=headers)
            res = conn.getresponse()
            data = json.loads(res.read().decode("utf-8"))
            
            if "domainRating" in data:
                return {"success": True, "data": data}
            else:
                return {"success": False, "error": data}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def analyze_similarweb(self, domain):
        try:
            conn = http.client.HTTPSConnection("similarweb-insights.p.rapidapi.com")
            headers = {
                'x-rapidapi-key': RAPIDAPI_KEY,
                'x-rapidapi-host': "similarweb-insights.p.rapidapi.com"
            }
            
            conn.request("GET", f"/traffic/?domain={domain}", headers=headers)
            res = conn.getresponse()
            data = json.loads(res.read().decode("utf-8"))
            
            if "visits" in data:
                return {"success": True, "data": data}
            else:
                return {"success": False, "error": data}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def analyze_seo_api(self, domain, location):
        try:
            conn = http.client.HTTPSConnection("seo-api-dr-rd-rank-keywords-backlinks1.p.rapidapi.com")
            headers = {
                'x-rapidapi-key': RAPIDAPI_KEY,
                'x-rapidapi-host': "seo-api-dr-rd-rank-keywords-backlinks1.p.rapidapi.com"
            }
            
            conn.request("GET", f"/backlinks/?domain={domain}&country={location.lower()}", headers=headers)
            res = conn.getresponse()
            data = json.loads(res.read().decode("utf-8"))
            
            if "overview" in data:
                return {"success": True, "data": data}
            else:
                return {"success": False, "error": data}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def analyze_google_keywords(self, domain, location, language):
        try:
            conn = http.client.HTTPSConnection("google-keyword-insight1.p.rapidapi.com")
            headers = {
                'x-rapidapi-key': RAPIDAPI_KEY,
                'x-rapidapi-host': "google-keyword-insight1.p.rapidapi.com"
            }
            
            conn.request("GET", f"/urlkeysuggest/?url={domain}&location={location}&lang={language}", headers=headers)
            res = conn.getresponse()
            data = json.loads(res.read().decode("utf-8"))
            
            if isinstance(data, list):
                return {"success": True, "data": data}
            else:
                return {"success": False, "error": data}
        except Exception as e:
            return {"success": False, "error": str(e)}

if __name__ == '__main__':
    root = tk.Tk()
    app = SEODashboard(root)
    root.mainloop()
