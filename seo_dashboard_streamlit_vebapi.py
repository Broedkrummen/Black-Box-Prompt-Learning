"""
SEO Analysis Dashboard - Streamlit Version with VebAPI Integration
Interactive graphical dashboard for comprehensive SEO analysis
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import http.client
import json
import time
import hashlib
import hmac
import base64
from urllib.parse import quote
import xml.etree.ElementTree as ET

# Page configuration
st.set_page_config(
    page_title="SEO Analysis Dashboard",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        font-weight: bold;
        border-radius: 5px;
        padding: 0.5rem 1rem;
    }
</style>
""", unsafe_allow_html=True)

# API Configuration
RAPIDAPI_KEY = "5c359bb774msh32eed0a33c585c4p1466d6jsn5620b810b2f7"
MOZ_ACCESS_ID = "mozscape-c7fe158e8e"
MOZ_SECRET_KEY = "e0c2a5e8e0e44f5e8c7fe158e8e0c2a5"
VEBAPI_KEY = "de26a23c-a63c-40d1-8e0d-6803f045035f"

# Initialize session state
if 'analysis_data' not in st.session_state:
    st.session_state.analysis_data = None
if 'analyzing' not in st.session_state:
    st.session_state.analyzing = False

def crawl_sitemap(domain):
    """Crawl sitemap and return page count"""
    try:
        import urllib.request
        sitemap_url = f"https://{domain}/sitemap.xml"
        
        with urllib.request.urlopen(sitemap_url, timeout=10) as response:
            xml_content = response.read().decode('utf-8')
        
        root = ET.fromstring(xml_content)
        urls = []
        
        for url in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
            loc = url.text
            if loc.endswith('.xml'):
                try:
                    with urllib.request.urlopen(loc, timeout=10) as sub_response:
                        sub_xml = sub_response.read().decode('utf-8')
                    sub_root = ET.fromstring(sub_xml)
                    for sub_url in sub_root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
                        if not sub_url.text.endswith('.xml'):
                            urls.append(sub_url.text)
                except:
                    pass
            else:
                urls.append(loc)
        
        return {"success": True, "pages": len(urls), "urls": urls[:20]}
    except Exception as e:
        return {"success": False, "error": str(e), "pages": 0}

def analyze_moz(domain):
    """Analyze with Moz API"""
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

def analyze_ahrefs(domain):
    """Analyze with Ahrefs API"""
    try:
        conn = http.client.HTTPSConnection("ahrefs-domain-research.p.rapidapi.com")
        headers = {
            'x-rapidapi-key': RAPIDAPI_KEY,
            'x-rapidapi-host': "ahrefs-domain-research.p.rapidapi.com"
        }
        
        conn.request("GET", f"/basic-metrics?url={domain}", headers=headers)
        res = conn.getresponse()
        data = json.loads(res.read().decode("utf-8"))
        
        if data.get("success") and data.get("data"):
            return {"success": True, "data": data.get("data")}
        elif "domainRating" in data or "ahRank" in data:
            return {"success": True, "data": data}
        else:
            return {"success": False, "error": data}
    except Exception as e:
        return {"success": False, "error": str(e)}

def analyze_similarweb(domain):
    """Analyze with SimilarWeb API"""
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

def analyze_seo_api(domain, location):
    """Analyze with SEO API"""
    try:
        conn = http.client.HTTPSConnection("seo-api-dr-rd-rank-keywords-backlinks1.p.rapidapi.com")
        headers = {
            'x-rapidapi-key': RAPIDAPI_KEY,
            'x-rapidapi-host': "seo-api-dr-rd-rank-keywords-backlinks1.p.rapidapi.com"
        }
        
        encoded_url = quote(domain, safe='')
        conn.request("GET", f"/backlink-checker?mode=subdomains&url={encoded_url}&limit=100", headers=headers)
        res = conn.getresponse()
        backlinks_data = json.loads(res.read().decode("utf-8"))
        
        conn = http.client.HTTPSConnection("seo-api-dr-rd-rank-keywords-backlinks1.p.rapidapi.com")
        conn.request("GET", f"/basic-metrics?url={encoded_url}", headers=headers)
        res = conn.getresponse()
        basic_data = json.loads(res.read().decode("utf-8"))
        
        combined_data = {
            "overview": basic_data if basic_data else {},
            "backlinks": backlinks_data.get("backlinks", []) if isinstance(backlinks_data, dict) else []
        }
        
        return {"success": True, "data": combined_data}
    except Exception as e:
        return {"success": False, "error": str(e)}

