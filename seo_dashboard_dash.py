"""
SEO Analysis Dashboard - Dash (Plotly) Version
Professional interactive dashboard with advanced visualizations
"""

import dash
from dash import dcc, html, Input, Output, State, dash_table
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

# Initialize Dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = "SEO Analysis Dashboard"

# API Configuration
RAPIDAPI_KEY = "5c359bb774msh32eed0a33c585c4p1466d6jsn5620b810b2f7"
MOZ_ACCESS_ID = "mozscape-c7fe158e8e"
MOZ_SECRET_KEY = "e0c2a5e8e0e44f5e8c7fe158e8e0c2a5"

# Styles
colors = {
    'background': '#f8f9fa',
    'text': '#212529',
    'primary': '#1f77b4',
    'secondary': '#6c757d',
    'success': '#28a745',
    'danger': '#dc3545',
    'card': '#ffffff'
}

# Analysis functions (same as Streamlit version)
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
        
        conn.request("GET", f"/domain-rating/?domain={domain}", headers=headers)
        res = conn.getresponse()
        data = json.loads(res.read().decode("utf-8"))
        
        if "domainRating" in data:
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
        
        conn.request("GET", f"/backlinks/?domain={domain}&country={location.lower()}", headers=headers)
        res = conn.getresponse()
        data = json.loads(res.read().decode("utf-8"))
        
        if "overview" in data:
            return {"success": True, "data": data}
        else:
            return {"success": False, "error": data}
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

def run_analysis(domain, location, language):
    """Run complete analysis"""
    results = {}
    
    results['sitemap'] = crawl_sitemap(domain)
    time.sleep(0.5)
    
    results['moz'] = analyze_moz(domain)
    time.sleep(1)
    
    results['ahrefs'] = analyze_ahrefs(domain)
    time.sleep(1)
    
    results['similarweb'] = analyze_similarweb(domain)
    time.sleep(1)
    
    results['seo_api'] = analyze_seo_api(domain, location)
    time.sleep(1)
    
    results['google'] = analyze_google_keywords(domain, location, language)
    
    return results

# Layout
app.layout = html.Div([
    # Header
    html.Div([
        html.H1("🔍 SEO Analysis Dashboard", 
                style={'textAlign': 'center', 'color': colors['primary'], 'marginBottom': '10px'}),
        html.P("Comprehensive SEO & Backlink Analysis Tool",
               style={'textAlign': 'center', 'color': colors['secondary'], 'marginBottom': '30px'})
    ], style={'backgroundColor': colors['card'], 'padding': '20px', 'marginBottom': '20px', 'borderRadius': '10px'}),
    
    # Input Section
    html.Div([
        html.Div([
            html.Label("🌐 Domain:", style={'fontWeight': 'bold'}),
            dcc.Input(
                id='domain-input',
                type='text',
                placeholder='example.com',
                style={'width': '100%', 'padding': '10px', 'borderRadius': '5px', 'border': '1px solid #ddd'}
            )
        ], style={'width': '30%', 'display': 'inline-block', 'marginRight': '2%'}),
        
        html.Div([
            html.Label("📍 Location:", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='location-dropdown',
                options=[
                    {'label': 'Denmark', 'value': 'DK'},
                    {'label': 'United States', 'value': 'US'},
                    {'label': 'United Kingdom', 'value': 'GB'},
                    {'label': 'Germany', 'value': 'DE'},
                    {'label': 'Sweden', 'value': 'SE'},
                    {'label': 'Norway', 'value': 'NO'}
                ],
                value='DK',
                style={'borderRadius': '5px'}
            )
        ], style={'width': '20%', 'display': 'inline-block', 'marginRight': '2%'}),
        
        html.Div([
            html.Label("🗣️ Language:", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='language-dropdown',
                options=[
                    {'label': 'Danish', 'value': 'da'},
                    {'label': 'English', 'value': 'en'},
                    {'label': 'German', 'value': 'de'},
                    {'label': 'Swedish', 'value': 'sv'},
                    {'label': 'Norwegian', 'value': 'no'}
                ],
                value='da',
                style={'borderRadius': '5px'}
            )
        ], style={'width': '20%', 'display': 'inline-block', 'marginRight': '2%'}),
        
        html.Div([
            html.Label("\u00A0", style={'fontWeight': 'bold'}),  # Spacer
            html.Button('🔍 Analyze', id='analyze-button', n_clicks=0,
                       style={'width': '100%', 'padding': '10px', 'backgroundColor': colors['primary'],
                              'color': 'white', 'border': 'none', 'borderRadius': '5px',
                              'cursor': 'pointer', 'fontWeight': 'bold'})
        ], style={'width': '20%', 'display': 'inline-block', 'verticalAlign': 'bottom'})
    ], style={'backgroundColor': colors['card'], 'padding': '20px', 'marginBottom': '20px', 'borderRadius': '10px'}),
    
    # Data Source Checkboxes
    html.Div([
        html.H4("📊 Select Data Sources:", style={'marginBottom': '15px', 'color': colors['primary']}),
        html.Div([
            dcc.Checklist(
                id='sitemap-check',
                options=[{'label': '🗺️ Sitemap Crawler', 'value': 'sitemap'}],
                value=['sitemap'],
                style={'marginBottom': '10px'}
            ),
            dcc.Checklist(
                id='moz-check',
                options=[{'label': '📈 Moz API', 'value': 'moz'}],
                value=['moz'],
                style={'marginBottom': '10px'}
            ),
            dcc.Checklist(
                id='ahrefs-check',
                options=[{'label': '🔗 Ahrefs API', 'value': 'ahrefs'}],
                value=['ahrefs'],
                style={'marginBottom': '10px'}
            ),
            dcc.Checklist(
                id='similarweb-check',
                options=[{'label': '📊 SimilarWeb API', 'value': 'similarweb'}],
                value=['similarweb'],
                style={'marginBottom': '10px'}
            ),
            dcc.Checklist(
                id='seo-api-check',
                options=[{'label': '🔍 SEO API', 'value': 'seo_api'}],
                value=['seo_api'],
                style={'marginBottom': '10px'}
            ),
            dcc.Checklist(
                id='google-check',
                options=[{'label': '🔑 Google Keywords', 'value': 'google'}],
                value=['google'],
                style={'marginBottom': '10px'}
            )
        ], style={'display': 'grid', 'gridTemplateColumns': 'repeat(2, 1fr)', 'gap': '10px'})
    ], style={'backgroundColor': colors['card'], 'padding': '20px', 'marginBottom': '20px', 'borderRadius': '10px'}),
    
    # Loading
    dcc.Loading(
        id="loading",
        type="default",
        children=[
            html.Div(id='loading-output')
        ]
    ),
    
    # Results
    html.Div(id='results-container')
    
], style={'backgroundColor': colors['background'], 'padding': '20px', 'fontFamily': 'Arial, sans-serif'})

