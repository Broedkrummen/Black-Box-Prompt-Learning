"""
Complete SEO Analysis Dashboard
Integrates ALL API endpoints: VEBAPI + RapidAPI + Onboarding Project
"""

import streamlit as st
import http.client
import json
from urllib.parse import quote
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Complete SEO Dashboard",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Keys
VEBAPI_KEY = "de26a23c-a63c-40d1-8e0d-6803f045035f"
RAPIDAPI_KEY = "5c359bb774msh32eed0a33c585c4p1466d6jsn5620b810b2f7"

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🚀 Complete SEO Analysis Dashboard</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #666;">Comprehensive SEO analysis with 36 API endpoints</p>', unsafe_allow_html=True)

# Helper function for API calls
def call_api(host, endpoint, headers, method="GET", payload=None):
    """Generic API call function"""
    try:
        conn = http.client.HTTPSConnection(host)
        if method == "POST" and payload:
            conn.request(method, endpoint, payload, headers)
        elif method == "DELETE" and payload:
            conn.request(method, endpoint, payload, headers)
        else:
            conn.request(method, endpoint, headers=headers)
        
        res = conn.getresponse()
        data = res.read().decode("utf-8")
        
        try:
            return True, json.loads(data)
        except:
            return False, data
    except Exception as e:
        return False, str(e)

# VEBAPI Functions
def vebapi_call(endpoint, params):
    """Call VEBAPI endpoint"""
    query_params = "&".join([f"{k}={quote(str(v))}" for k, v in params.items()])
    url = f"/api{endpoint}?{query_params}"
    headers = {
        'X-API-KEY': VEBAPI_KEY,
        'Content-Type': 'application/json'
    }
    return call_api("vebapi.com", url, headers)

# RapidAPI Functions
def rapidapi_call(host, endpoint, method="GET", payload=None):
    """Call RapidAPI endpoint"""
    headers = {
        'x-rapidapi-key': RAPIDAPI_KEY,
        'x-rapidapi-host': host,
        'Content-Type': 'application/json'
    }
    return call_api(host, endpoint, headers, method, payload)

# Sidebar
st.sidebar.title("⚙️ Configuration")
domain = st.sidebar.text_input("🌐 Domain", "codeconia.com")
url = f"https://{domain}"
keyword = st.sidebar.text_input("🔑 Keyword", "seo tools")
country = st.sidebar.selectbox("🌍 Country", ["us", "uk", "dk", "de", "fr"])

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Select API Groups")

# API Group Selection
use_vebapi = st.sidebar.checkbox("🚀 VEBAPI (11 endpoints)", value=True)
use_rapidapi_seo = st.sidebar.checkbox("🔍 RapidAPI SEO Tools (9 endpoints)", value=True)
use_rapidapi_keywords = st.sidebar.checkbox("🔑 RapidAPI Keywords (4 endpoints)", value=True)
use_rapidapi_other = st.sidebar.checkbox("📈 RapidAPI Other (3 endpoints)", value=True)
use_onboarding = st.sidebar.checkbox("🛒 Onboarding Project (7 endpoints)", value=False)

analyze_button = st.sidebar.button("🚀 Run Complete Analysis", type="primary")