def analyze_google_keywords(domain, location, language):
    """Analyze with Google Keyword Insight"""
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

# VebAPI Functions
def analyze_vebapi_single_keyword(keyword, country):
    """Analyze single keyword with VebAPI"""
    try:
        conn = http.client.HTTPSConnection("vebapi.com")
        headers = {
            'X-API-KEY': VEBAPI_KEY,
            'Content-Type': 'application/json'
        }
        
        conn.request("GET", f"/api/seo/singlekeyword?keyword={quote(keyword)}&country={country.lower()}", headers=headers)
        res = conn.getresponse()
        data = json.loads(res.read().decode("utf-8"))
        
        if res.status == 200:
            return {"success": True, "data": data}
        else:
            return {"success": False, "error": data}
    except Exception as e:
        return {"success": False, "error": str(e)}

def analyze_vebapi_related_keywords(keyword, country):
    """Analyze related keywords with VebAPI"""
    try:
        conn = http.client.HTTPSConnection("vebapi.com")
        headers = {
            'X-API-KEY': VEBAPI_KEY,
            'Content-Type': 'application/json'
        }
        
        conn.request("GET", f"/api/seo/keywordresearch?keyword={quote(keyword)}&country={country.lower()}", headers=headers)
        res = conn.getresponse()
        data = json.loads(res.read().decode("utf-8"))
        
        if res.status == 200:
            return {"success": True, "data": data}
        else:
            return {"success": False, "error": data}
    except Exception as e:
        return {"success": False, "error": str(e)}

def analyze_vebapi_backlink_data(domain):
    """Analyze backlink data with VebAPI"""
    try:
        conn = http.client.HTTPSConnection("vebapi.com")
        headers = {
            'X-API-KEY': VEBAPI_KEY,
            'Content-Type': 'application/json'
        }
        
        conn.request("GET", f"/api/seo/backlinkdata?website={domain}", headers=headers)
        res = conn.getresponse()
        data = json.loads(res.read().decode("utf-8"))
        
        if res.status == 200:
            return {"success": True, "data": data}
        else:
            return {"success": False, "error": data}
    except Exception as e:
        return {"success": False, "error": str(e)}

def analyze_vebapi_referral_domains(domain):
    """Analyze referral domains with VebAPI"""
    try:
        conn = http.client.HTTPSConnection("vebapi.com")
        headers = {
            'X-API-KEY': VEBAPI_KEY,
            'Content-Type': 'application/json'
        }

        conn.request("GET", f"/apis/referral-domains?domain={domain}", headers=headers)
        res = conn.getresponse()
        data = res.read().decode("utf-8")

        try:
            json_data = json.loads(data)
            if res.status == 200:
                return {"success": True, "data": json_data}
            else:
                return {"success": False, "error": json_data}
        except json.JSONDecodeError:
            return {"success": False, "error": "API returned HTML instead of JSON", "html_response": data[:500]}

    except Exception as e:
        return {"success": False, "error": str(e)}

def analyze_vebapi_top_search_keywords(domain):
    """Analyze top search keywords with VebAPI"""
    try:
        conn = http.client.HTTPSConnection("vebapi.com")
        headers = {
            'X-API-KEY': VEBAPI_KEY,
            'Content-Type': 'application/json'
        }

        conn.request("GET", f"/apis/topsearch-keywords?domain={domain}", headers=headers)
        res = conn.getresponse()
        data = res.read().decode("utf-8")

        try:
            json_data = json.loads(data)
            if res.status == 200:
                return {"success": True, "data": json_data}
            else:
                return {"success": False, "error": json_data}
        except json.JSONDecodeError:
            return {"success": False, "error": "API returned HTML instead of JSON", "html_response": data[:500]}

    except Exception as e:
        return {"success": False, "error": str(e)}

