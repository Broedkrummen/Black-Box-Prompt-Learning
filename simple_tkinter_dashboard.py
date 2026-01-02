ot """
Simple Tkinter SEO Dashboard
----------------------------
A desktop application for SEO analysis using Tkinter
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import webbrowser
import os
import pandas as pd
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class SimpleSEODashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("🔍 Simple SEO Dashboard")
        self.root.geometry("800x600")
        self.root.minsize(800, 600)
        
        # Set up the main frame
        self.main_frame = ttk.Frame(root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create header
        self.create_header()
        
        # Create input form
        self.create_form()
        
        # Create tabs for results
        self.create_tabs()
        
        # Create status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_bar = ttk.Label(root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Sample data for demonstration
        self.sample_data = {
            'domain_authority': 42,
            'domain_rating': 38,
            'monthly_visits': 12500,
            'pages_indexed': 158,
            'backlinks': 1250,
            'keywords': [
                {'keyword': 'example keyword 1', 'volume': 1500, 'position': 3},
                {'keyword': 'example keyword 2', 'volume': 800, 'position': 8},
                {'keyword': 'example keyword 3', 'volume': 2200, 'position': 12},
                {'keyword': 'example keyword 4', 'volume': 1100, 'position': 5},
                {'keyword': 'example keyword 5', 'volume': 950, 'position': 15}
            ],
            'traffic_data': {
                'months': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                'visits': [8500, 9200, 10500, 11800, 12500, 12300]
            }
        }
    
    def create_header(self):
        """Create the dashboard header"""
        header_frame = ttk.Frame(self.main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = ttk.Label(header_frame, text="🔍 Simple SEO Dashboard", font=("Arial", 18, "bold"))
        title_label.pack(pady=(0, 5))
        
        subtitle_label = ttk.Label(header_frame, text="A desktop application for SEO analysis")
        subtitle_label.pack()
    
    def create_form(self):
        """Create the input form"""
        form_frame = ttk.LabelFrame(self.main_frame, text="Enter Domain to Analyze")
        form_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Domain input
        domain_frame = ttk.Frame(form_frame)
        domain_frame.pack(fill=tk.X, padx=10, pady=10)
        
        domain_label = ttk.Label(domain_frame, text="Domain:")
        domain_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.domain_var = tk.StringVar()
        self.domain_entry = ttk.Entry(domain_frame, textvariable=self.domain_var, width=40)
        self.domain_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.domain_var.set("simplybeyond.dk")  # Default value
        
        # Location and language
        options_frame = ttk.Frame(form_frame)
        options_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # Location
        location_label = ttk.Label(options_frame, text="Location:")
        location_label.grid(row=0, column=0, padx=(0, 10), sticky=tk.W)
        
        self.location_var = tk.StringVar()
        location_combo = ttk.Combobox(options_frame, textvariable=self.location_var, width=15)
        location_combo['values'] = ('DK', 'US', 'GB', 'DE', 'SE', 'NO')
        location_combo.current(0)
        location_combo.grid(row=0, column=1, padx=(0, 20), sticky=tk.W)
        
        # Language
        language_label = ttk.Label(options_frame, text="Language:")
        language_label.grid(row=0, column=2, padx=(0, 10), sticky=tk.W)
        
        self.language_var = tk.StringVar()
        language_combo = ttk.Combobox(options_frame, textvariable=self.language_var, width=15)
        language_combo['values'] = ('da', 'en', 'de', 'sv', 'no')
        language_combo.current(0)
        language_combo.grid(row=0, column=3, sticky=tk.W)
        
        # Analyze button
        button_frame = ttk.Frame(form_frame)
        button_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        analyze_button = ttk.Button(button_frame, text="Analyze", command=self.analyze_domain)
        analyze_button.pack(side=tk.RIGHT)
    
    def create_tabs(self):
        """Create tabs for results"""
        self.tab_control = ttk.Notebook(self.main_frame)
        self.tab_control.pack(fill=tk.BOTH, expand=True)
        
        # Overview tab
        self.overview_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.overview_tab, text="Overview")
        
        # Keywords tab
        self.keywords_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.keywords_tab, text="Keywords")
        
        # Traffic tab
        self.traffic_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.traffic_tab, text="Traffic")
        
        # Technical tab
        self.technical_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.technical_tab, text="Technical SEO")
        
        # Initialize tabs with empty content
        self.initialize_tabs()
    
    def initialize_tabs(self):
        """Initialize tabs with empty content"""
        # Overview tab
        overview_label = ttk.Label(self.overview_tab, text="Enter a domain and click 'Analyze' to see results")
        overview_label.pack(pady=50)
        
        # Keywords tab
        keywords_label = ttk.Label(self.keywords_tab, text="Keyword data will appear here")
        keywords_label.pack(pady=50)
        
        # Traffic tab
        traffic_label = ttk.Label(self.traffic_tab, text="Traffic data will appear here")
        traffic_label.pack(pady=50)
        
        # Technical tab
        technical_label = ttk.Label(self.technical_tab, text="Technical SEO data will appear here")
        technical_label.pack(pady=50)
    
    def analyze_domain(self):
        """Analyze the domain"""
        domain = self.domain_var.get().strip()
        
        if not domain:
            messagebox.showerror("Error", "Please enter a domain")
            return
        
        # Update status
        self.status_var.set(f"Analyzing {domain}...")
        
        # Start analysis in a separate thread
        threading.Thread(target=self.perform_analysis, args=(domain,)).start()
    
    def perform_analysis(self, domain):
        """Perform the analysis using selected data sources"""
        try:
            # Import required modules
            import http.client
            import json
            import time
            import hashlib
            import hmac
            import base64
            from urllib.parse import quote
            import xml.etree.ElementTree as ET

            # API Configuration
            RAPIDAPI_KEY = "5c359bb774msh32eed0a33c585c4p1466d6jsn5620b810b2f7"
            MOZ_ACCESS_ID = "mozscape-c7fe158e8e"
            MOZ_SECRET_KEY = "e0c2a5e8e0e44f5e8c7fe158e8e0c2a5"

            results = {}

            # Sitemap analysis
            if self.use_sitemap.get():
                self.root.after(0, lambda: self.status_var.set("🔍 Crawling sitemap..."))
                results['sitemap'] = self.crawl_sitemap(domain)
                time.sleep(0.5)

            # Moz analysis
            if self.use_moz.get():
                self.root.after(0, lambda: self.status_var.set("📊 Analyzing with Moz..."))
                results['moz'] = self.analyze_moz(domain)
                time.sleep(1)

            # Ahrefs analysis
            if self.use_ahrefs.get():
                self.root.after(0, lambda: self.status_var.set("📊 Analyzing with Ahrefs..."))
                results['ahrefs'] = self.analyze_ahrefs(domain)
                time.sleep(1)

            # SimilarWeb analysis
            if self.use_similarweb.get():
                self.root.after(0, lambda: self.status_var.set("📊 Analyzing with SimilarWeb..."))
                results['similarweb'] = self.analyze_similarweb(domain)
                time.sleep(1)

            # SEO API analysis
            if self.use_seo_api.get():
                self.root.after(0, lambda: self.status_var.set("📊 Analyzing backlinks..."))
                results['seo_api'] = self.analyze_seo_api(domain, self.location_var.get())
                time.sleep(1)

            # Google Keywords analysis
            if self.use_google.get():
                self.root.after(0, lambda: self.status_var.set("📊 Analyzing keywords..."))
                results['google'] = self.analyze_google_keywords(domain, self.location_var.get(), self.language_var.get())

            # Store results and update UI
            self.analysis_results = results
            self.root.after(0, self.update_results, domain)

        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Analysis failed: {str(e)}"))
            self.root.after(0, lambda: self.status_var.set("Analysis failed"))
    
    def update_results(self, domain):
        """Update the UI with results"""
        # Clear existing content
        for widget in self.overview_tab.winfo_children():
            widget.destroy()
        
        for widget in self.keywords_tab.winfo_children():
            widget.destroy()
        
        for widget in self.traffic_tab.winfo_children():
            widget.destroy()
        
        for widget in self.technical_tab.winfo_children():
            widget.destroy()
        
        # Update overview tab
        self.update_overview_tab(domain)
        
        # Update keywords tab
        self.update_keywords_tab()
        
        # Update traffic tab
        self.update_traffic_tab()
        
        # Update technical tab
        self.update_technical_tab(domain)
        
        # Update status
        self.status_var.set(f"Analysis complete for {domain}")
    
    def update_overview_tab(self, domain):
        """Update the overview tab with results"""
        # Create a frame for metrics
        metrics_frame = ttk.LabelFrame(self.overview_tab, text="Key Metrics")
        metrics_frame.pack(fill=tk.X, padx=10, pady=10)

        # Get real data from analysis results
        results = getattr(self, 'analysis_results', {})

        # Create metric cards
        metrics = []

        # Domain Authority
        if 'moz' in results and results['moz']['success']:
            da = results['moz']['data'].get('domain_authority', 'N/A')
            metrics.append({"name": "Domain Authority", "value": da})
        else:
            metrics.append({"name": "Domain Authority", "value": "N/A"})

        # Domain Rating
        if 'ahrefs' in results and results['ahrefs']['success']:
            dr = results['ahrefs']['data'].get('domainRating', 'N/A')
            metrics.append({"name": "Domain Rating", "value": dr})
        else:
            metrics.append({"name": "Domain Rating", "value": "N/A"})

        # Monthly Visits
        if 'similarweb' in results and results['similarweb']['success']:
            visits_data = results['similarweb']['data'].get('visits', {})
            if visits_data:
                latest_visits = list(visits_data.values())[-1]
                metrics.append({"name": "Monthly Visits", "value": f"{latest_visits:,}"})
            else:
                metrics.append({"name": "Monthly Visits", "value": "N/A"})
        else:
            metrics.append({"name": "Monthly Visits", "value": "N/A"})

        # Pages Indexed
        if 'sitemap' in results and results['sitemap']['success']:
            pages = results['sitemap']['pages']
            metrics.append({"name": "Pages Indexed", "value": pages})
        else:
            metrics.append({"name": "Pages Indexed", "value": "N/A"})

        # Create a frame for the metrics
        cards_frame = ttk.Frame(metrics_frame)
        cards_frame.pack(fill=tk.X, padx=10, pady=10)

        # Configure grid
        for i in range(4):
            cards_frame.columnconfigure(i, weight=1)

        # Add metric cards
        for i, metric in enumerate(metrics):
            card = ttk.Frame(cards_frame, relief=tk.RAISED, borderwidth=1)
            card.grid(row=0, column=i, padx=5, pady=5, sticky=tk.NSEW)

            value_label = ttk.Label(card, text=str(metric["value"]), font=("Arial", 16, "bold"))
            value_label.pack(pady=(10, 5))

            name_label = ttk.Label(card, text=metric["name"])
            name_label.pack(pady=(0, 10))

        # Summary section
        summary_frame = ttk.LabelFrame(self.overview_tab, text="Summary")
        summary_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Count successful analyses
        successful_sources = sum(1 for result in results.values() if result.get('success', False))
        total_sources = len(results)

        summary_text = f"""