# Main content
if analyze_button:
    results = {}
    
    # Progress tracking
    total_apis = 0
    if use_vebapi: total_apis += 11
    if use_rapidapi_seo: total_apis += 9
    if use_rapidapi_keywords: total_apis += 4
    if use_rapidapi_other: total_apis += 3
    if use_onboarding: total_apis += 7
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    current_api = 0
    
    # VEBAPI Endpoints
    if use_vebapi:
        st.header("🚀 VEBAPI Results")
        
        with st.spinner("Analyzing with VEBAPI..."):
            vebapi_results = {}
            
            # 1. Page Analysis
            current_api += 1
            progress_bar.progress(current_api / total_apis)
            status_text.text(f"[{current_api}/{total_apis}] Page Analysis...")
            success, data = vebapi_call("/seo/analyze", {"website": domain})
            vebapi_results['page_analysis'] = {'success': success, 'data': data}
            
            # 2. AI Search Engine Analyzer
            current_api += 1
            progress_bar.progress(current_api / total_apis)
            status_text.text(f"[{current_api}/{total_apis}] AI Search Engine Analyzer...")
            success, data = vebapi_call("/seo/apipagechecker", {"website": domain})
            vebapi_results['ai_search_analyzer'] = {'success': success, 'data': data}
            
            # 3. Loading Speed
            current_api += 1
            progress_bar.progress(current_api / total_apis)
            status_text.text(f"[{current_api}/{total_apis}] Loading Speed...")
            success, data = vebapi_call("/seo/loadingspeeddata", {"website": domain})
            vebapi_results['loading_speed'] = {'success': success, 'data': data}
            
            # 4. Domain Data
            current_api += 1
            progress_bar.progress(current_api / total_apis)
            status_text.text(f"[{current_api}/{total_apis}] Domain Data...")
            success, data = vebapi_call("/seo/domainnamedata", {"website": domain})
            vebapi_results['domain_data'] = {'success': success, 'data': data}
            
            # 5. Backlink Data
            current_api += 1
            progress_bar.progress(current_api / total_apis)
            status_text.text(f"[{current_api}/{total_apis}] Backlink Data...")
            success, data = vebapi_call("/seo/backlinkdata", {"website": domain})
            vebapi_results['backlink_data'] = {'success': success, 'data': data}
            
            # 6. New Backlinks
            current_api += 1
            progress_bar.progress(current_api / total_apis)
            status_text.text(f"[{current_api}/{total_apis}] New Backlinks...")
            success, data = vebapi_call("/seo/newbacklinks", {"website": domain})
            vebapi_results['new_backlinks'] = {'success': success, 'data': data}
            
            # 7. Referral Domains
            current_api += 1
            progress_bar.progress(current_api / total_apis)
            status_text.text(f"[{current_api}/{total_apis}] Referral Domains...")
            success, data = vebapi_call("/seo/referraldomains", {"website": domain})
            vebapi_results['referral_domains'] = {'success': success, 'data': data}
            
            # 8. AI SEO Crawler
            current_api += 1
            progress_bar.progress(current_api / total_apis)
            status_text.text(f"[{current_api}/{total_apis}] AI SEO Crawler...")
            success, data = vebapi_call("/seo/aiseochecker", {"website": domain})
            vebapi_results['ai_seo_crawler'] = {'success': success, 'data': data}
            
            # 9. Top Keywords
            current_api += 1
            progress_bar.progress(current_api / total_apis)
            status_text.text(f"[{current_api}/{total_apis}] Top Keywords...")
            success, data = vebapi_call("/seo/topsearchkeywords", {"website": domain})
            vebapi_results['top_keywords'] = {'success': success, 'data': data}
            
            # 10. Poor Backlinks
            current_api += 1
            progress_bar.progress(current_api / total_apis)
            status_text.text(f"[{current_api}/{total_apis}] Poor Backlinks...")
            success, data = vebapi_call("/seo/poorbacklinks", {"website": domain})
            vebapi_results['poor_backlinks'] = {'success': success, 'data': data}
            
            # 11. Keyword Density
            current_api += 1
            progress_bar.progress(current_api / total_apis)
            status_text.text(f"[{current_api}/{total_apis}] Keyword Density...")
            success, data = vebapi_call("/seo/keyworddensity", {"keyword": keyword, "website": domain})
            vebapi_results['keyword_density'] = {'success': success, 'data': data}
            
            results['vebapi'] = vebapi_results
            
            # Display VEBAPI results
            col1, col2, col3 = st.columns(3)
            working = sum(1 for v in vebapi_results.values() if v['success'])
            col1.metric("Total Endpoints", "11")
            col2.metric("Working", working)
            col3.metric("Success Rate", f"{(working/11*100):.1f}%")
    
    # RapidAPI SEO Tools
    if use_rapidapi_seo:
        st.header("🔍 RapidAPI SEO Tools")
        
        with st.spinner("Analyzing with RapidAPI SEO Tools..."):
            rapidapi_seo_results = {}
            
            # 1. SEOX - Keywords
            current_api += 1
            progress_bar.progress(current_api / total_apis)
            status_text.text(f"[{current_api}/{total_apis}] SEOX Keywords...")
            success, data = rapidapi_call("seox.p.rapidapi.com", f"/api/keywordsu?url={quote(url)}", "POST", "{}")
            rapidapi_seo_results['seox_keywords'] = {'success': success, 'data': data}
            
            # 2. SEOX - Links
            current_api += 1
            progress_bar.progress(current_api / total_apis)
            status_text.text(f"[{current_api}/{total_apis}] SEOX Links...")
            success, data = rapidapi_call("seox.p.rapidapi.com", f"/api/links?url={quote(url)}")
            rapidapi_seo_results['seox_links'] = {'success': success, 'data': data}
            
            # 3. SEOX - Sitemap
            current_api += 1
            progress_bar.progress(current_api / total_apis)
            status_text.text(f"[{current_api}/{total_apis}] SEOX Sitemap...")
            success, data = rapidapi_call("seox.p.rapidapi.com", f"/api/sitemap/get?url={quote(url)}")
            rapidapi_seo_results['seox_sitemap'] = {'success': success, 'data': data}
            
            # 4. SEOX - SEO Analysis
            current_api += 1
            progress_bar.progress(current_api / total_apis)
            status_text.text(f"[{current_api}/{total_apis}] SEOX SEO Analysis...")
            success, data = rapidapi_call("seox.p.rapidapi.com", f"/api/seo?url={quote(url)}")
            rapidapi_seo_results['seox_seo'] = {'success': success, 'data': data}
            
            # 5. SEOX - SSL Check
            current_api += 1
            progress_bar.progress(current_api / total_apis)
            status_text.text(f"[{current_api}/{total_apis}] SEOX SSL...")
            success, data = rapidapi_call("seox.p.rapidapi.com", f"/api/ssl?domain={domain}")
            rapidapi_seo_results['seox_ssl'] = {'success': success, 'data': data}
            
            # 6. SEOX - DNS
            current_api += 1
            progress_bar.progress(current_api / total_apis)
            status_text.text(f"[{current_api}/{total_apis}] SEOX DNS...")
            success, data = rapidapi_call("seox.p.rapidapi.com", f"/api/dns?domain={domain}&whois=true&iplookup=true")
            rapidapi_seo_results['seox_dns'] = {'success': success, 'data': data}
            
            # 7. AI Scraper
            current_api += 1
            progress_bar.progress(current_api / total_apis)
            status_text.text(f"[{current_api}/{total_apis}] AI Scraper...")
            success, data = rapidapi_call("ai-scraper-api.p.rapidapi.com", f"/AIscrape?url={quote(url)}&schema=%7B%7D&headers=%7B%7D&country=us")
            rapidapi_seo_results['ai_scraper'] = {'success': success, 'data': data}
            
            # 8. Moz DA/PA
            current_api += 1
            progress_bar.progress(current_api / total_apis)
            status_text.text(f"[{current_api}/{total_apis}] Moz DA/PA...")
            payload = json.dumps({"q": domain})
            success, data = rapidapi_call("moz-da-pa1.p.rapidapi.com", "/v1/getDaPa", "POST", payload)
            rapidapi_seo_results['moz_dapa'] = {'success': success, 'data': data}
            
            # 9. SEO Keyword Research
            current_api += 1
            progress_bar.progress(current_api / total_apis)
            status_text.text(f"[{current_api}/{total_apis}] SEO Keyword Research...")
            success, data = rapidapi_call("seo-keyword-research.p.rapidapi.com", f"/keyworddensity.php?keyword={quote(keyword)}&site={domain}")
            rapidapi_seo_results['seo_keyword_research'] = {'success': success, 'data': data}
            
            results['rapidapi_seo'] = rapidapi_seo_results
            
            # Display results
            col1, col2, col3 = st.columns(3)
            working = sum(1 for v in rapidapi_seo_results.values() if v['success'])
            col1.metric("Total Endpoints", "9")
            col2.metric("Working", working)
            col3.metric("Success Rate", f"{(working/9*100):.1f}%")
    
    # RapidAPI Keywords
    if use_rapidapi_keywords:
        st.header("🔑 RapidAPI Keyword Tools")
        
        with st.spinner("Analyzing keywords..."):
            rapidapi_keyword_results = {}
            
            # 1. Semrush - Global Volume
            current_api += 1
            progress_bar.progress(current_api / total_apis)
            status_text.text(f"[{current_api}/{total_apis}] Semrush Global Volume...")
            success, data = rapidapi_call("semrush-keyword-magic-tool.p.rapidapi.com", f"/global-volume?keyword={quote(keyword)}&country={country}")
            rapidapi_keyword_results['semrush_volume'] = {'success': success, 'data': data}
            
            # 2. Semrush - Keyword Research
            current_api += 1
            progress_bar.progress(current_api / total_apis)
            status_text.text(f"[{current_api}/{total_apis}] Semrush Keyword Research...")
            success, data = rapidapi_call("semrush-keyword-magic-tool.p.rapidapi.com", f"/keyword-research?keyword={quote(keyword)}&country={country}&languagecode=en")
            rapidapi_keyword_results['semrush_research'] = {'success': success, 'data': data}
            
            # 3. Semrush - Question Keywords
            current_api += 1
            progress_bar.progress(current_api / total_apis)
            status_text.text(f"[{current_api}/{total_apis}] Semrush Questions...")
            success, data = rapidapi_call("semrush-keyword-magic-tool.p.rapidapi.com", f"/Question-keyword-research-More?keyword={quote(keyword)}&country={country}")
            rapidapi_keyword_results['semrush_questions'] = {'success': success, 'data': data}
            
            # 4. G-KeyInsight
            current_api += 1
            progress_bar.progress(current_api / total_apis)
            status_text.text(f"[{current_api}/{total_apis}] G-KeyInsight...")
            success, data = rapidapi_call("g-keyinsight.p.rapidapi.com", f"/api/v1/keyword-suggestions?keyword={quote(keyword)}&country={country}")
            rapidapi_keyword_results['g_keyinsight'] = {'success': success, 'data': data}
            
            results['rapidapi_keywords'] = rapidapi_keyword_results
            
            # Display results
            col1, col2, col3 = st.columns(3)
            working = sum(1 for v in rapidapi_keyword_results.values() if v['success'])
            col1.metric("Total Endpoints", "4")
            col2.metric("Working", working)
    
    # RapidAPI Other Tools
    if use_rapidapi_other:
        st.header("📈 RapidAPI Other Tools")
        
        with st.spinner("Running additional analyses..."):
            rapidapi_other_results = {}
            
            # 1. Google Rank Checker
            current_api += 1
            progress_bar.progress(current_api / total_apis)
            status_text.text(f"[{current_api}/{total_apis}] Google Rank...")
            success, data = rapidapi_call("google-rank-checker1.p.rapidapi.com", f"/rank?keyword={quote(keyword)}&url={quote(url)}")
            rapidapi_other_results['google_rank'] = {'success': success, 'data': data}
            
            # 2. Website Utilities
            current_api += 1
            progress_bar.progress(current_api / total_apis)
            status_text.text(f"[{current_api}/{total_apis}] Website Utilities...")
            success, data = rapidapi_call("website-utilities.p.rapidapi.com", f"/ping?url={quote(url)}")
            rapidapi_other_results['website_utilities'] = {'success': success, 'data': data}
            
            # 3. Google Trends
            current_api += 1
            progress_bar.progress(current_api / total_apis)
            status_text.text(f"[{current_api}/{total_apis}] Google Trends...")
            success, data = rapidapi_call("google-trends-api1.p.rapidapi.com", f"/trendsearch?keyword={quote(keyword)}&country={country}")
            rapidapi_other_results['google_trends'] = {'success': success, 'data': data}
            
            results['rapidapi_other'] = rapidapi_other_results
            
            # Display results
            col1, col2, col3 = st.columns(3)
            working = sum(1 for v in rapidapi_other_results.values() if v['success'])
            col1.metric("Total Endpoints", "3")
            col2.metric("Working", working)
            col3.metric("Success Rate", f"{(working/3*100):.1f}%")
    
    # Onboarding Project API
    if use_onboarding:
        st.header("🛒 Onboarding Project API")
        
        with st.spinner("Testing Onboarding Project API..."):
            onboarding_results = {}
            
            # 1. Get My Orders
            current_api += 1
            progress_bar.progress(current_api / total_apis)
            status_text.text(f"[{current_api}/{total_apis}] Get My Orders...")
            success, data = rapidapi_call("onboarding-project3982.p.rapidapi.com", "/order/my")
            onboarding_results['my_orders'] = {'success': success, 'data': data}
            
            # 2. Get All Products
            current_api += 1
            progress_bar.progress(current_api / total_apis)
            status_text.text(f"[{current_api}/{total_apis}] Get All Products...")
            success, data = rapidapi_call("onboarding-project3982.p.rapidapi.com", "/catalog/products")
            onboarding_results['all_products'] = {'success': success, 'data': data}
            
            # 3. Get Products by Category
            current_api += 1
            progress_bar.progress(current_api / total_apis)
            status_text.text(f"[{current_api}/{total_apis}] Get Products by Category...")
            success, data = rapidapi_call("onboarding-project3982.p.rapidapi.com", "/catalog/category/electronics/products")
            onboarding_results['category_products'] = {'success': success, 'data': data}
            
            # 4. Get All Categories
            current_api += 1
            progress_bar.progress(current_api / total_apis)
            status_text.text(f"[{current_api}/{total_apis}] Get All Categories...")
            success, data = rapidapi_call("onboarding-project3982.p.rapidapi.com", "/catalog/categories")
            onboarding_results['categories'] = {'success': success, 'data': data}
            
            # 5. Get Product by ID
            current_api += 1
            progress_bar.progress(current_api / total_apis)
            status_text.text(f"[{current_api}/{total_apis}] Get Product by ID...")
            success, data = rapidapi_call("onboarding-project3982.p.rapidapi.com", "/catalog/product/1")
            onboarding_results['product_by_id'] = {'success': success, 'data': data}
            
            # 6. Create Product (POST)
            current_api += 1
            progress_bar.progress(current_api / total_apis)
            status_text.text(f"[{current_api}/{total_apis}] Create Product...")
            payload = json.dumps({
                "name": "Test Product",
                "price": 99.99,
                "manufacturer": "Test Manufacturer",
                "category": "electronics",
                "description": "Test Description",
                "tags": "test,demo"
            })
            success, data = rapidapi_call("onboarding-project3982.p.rapidapi.com", "/catalog/product", "POST", payload)
            onboarding_results['create_product'] = {'success': success, 'data': data}
            
            # 7. Delete Product (DELETE)
            current_api += 1
            progress_bar.progress(current_api / total_apis)
            status_text.text(f"[{current_api}/{total_apis}] Delete Product...")
            success, data = rapidapi_call("onboarding-project3982.p.rapidapi.com", "/catalog/product/999", "DELETE", "{}")
            onboarding_results['delete_product'] = {'success': success, 'data': data}
            
            results['onboarding'] = onboarding_results
            
            # Display results
            col1, col2, col3 = st.columns(3)
            working = sum(1 for v in onboarding_results.values() if v['success'])
            col1.metric("Total Endpoints", "7")
            col2.metric("Working", working)
            col3.metric("Success Rate", f"{(working/7*100):.1f}%")
    
    # Clear progress
    progress_bar.empty()
    status_text.empty()
    
    # Overall Summary
    st.header("📊 Overall Summary")
    
    total_endpoints = 0
    total_working = 0
    
    for group_name, group_data in results.items():
        if isinstance(group_data, dict):
            total_endpoints += len(group_data)
            total_working += sum(1 for v in group_data.values() if isinstance(v, dict) and v.get('success'))
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total APIs Tested", total_endpoints)
    col2.metric("Working APIs", total_working)
    col3.metric("Failed APIs", total_endpoints - total_working)
    col4.metric("Success Rate", f"{(total_working/total_endpoints*100):.1f}%")
    
    # Keyword Analysis Table
    st.header("🔑 Keyword Analysis Overview")
    
    # Semrush Volume - Monthly Trend Analysis
    if 'rapidapi_keywords' in results:
        if results['rapidapi_keywords'].get('semrush_volume', {}).get('success'):
            st.subheader("📈 Semrush Monthly Search Volume Trend")
            
            semrush_data = results['rapidapi_keywords']['semrush_volume']['data']
            
            # Check if monthly data exists
            if isinstance(semrush_data, dict):
                # Display main metrics
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Keyword", keyword)
                col2.metric("Country", country.upper())
                col3.metric("Total Volume", semrush_data.get('volume', 'N/A'))
                col4.metric("Avg CPC", f"${semrush_data.get('cpc', 0):.2f}" if isinstance(semrush_data.get('cpc'), (int, float)) else 'N/A')
                
                # Extract monthly data if available
                monthly_data = semrush_data.get('monthly_searches', [])
                if monthly_data and isinstance(monthly_data, list):
                    # Create DataFrame for monthly data
                    df_monthly = pd.DataFrame(monthly_data)
                    
                    if not df_monthly.empty and 'month' in df_monthly.columns and 'searches' in df_monthly.columns:
                        st.markdown("### 📊 Monthly Search Volume Table")
                        
                        # Format the table
                        df_display = df_monthly.copy()
                        if 'searches' in df_display.columns:
                            df_display['searches'] = df_display['searches'].apply(lambda x: f"{int(x):,}" if pd.notna(x) else 'N/A')
                        
                        st.dataframe(
                            df_display,
                            use_container_width=True,
                            hide_index=True
                        )
                        
                        # Create line chart for monthly trend
                        st.markdown("### 📈 Monthly Search Volume Trend")
                        
                        df_chart = pd.DataFrame(monthly_data)
                        if 'month' in df_chart.columns and 'searches' in df_chart.columns:
                            fig = px.line(
                                df_chart,
                                x='month',
                                y='searches',
                                title=f'Search Volume Trend for "{keyword}" in {country.upper()}',
                                markers=True,
                                labels={'month': 'Month', 'searches': 'Search Volume'}
                            )
                            fig.update_layout(
                                xaxis_title="Month",
                                yaxis_title="Search Volume",
                                hovermode='x unified'
                            )
                            fig.update_traces(
                                line=dict(color='#1f77b4', width=3),
                                marker=dict(size=8)
                            )
                            st.plotly_chart(fig, use_container_width=True)
                            
                            # Download button for monthly data
                            csv_monthly = df_monthly.to_csv(index=False)
                            st.download_button(
                                label="📥 Download Monthly Data CSV",
                                data=csv_monthly,
                                file_name=f"semrush_monthly_{keyword}_{country}_{datetime.now().strftime('%Y%m%d')}.csv",
                                mime="text/csv"
                            )
                    else:
                        st.info("Monthly search data structure not available in API response")
                else:
                    # If no monthly data, show available data
                    st.info("Monthly breakdown not available. Showing aggregate data:")
                    st.json(semrush_data)
            else:
                st.warning("Unexpected data format from Semrush API")
    
    st.markdown("---")
    
    # Aggregated Keyword Data Table
    st.subheader("🔍 All Keywords Overview")
    
    keyword_data = []
    
    # Extract keyword data from RapidAPI Keywords
    if 'rapidapi_keywords' in results:
        # Semrush Global Volume
        if results['rapidapi_keywords'].get('semrush_volume', {}).get('success'):
            data = results['rapidapi_keywords']['semrush_volume']['data']
            if isinstance(data, dict) and 'volume' in data:
                keyword_data.append({
                    'Keyword': keyword,
                    'Source': 'Semrush',
                    'Search Volume': data.get('volume', 'N/A'),
                    'CPC': data.get('cpc', 'N/A'),
                    'Competition': data.get('competition', 'N/A'),
                    'Trend': data.get('trend', 'N/A')
                })
        
        # Semrush Keyword Research
        if results['rapidapi_keywords'].get('semrush_research', {}).get('success'):
            data = results['rapidapi_keywords']['semrush_research']['data']
            if isinstance(data, dict) and 'keywords' in data:
                for kw in data['keywords'][:10]:  # Top 10
                    keyword_data.append({
                        'Keyword': kw.get('keyword', 'N/A'),
                        'Source': 'Semrush Research',
                        'Search Volume': kw.get('search_volume', 'N/A'),
                        'CPC': kw.get('cpc', 'N/A'),
                        'Competition': kw.get('competition', 'N/A'),
                        'Trend': kw.get('trend', 'N/A')
                    })
        
        # G-KeyInsight
        if results['rapidapi_keywords'].get('g_keyinsight', {}).get('success'):
            data = results['rapidapi_keywords']['g_keyinsight']['data']
            if isinstance(data, dict) and 'suggestions' in data:
                for kw in data['suggestions'][:10]:  # Top 10
                    keyword_data.append({
                        'Keyword': kw.get('keyword', 'N/A'),
                        'Source': 'G-KeyInsight',
                        'Search Volume': kw.get('volume', 'N/A'),
                        'CPC': kw.get('cpc', 'N/A'),
                        'Competition': kw.get('competition', 'N/A'),
                        'Trend': 'N/A'
                    })
    
    # Extract keyword data from VEBAPI Top Keywords
    if 'vebapi' in results:
        if results['vebapi'].get('top_keywords', {}).get('success'):
            data = results['vebapi']['top_keywords']['data']
            if isinstance(data, dict) and 'keywords' in data:
                for kw in data['keywords'][:10]:  # Top 10
                    keyword_data.append({
                        'Keyword': kw.get('keyword', 'N/A'),
                        'Source': 'VEBAPI',
                        'Search Volume': kw.get('volume', 'N/A'),
                        'CPC': kw.get('cpc', 'N/A'),
                        'Competition': kw.get('competition', 'N/A'),
                        'Trend': kw.get('trend', 'N/A')
                    })
    
    if keyword_data:
        df_keywords = pd.DataFrame(keyword_data)
        
        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Keywords", len(df_keywords))
        
        if 'Search Volume' in df_keywords.columns:
            try:
                avg_volume = df_keywords['Search Volume'].apply(lambda x: float(x) if str(x).replace('.','').isdigit() else 0).mean()
                col2.metric("Avg Search Volume", f"{avg_volume:,.0f}")
            except:
                col2.metric("Avg Search Volume", "N/A")
        
        if 'CPC' in df_keywords.columns:
            try:
                avg_cpc = df_keywords['CPC'].apply(lambda x: float(str(x).replace('$','')) if '$' in str(x) else (float(x) if str(x).replace('.','').isdigit() else 0)).mean()
                col3.metric("Avg CPC", f"${avg_cpc:.2f}")
            except:
                col3.metric("Avg CPC", "N/A")
        
        col4.metric("Data Sources", df_keywords['Source'].nunique())
        
        # Display table
        st.markdown("### 📊 Keyword Data Table")
        st.dataframe(
            df_keywords,
            use_container_width=True,
            hide_index=True
        )
        
        # Download button for keywords
        csv = df_keywords.to_csv(index=False)
        st.download_button(
            label="📥 Download Keywords CSV",
            data=csv,
            file_name=f"keywords_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
        
        # Visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            if 'Search Volume' in df_keywords.columns:
                st.markdown("### 📈 Search Volume Distribution")
                try:
                    df_plot = df_keywords.copy()
                    df_plot['Search Volume'] = pd.to_numeric(df_plot['Search Volume'], errors='coerce')
                    df_plot = df_plot.dropna(subset=['Search Volume'])
                    if not df_plot.empty:
                        fig = px.bar(
                            df_plot.head(15),
                            x='Keyword',
                            y='Search Volume',
                            color='Source',
                            title='Top 15 Keywords by Search Volume'
                        )
                        fig.update_xaxis(tickangle=-45)
                        st.plotly_chart(fig, use_container_width=True)
                except Exception as e:
                    st.info("Unable to create search volume chart")
        
        with col2:
            if 'CPC' in df_keywords.columns:
                st.markdown("### 💰 CPC Analysis")
                try:
                    df_plot = df_keywords.copy()
                    df_plot['CPC_numeric'] = df_plot['CPC'].apply(
                        lambda x: float(str(x).replace('$','')) if '$' in str(x) else (float(x) if str(x).replace('.','').isdigit() else 0)
                    )
                    df_plot = df_plot[df_plot['CPC_numeric'] > 0]
                    if not df_plot.empty:
                        fig = px.scatter(
                            df_plot.head(15),
                            x='Search Volume',
                            y='CPC_numeric',
                            size='CPC_numeric',
                            color='Source',
                            hover_data=['Keyword'],
                            title='Search Volume vs CPC'
                        )
                        st.plotly_chart(fig, use_container_width=True)
                except Exception as e:
                    st.info("Unable to create CPC chart")
    else:
        st.info("No keyword data available. Enable keyword analysis APIs to see keyword metrics.")
    
    # Detailed Results
    st.header("📋 Detailed Results")
    
    for group_name, group_data in results.items():
        with st.expander(f"📂 {group_name.upper().replace('_', ' ')} - {len(group_data)} endpoints"):
            for api_name, api_result in group_data.items():
                status_icon = "✅" if api_result.get('success') else "❌"
                st.markdown(f"**{status_icon} {api_name.replace('_', ' ').title()}**")
                
                if api_result.get('success'):
                    st.json(api_result['data'] if isinstance(api_result['data'], dict) else {"response": str(api_result['data'])[:500]})
                else:
                    st.error(f"Error: {api_result.get('data', 'Unknown error')}")
                
                st.markdown("---")
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"complete_seo_analysis_{timestamp}.json"
    
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    st.success(f"✅ Analysis complete! Results saved to {filename}")
    
    # Download button
    st.download_button(
        label="📥 Download Results",
        data=json.dumps(results, indent=2, default=str),
        file_name=filename,
        mime="application/json"
    )

else:
    st.info("👈 Configure your settings in the sidebar and click 'Run Complete Analysis' to start")
    
    # Show API counts
    st.markdown("### 📊 Available APIs")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**VEBAPI (11 endpoints)**")
        st.markdown("""
        - Page Analysis
        - AI Search Engine Analyzer
        - Loading Speed Data
        - Domain Name Data
        - Backlink Data
        - New Backlinks
        - Referral Domains
        - AI SEO Crawler
        - Top Search Keywords
        - Poor Backlinks
        - Keyword Density
        """)
    
    with col2:
        st.markdown("**RapidAPI (25+ endpoints)**")
        st.markdown("""
        **SEO Tools (9):**
        - SEOX Keywords, Links, Sitemap
        - SEOX SEO, SSL, DNS
        - AI Scraper, Moz DA/PA
        - SEO Keyword Research
        
        **Keywords (4):**
        - Semrush Volume, Research, Questions
        - G-KeyInsight
        
        **Other (3):**
        - Google Rank, Website Utilities
        - Google Trends
        
        **Onboarding Project (7):**
        - My Orders, All Products
        - Products by Category, Categories
        - Product by ID, Create Product
        - Delete Product
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🚀 Complete SEO Dashboard | 34 API Endpoints | Built with Streamlit</p>
</div>
""", unsafe_allow_html=True)