def analyze_vebapi_ai_seo_checker(domain):
    """Analyze AI SEO with VebAPI"""
    try:
        conn = http.client.HTTPSConnection("vebapi.com")
        headers = {
            'X-API-KEY': VEBAPI_KEY,
            'Content-Type': 'application/json'
        }

        conn.request("GET", f"/apis/ai-seo-crawler?url={domain}", headers=headers)
        res = conn.getresponse()
        data = res.read().decode("utf-8")

        try:
            json_data = json.loads(data)
            if res.status == 200:
                return {"success": True, "data": json_data}
            else:
                return {"success": False, "error": json_data}
        except json.JSONDecodeError:
            return {"success": False, "error": "API returned HTML instead of JSON", "html_response": data[:500]}

    except Exception as e:
        return {"success": False, "error": str(e)}

def analyze_vebapi_poor_backlinks(domain):
    """Analyze poor backlinks with VebAPI"""
    try:
        conn = http.client.HTTPSConnection("vebapi.com")
        headers = {
            'X-API-KEY': VEBAPI_KEY,
            'Content-Type': 'application/json'
        }

        conn.request("GET", f"/apis/poorbacklinks?domain={domain}", headers=headers)
        res = conn.getresponse()
        data = res.read().decode("utf-8")

        try:
            json_data = json.loads(data)
            if res.status == 200:
                return {"success": True, "data": json_data}
            else:
                return {"success": False, "error": json_data}
        except json.JSONDecodeError:
            return {"success": False, "error": "API returned HTML instead of JSON", "html_response": data[:500]}

    except Exception as e:
        return {"success": False, "error": str(e)}

def analyze_vebapi_keyword_density(keyword, website):
    """Analyze keyword density with VebAPI"""
    try:
        conn = http.client.HTTPSConnection("vebapi.com")
        headers = {
            'X-API-KEY': VEBAPI_KEY,
            'Content-Type': 'application/json'
        }
        
        conn.request("GET", f"/api/seo/keyworddensity?keyword={quote(keyword)}&website={website}", headers=headers)
        res = conn.getresponse()
        data = json.loads(res.read().decode("utf-8"))
        
        if res.status == 200:
            return {"success": True, "data": data}
        else:
            return {"success": False, "error": data}
    except Exception as e:
        return {"success": False, "error": str(e)}

def run_analysis(domain, location, language, use_sitemap=True, use_moz=True, use_ahrefs=True,
                 use_similarweb=True, use_seo_api=True, use_google=True, use_vebapi=True, vebapi_keyword=None):
    """Run selective analysis based on user choices"""
    results = {}

    selected_sources = [use_sitemap, use_moz, use_ahrefs, use_similarweb, use_seo_api, use_google, use_vebapi]
    total_sources = sum(selected_sources)
    if total_sources == 0:
        return results

    progress_increment = 100 / total_sources
    current_progress = 0

    progress_bar = st.progress(0)
    status_text = st.empty()

    if use_sitemap:
        status_text.text("🔍 Crawling sitemap...")
        results['sitemap'] = crawl_sitemap(domain)
        current_progress += progress_increment
        progress_bar.progress(min(int(current_progress), 100))
        time.sleep(0.5)

    if use_moz:
        status_text.text("📊 Analyzing with Moz...")
        results['moz'] = analyze_moz(domain)
        current_progress += progress_increment
        progress_bar.progress(min(int(current_progress), 100))
        time.sleep(1)

    if use_ahrefs:
        status_text.text("📊 Analyzing with Ahrefs...")
        results['ahrefs'] = analyze_ahrefs(domain)
        current_progress += progress_increment
        progress_bar.progress(min(int(current_progress), 100))
        time.sleep(1)

    if use_similarweb:
        status_text.text("📊 Analyzing with SimilarWeb...")
        results['similarweb'] = analyze_similarweb(domain)
        current_progress += progress_increment
        progress_bar.progress(min(int(current_progress), 100))
        time.sleep(1)

    if use_seo_api:
        status_text.text("📊 Analyzing backlinks...")
        results['seo_api'] = analyze_seo_api(domain, location)
        current_progress += progress_increment
        progress_bar.progress(min(int(current_progress), 100))
        time.sleep(1)

    if use_google:
        status_text.text("📊 Analyzing keywords...")
        results['google'] = analyze_google_keywords(domain, location, language)
        current_progress += progress_increment
        progress_bar.progress(min(int(current_progress), 100))
        time.sleep(1)

    if use_vebapi:
        status_text.text("🚀 Analyzing with VebAPI...")
        keyword = vebapi_keyword if vebapi_keyword else domain.split('.')[0]

        results['vebapi'] = {
            'keyword_research': analyze_vebapi_related_keywords(keyword, location),
            'single_keyword': analyze_vebapi_single_keyword(keyword, location),
            'keyword_density': analyze_vebapi_keyword_density(keyword, location)
        }
        current_progress += progress_increment
        progress_bar.progress(min(int(current_progress), 100))

    status_text.text("✅ Analysis complete!")
    time.sleep(0.5)
    progress_bar.empty()
    status_text.empty()

    return results