Domain: {domain}
Location: {self.location_var.get()}
Language: {self.language_var.get()}

Analysis Results: {successful_sources}/{total_sources} data sources successful

Data Sources Used:
"""

        # Add data source status
        if 'sitemap' in results:
            status = "✅" if results['sitemap']['success'] else "❌"
            summary_text += f"- Sitemap: {status}\n"
        if 'moz' in results:
            status = "✅" if results['moz']['success'] else "❌"
            summary_text += f"- Moz: {status}\n"
        if 'ahrefs' in results:
            status = "✅" if results['ahrefs']['success'] else "❌"
            summary_text += f"- Ahrefs: {status}\n"
        if 'similarweb' in results:
            status = "✅" if results['similarweb']['success'] else "❌"
            summary_text += f"- SimilarWeb: {status}\n"
        if 'seo_api' in results:
            status = "✅" if results['seo_api']['success'] else "❌"
            summary_text += f"- SEO API: {status}\n"
        if 'google' in results:
            status = "✅" if results['google']['success'] else "❌"
            summary_text += f"- Google Keywords: {status}\n"

        summary_area = scrolledtext.ScrolledText(summary_frame, wrap=tk.WORD)
        summary_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        summary_area.insert(tk.END, summary_text)
        summary_area.config(state=tk.DISABLED)
    
    def update_keywords_tab(self):
        """Update the keywords tab with results"""
        # Create a frame for the keyword table
        table_frame = ttk.Frame(self.keywords_tab)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create treeview for keywords
        columns = ("keyword", "volume", "position")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        # Define headings
        tree.heading("keyword", text="Keyword")
        tree.heading("volume", text="Monthly Volume")
        tree.heading("position", text="Position")
        
        # Define columns
        tree.column("keyword", width=300)
        tree.column("volume", width=150, anchor=tk.CENTER)
        tree.column("position", width=150, anchor=tk.CENTER)
        
        # Add data
        for kw in self.sample_data['keywords']:
            tree.insert("", tk.END, values=(kw['keyword'], f"{kw['volume']:,}", kw['position']))
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(fill=tk.BOTH, expand=True)
    
    def update_traffic_tab(self):
        """Update the traffic tab with results"""
        # Create a frame for the chart
        chart_frame = ttk.Frame(self.traffic_tab)
        chart_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Get real data from analysis results
        results = getattr(self, 'analysis_results', {})

        # Create figure
        fig = Figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot(111)

        # Try to use real SimilarWeb data
        if 'similarweb' in results and results['similarweb']['success']:
            visits_data = results['similarweb']['data'].get('visits', {})
            if visits_data:
                months = list(visits_data.keys())
                visits = list(visits_data.values())
                ax.plot(months, visits, marker='o', linestyle='-', color='#1f77b4')
                ax.set_title('Monthly Traffic (SimilarWeb)')
            else:
                # Fallback to sample data
                months = self.sample_data['traffic_data']['months']
                visits = self.sample_data['traffic_data']['visits']
                ax.plot(months, visits, marker='o', linestyle='-', color='#1f77b4')
                ax.set_title('Monthly Traffic (Sample Data)')
        else:
            # Use sample data
            months = self.sample_data['traffic_data']['months']
            visits = self.sample_data['traffic_data']['visits']
            ax.plot(months, visits, marker='o', linestyle='-', color='#1f77b4')
            ax.set_title('Monthly Traffic (Sample Data)')

        ax.set_xlabel('Month')
        ax.set_ylabel('Visits')
        ax.grid(True, linestyle='--', alpha=0.7)

        # Create canvas
        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def update_technical_tab(self, domain):
        """Update the technical tab with results"""
        # Create a frame for technical issues
        issues_frame = ttk.LabelFrame(self.technical_tab, text="Technical Issues")
        issues_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Sample technical issues
        issues = [
            {"severity": "High", "issue": "Missing meta descriptions on 5 pages"},
            {"severity": "Medium", "issue": "3 pages with duplicate title tags"},
            {"severity": "Medium", "issue": "8 images missing alt text"},
            {"severity": "Low", "issue": "2 pages with low word count"},
            {"severity": "Low", "issue": "robots.txt missing"}
        ]
        
        # Create treeview for issues
        columns = ("severity", "issue")
        tree = ttk.Treeview(issues_frame, columns=columns, show="headings")
        
        # Define headings
        tree.heading("severity", text="Severity")
        tree.heading("issue", text="Issue")
        
        # Define columns
        tree.column("severity", width=100)
        tree.column("issue", width=500)
        
        # Add data
        for issue in issues:
            tree.insert("", tk.END, values=(issue['severity'], issue['issue']))
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(issues_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(fill=tk.BOTH, expand=True)

def main():
    root = tk.Tk()
    app = SimpleSEODashboard(root)
    root.mainloop()

if __name__ == "__main__":
    main()