# Callback
@app.callback(
    [Output('results-container', 'children'),
     Output('loading-output', 'children')],
    [Input('analyze-button', 'n_clicks')],
    [State('domain-input', 'value'),
     State('location-dropdown', 'value'),
     State('language-dropdown', 'value'),
     State('sitemap-check', 'value'),
     State('moz-check', 'value'),
     State('ahrefs-check', 'value'),
     State('similarweb-check', 'value'),
     State('seo-api-check', 'value'),
     State('google-check', 'value')]
)
def update_results(n_clicks, domain, location, language, sitemap_check, moz_check, ahrefs_check, similarweb_check, seo_api_check, google_check):
    if n_clicks == 0 or not domain:
        return html.Div([
            html.Div([
                html.H3("👋 Welcome!", style={'color': colors['primary']}),
                html.P("Enter a domain above and click 'Analyze' to get started."),
                html.Hr(),
                html.H4("📊 Features:"),
                html.Ul([
                    html.Li("Domain Authority & Rating metrics"),
                    html.Li("Comprehensive backlink analysis"),
                    html.Li("Keyword research and volume data"),
                    html.Li("Traffic trends and engagement"),
                    html.Li("Technical SEO analysis")
                ])
            ], style={'backgroundColor': colors['card'], 'padding': '30px', 'borderRadius': '10px'})
        ]), ""

    # Clean domain
    domain = domain.replace("https://", "").replace("http://", "").replace("www.", "").rstrip("/")

    # Convert checkbox values to booleans
    use_sitemap = 'sitemap' in (sitemap_check or [])
    use_moz = 'moz' in (moz_check or [])
    use_ahrefs = 'ahrefs' in (ahrefs_check or [])
    use_similarweb = 'similarweb' in (similarweb_check or [])
    use_seo_api = 'seo_api' in (seo_api_check or [])
    use_google = 'google' in (google_check or [])

    # Check if at least one data source is selected
    if not any([use_sitemap, use_moz, use_ahrefs, use_similarweb, use_seo_api, use_google]):
        return html.Div([
            html.Div([
                html.H3("⚠️ No Data Sources Selected", style={'color': colors['danger']}),
                html.P("Please select at least one data source to analyze.")
            ], style={'backgroundColor': colors['card'], 'padding': '30px', 'borderRadius': '10px'})
        ]), ""

    # Run analysis with selected sources
    data = run_analysis(domain, location, language, use_sitemap, use_moz, use_ahrefs, use_similarweb, use_seo_api, use_google)
    
    # Metric cards
    metrics_row = html.Div([
        html.Div([
            html.H3(data['moz']['data'].get('domain_authority', 'N/A') if data['moz']['success'] else 'N/A',
                   style={'color': colors['primary'], 'marginBottom': '5px'}),
            html.P("Domain Authority", style={'color': colors['secondary'], 'margin': '0'})
        ], style={'backgroundColor': colors['card'], 'padding': '20px', 'borderRadius': '10px',
                 'textAlign': 'center', 'width': '23%', 'display': 'inline-block', 'marginRight': '2%'}),
        
        html.Div([
            html.H3(data['ahrefs']['data'].get('domainRating', 'N/A') if data['ahrefs']['success'] else 'N/A',
                   style={'color': colors['primary'], 'marginBottom': '5px'}),
            html.P("Domain Rating", style={'color': colors['secondary'], 'margin': '0'})
        ], style={'backgroundColor': colors['card'], 'padding': '20px', 'borderRadius': '10px',
                 'textAlign': 'center', 'width': '23%', 'display': 'inline-block', 'marginRight': '2%'}),
        
        html.Div([
            html.H3(f"{list(data['similarweb']['data'].get('visits', {}).values())[-1]:,}" if data['similarweb']['success'] and data['similarweb']['data'].get('visits') else 'N/A',
                   style={'color': colors['primary'], 'marginBottom': '5px'}),
            html.P("Monthly Visits", style={'color': colors['secondary'], 'margin': '0'})
        ], style={'backgroundColor': colors['card'], 'padding': '20px', 'borderRadius': '10px',
                 'textAlign': 'center', 'width': '23%', 'display': 'inline-block', 'marginRight': '2%'}),
        
        html.Div([
            html.H3(data['sitemap']['pages'] if data['sitemap']['success'] else 'N/A',
                   style={'color': colors['primary'], 'marginBottom': '5px'}),
            html.P("Pages Indexed", style={'color': colors['secondary'], 'margin': '0'})
        ], style={'backgroundColor': colors['card'], 'padding': '20px', 'borderRadius': '10px',
                 'textAlign': 'center', 'width': '23%', 'display': 'inline-block'})
    ], style={'marginBottom': '20px'})
    
    # Charts
    charts_section = html.Div([
        # Authority comparison
        html.Div([
            dcc.Graph(
                figure=go.Figure(data=[
                    go.Bar(name='Moz DA', x=['Authority'], y=[data['moz']['data'].get('domain_authority', 0) if data['moz']['success'] else 0]),
                    go.Bar(name='Ahrefs DR', x=['Authority'], y=[data['ahrefs']['data'].get('domainRating', 0) if data['ahrefs']['success'] else 0])
                ]).update_layout(title='Authority Metrics', barmode='group', height=300)
            )
        ], style={'backgroundColor': colors['card'], 'padding': '20px', 'borderRadius': '10px',
                 'width': '48%', 'display': 'inline-block', 'marginRight': '2%'}),
        
        # Backlinks
        html.Div([
            dcc.Graph(
                figure=go.Figure(data=[
                    go.Indicator(
                        mode="number+delta",
                        value=data['seo_api']['data'].get('overview', {}).get('backlinks', 0) if data['seo_api']['success'] else 0,
                        title={'text': "Total Backlinks"},
                        domain={'x': [0, 1], 'y': [0, 1]}
                    )
                ]).update_layout(height=300)
            )
        ], style={'backgroundColor': colors['card'], 'padding': '20px', 'borderRadius': '10px',
                 'width': '48%', 'display': 'inline-block'})
    ], style={'marginBottom': '20px'})
    
    # Backlinks table
    backlinks_section = html.Div([
        html.H3("🔗 Top Backlinks", style={'color': colors['primary']}),
        dash_table.DataTable(
            data=[
                {
                    "Anchor": bl.get('anchor', 'N/A')[:50],
                    "DR": bl.get('domainRating', 0),
                    "From": bl.get('urlFrom', 'N/A')[:60]
                }
                for bl in data['seo_api']['data'].get('backlinks', [])[:20]
            ] if data['seo_api']['success'] else [],
            columns=[
                {"name": "Anchor", "id": "Anchor"},
                {"name": "DR", "id": "DR"},
                {"name": "From", "id": "From"}
            ],
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'left', 'padding': '10px'},
            style_header={'backgroundColor': colors['primary'], 'color': 'white', 'fontWeight': 'bold'}
        )
    ], style={'backgroundColor': colors['card'], 'padding': '20px', 'borderRadius': '10px', 'marginBottom': '20px'})
    
    return html.Div([metrics_row, charts_section, backlinks_section]), ""

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