# Header
st.markdown('<div class="main-header">🔍 SEO Analysis Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Comprehensive SEO & Backlink Analysis Tool</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")

    domain = st.text_input(
        "🌐 Domain",
        placeholder="example.com",
        help="Enter domain without http:// or www."
    )

    location = st.selectbox(
        "📍 Location",
        ["DK", "US", "GB", "DE", "SE", "NO", "FR", "ES", "IT"],
        help="Select target country"
    )

    language = st.selectbox(
        "🗣️ Language",
        ["da", "en", "de", "sv", "no", "fr", "es", "it"],
        help="Select target language"
    )

    st.markdown("---")

    st.subheader("📊 Data Sources")

    use_sitemap = st.checkbox("🗺️ Sitemap Crawler", value=True, help="Crawl website sitemap for page count")
    use_moz = st.checkbox("📈 Moz API", value=True, help="Domain Authority and Page Authority")
    use_ahrefs = st.checkbox("🔗 Ahrefs API", value=True, help="Domain Rating and backlink data")
    use_similarweb = st.checkbox("📊 SimilarWeb API", value=True, help="Traffic and visitor data")
    use_seo_api = st.checkbox("🔍 SEO API", value=True, help="Detailed backlink analysis")
    use_google = st.checkbox("🔑 Google Keywords", value=True, help="Keyword research and suggestions")
    use_vebapi = st.checkbox("🚀 VebAPI", value=True, help="Additional SEO tools and keyword research")
    
    vebapi_keyword = None
    if use_vebapi:
        vebapi_keyword = st.text_input(
            "🔑 VebAPI Keyword (optional)",
            placeholder="Leave empty to use domain name",
            help="Keyword for VebAPI analysis. Defaults to domain name if empty."
        )

    st.markdown("---")

    analyze_button = st.button("🔍 Analyze Domain", type="primary", use_container_width=True)

    if analyze_button and domain:
        domain = domain.replace("https://", "").replace("http://", "").replace("www.", "").rstrip("/")

        with st.spinner("Analyzing..."):
            st.session_state.analysis_data = run_analysis(
                domain, location, language,
                use_sitemap, use_moz, use_ahrefs,
                use_similarweb, use_seo_api, use_google, use_vebapi, vebapi_keyword
            )
            st.session_state.domain = domain
    
    st.markdown("---")
    st.markdown("### 📊 Data Sources")
    st.markdown("""
    - ✅ Moz API
    - ✅ Ahrefs API
    - ✅ SimilarWeb API
    - ✅ SEO API
    - ✅ Google Keywords
    - ✅ VebAPI
    - ✅ Custom Crawler
    """)

# Main content
if st.session_state.analysis_data:
    data = st.session_state.analysis_data
    domain = st.session_state.domain
    
    # Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if 'moz' in data and data['moz']['success']:
            da = data['moz']['data'].get('domain_authority', 0)
            st.metric("Domain Authority", da, delta=None, help="Moz Domain Authority")
        else:
            st.metric("Domain Authority", "N/A")
    
    with col2:
        if 'ahrefs' in data and data['ahrefs']['success']:
            dr = data['ahrefs']['data'].get('domainRating', 0)
            st.metric("Domain Rating", dr, delta=None, help="Ahrefs Domain Rating")
        else:
            st.metric("Domain Rating", "N/A")
    
    with col3:
        if 'similarweb' in data and data['similarweb']['success']:
            visits = data['similarweb']['data'].get('visits', {})
            if visits:
                latest_month = list(visits.keys())[-1]
                latest_visits = visits[latest_month]
                st.metric("Monthly Visits", f"{latest_visits:,}", delta=None, help=f"SimilarWeb - {latest_month}")
            else:
                st.metric("Monthly Visits", "N/A")
        else:
            st.metric("Monthly Visits", "N/A")
    
    with col4:
        if 'sitemap' in data and data['sitemap']['success']:
            pages = data['sitemap']['pages']
            st.metric("Pages Indexed", pages, delta=None, help="From sitemap")
        else:
            st.metric("Pages Indexed", "N/A")
    
    st.markdown("---")
    
    # Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Overview", "🔗 Backlinks", "🔑 Keywords", "📈 Traffic", "📄 Technical"])
    
    with tab1:
        st.subheader("📊 Overview")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Authority Metrics")
            
            if 'moz' in data and 'ahrefs' in data and data['moz']['success'] and data['ahrefs']['success']:
                fig = go.Figure(data=[
                    go.Bar(name='Moz DA', x=['Domain Authority'], y=[data['moz']['data'].get('domain_authority', 0)]),
                    go.Bar(name='Ahrefs DR', x=['Domain Rating'], y=[data['ahrefs']['data'].get('domainRating', 0)])
                ])
                fig.update_layout(barmode='group', height=300)
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### Backlink Overview")
            
            if 'seo_api' in data and data['seo_api']['success']:
                overview = data['seo_api']['data'].get('overview', {})
                st.write(f"**Total Backlinks:** {overview.get('backlinks', 0):,}")
                st.write(f"**Referring Domains:** {overview.get('referringDomains', 0):,}")
                st.write(f"**Dofollow:** {overview.get('dofollowBacklinks', {}).get('percentage', 0)}%")
    
    with tab2:
        st.subheader("🔗 Backlink Profile")
        
        if 'seo_api' in data and data['seo_api']['success']:
            seo_data = data['seo_api']['data']
            overview = seo_data.get('overview', {})
            backlinks = seo_data.get('backlinks', [])
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Backlinks", f"{overview.get('backlinks', 0):,}")
            col2.metric("Referring Domains", f"{overview.get('referringDomains', 0):,}")
            col3.metric("Domain Rating", overview.get('domainRating', 0))
            
            if backlinks:
                st.markdown("### Top Backlinks")
                df_backlinks = pd.DataFrame([
                    {
                        "Anchor": bl.get('anchor', 'N/A')[:50],
                        "DR": bl.get('domainRating', 0),
                        "From": bl.get('urlFrom', 'N/A')[:60],
                        "To": bl.get('urlTo', 'N/A')[:60]
                    }
                    for bl in backlinks[:20]
                ])
                st.dataframe(df_backlinks, use_container_width=True, height=400)
        else:
            st.info("No backlink data available")
    
    with tab3:
        st.subheader("🔑 Keyword Analysis")
        
        if 'google' in data and data['google']['success']:
            keywords = data['google']['data']
            
            if keywords:
                st.markdown(f"### Found {len(keywords)} Keywords")
                df_keywords = pd.DataFrame([
                    {
                        "Keyword": kw.get('text', 'N/A'),
                        "Volume": kw.get('volume', 0),
                        "Competition": kw.get('competition_level', 'N/A'),
                        "CPC": f"${kw.get('low_bid', 0):.2f} - ${kw.get('high_bid', 0):.2f}",
                        "Trend": f"{kw.get('trend', 0):.1f}%"
                    }
                    for kw in keywords[:30]
                ])
                st.dataframe(df_keywords, use_container_width=True, height=400)
                
                st.markdown("### Top Keywords by Volume")
                top_keywords = sorted(keywords[:20], key=lambda x: x.get('volume', 0), reverse=True)[:10]
                fig = px.bar(
                    x=[kw.get('text', '') for kw in top_keywords],
                    y=[kw.get('volume', 0) for kw in top_keywords],
                    labels={'x': 'Keyword', 'y': 'Search Volume'},
                    title="Top 10 Keywords"
                )
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No keyword data available")
    
    with tab4:
        st.subheader("📈 Traffic Analysis")
        
        if 'similarweb' in data and data['similarweb']['success']:
            sw_data = data['similarweb']['data']
            visits = sw_data.get('visits', {})
            
            if visits:
                st.markdown("### Traffic Trend")
                df_traffic = pd.DataFrame([
                    {"Month": month, "Visits": count}
                    for month, count in visits.items()
                ])
                fig = px.line(df_traffic, x='Month', y='Visits', title='Monthly Visits', markers=True)
                st.plotly_chart(fig, use_container_width=True)
                
                latest_month = list(visits.keys())[-1]
                latest_visits = visits[latest_month]
                
                col1, col2, col3 = st.columns(3)
                col1.metric("Latest Month", latest_month)
                col2.metric("Visits", f"{latest_visits:,}")
                
                if len(visits) > 1:
                    prev_month = list(visits.keys())[-2]
                    prev_visits = visits[prev_month]
                    growth = ((latest_visits - prev_visits) / prev_visits * 100) if prev_visits > 0 else 0
                    col3.metric("Growth", f"{growth:+.1f}%")
        else:
            st.info("No traffic data available")
    
    with tab5:
        st.subheader("📄 Technical SEO")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Sitemap Analysis")
            
            if 'sitemap' in data and data['sitemap']['success']:
                st.success(f"✅ Sitemap found")
                st.write(f"**Total Pages:** {data['sitemap']['pages']}")
                
                if data['sitemap']['urls']:
                    with st.expander("View Sample URLs"):
                        for url in data['sitemap']['urls'][:10]:
                            st.text(url)
            else:
                st.error(f"❌ Sitemap error: {data.get('sitemap', {}).get('error', 'Unknown')}")
        
        with col2:
            st.markdown("### API Status")
            
            apis = [
                ("Moz", data.get('moz', {}).get('success', False)),
                ("Ahrefs", data.get('ahrefs', {}).get('success', False)),
                ("SimilarWeb", data.get('similarweb', {}).get('success', False)),
                ("SEO API", data.get('seo_api', {}).get('success', False)),
                ("Google Keywords", data.get('google', {}).get('success', False)),
                ("VebAPI", data.get('vebapi', {}).get('keyword_research', {}).get('success', False))
            ]
            
            for api_name, status in apis:
                if status:
                    st.success(f"✅ {api_name}")
                else:
                    st.error(f"❌ {api_name}")
    
    # Export section
    st.markdown("---")
    st.subheader("📥 Export Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📄 Export as JSON", use_container_width=True):
            json_str = json.dumps(data, indent=2)
            st.download_button(
                label="Download JSON",
                data=json_str,
                file_name=f"{domain}_seo_analysis.json",
                mime="application/json"
            )
    
    with col2:
        if st.button("📊 Export Summary", use_container_width=True):
            summary = f"""
SEO Analysis Report for {domain}
Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}

=== METRICS ===
Domain Authority (Moz): {data.get('moz', {}).get('data', {}).get('domain_authority', 'N/A')}
Domain Rating (Ahrefs): {data.get('ahrefs', {}).get('data', {}).get('domainRating', 'N/A')}
Total Backlinks: {data.get('seo_api', {}).get('data', {}).get('overview', {}).get('backlinks', 'N/A')}
Referring Domains: {data.get('seo_api', {}).get('data', {}).get('overview', {}).get('referringDomains', 'N/A')}
Pages Indexed: {data.get('sitemap', {}).get('pages', 'N/A')}

=== API STATUS ===
"""
            for api_name, status in apis:
                summary += f"{api_name}: {'✅ Success' if status else '❌ Failed'}\n"
            
            st.download_button(
                label="Download Summary",
                data=summary,
                file_name=f"{domain}_summary.txt",
                mime="text/plain"
            )

else:
    st.info("👈 Enter a domain and click 'Analyze Domain' to start")
    
    st.markdown("---")
    st.markdown("### 🎯 Features")
    st.markdown("""
    - **Domain Authority** - Moz DA & Ahrefs DR metrics
    - **Backlink Analysis** - Comprehensive backlink profile
    - **Keyword Research** - Google keyword suggestions
    - **Traffic Analysis** - SimilarWeb visitor data
    - **Technical SEO** - Sitemap crawling & analysis
    - **VebAPI Integration** - Additional SEO tools
    - **Export Options** - JSON & text export
    """)
    
    st.markdown("---")
    st.markdown("### 📊 Supported APIs")
    st.markdown("""
    1. **Moz API** - Domain & Page Authority
    2. **Ahrefs API** - Domain Rating & Backlinks
    3. **SimilarWeb API** - Traffic & Engagement
    4. **SEO API** - Backlink Analysis
    5. **Google Keywords API** - Keyword Research
    6. **VebAPI** - Comprehensive SEO Tools
    7. **Custom Crawler** - Sitemap Analysis
    """)
