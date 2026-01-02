"""
SEO Analysis Dashboard - Flask Version
Web-based dashboard with custom HTML/CSS/JS interface
"""

from flask import Flask, render_template, request, jsonify
import http.client
import json
import time
import hashlib
import hmac
import base64
from urllib.parse import quote
import xml.etree.ElementTree as ET

app = Flask(__name__)

# API Configuration
RAPIDAPI_KEY = "5c359bb774msh32eed0a33c585c4p1466d6jsn5620b810b2f7"
MOZ_ACCESS_ID = "mozscape-c7fe158e8e"
MOZ_SECRET_KEY = "e0c2a5e8e0e44f5e8c7fe158e8e0c2a5"

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

@app.route('/')
def index():
    """Render main page"""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """Run analysis"""
    data = request.json
    domain = data.get('domain', '').replace("https://", "").replace("http://", "").replace("www.", "").rstrip("/")
    location = data.get('location', 'DK')
    language = data.get('language', 'da')
    
    if not domain:
        return jsonify({"error": "Domain is required"}), 400
    
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
    
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
