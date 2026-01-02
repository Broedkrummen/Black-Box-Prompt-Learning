import urllib.request
import urllib.parse
import json
import hashlib
import hmac
import base64
import time

class MozAPI:
    def __init__(self, access_id, secret_key):
        self.access_id = access_id
        self.secret_key = secret_key
        # Using Mozscape API endpoints
        self.api_endpoint = "https://lsapi.seomoz.com/linkscape/url-metrics/"
        self.links_endpoint = "https://lsapi.seomoz.com/linkscape/links/"
        
    def generate_auth_string(self):
        """Generate authentication string for Mozscape API"""
        expires = int(time.time()) + 300  # 5 minutes from now
        string_to_sign = f"{self.access_id}\n{expires}"
        
        # Create HMAC-SHA1 signature
        binary_signature = hmac.new(
            self.secret_key.encode('utf-8'),
            string_to_sign.encode('utf-8'),
            hashlib.sha1
        ).digest()
        
        # Base64 encode the signature
        signature = base64.b64encode(binary_signature).decode('utf-8')
        
        # Return the authentication parameters
        return {
            'AccessID': self.access_id,
            'Expires': expires,
            'Signature': signature
        }
    
    def get_url_metrics(self, url):
        """Get URL metrics including Domain Authority, Page Authority, etc."""
        try:
            print(f"\n🔍 Fetching URL metrics for {url}...")
            
            auth_params = self.generate_auth_string()
            
            # Cols parameter: 103079231492 gets DA, PA, links, etc.
            # See: https://moz.com/help/links-api/making-calls/url-metrics
            params = {
                'Cols': '103079231492',
                'AccessID': auth_params['AccessID'],
                'Expires': auth_params['Expires'],
                'Signature': auth_params['Signature']
            }
            
            encoded_url = urllib.parse.quote(url, safe='')
            query_string = urllib.parse.urlencode(params)
            full_url = f"{self.api_endpoint}{encoded_url}?{query_string}"
            
            req = urllib.request.Request(full_url)
            
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode('utf-8'))
            
            print(f"✅ Successfully fetched URL metrics")
            return result
            
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8')
            print(f"❌ HTTP Error {e.code}: {error_body}")
            return None
        except Exception as e:
            print(f"❌ Error fetching URL metrics: {e}")
            return None
    
    def get_backlinks(self, url, limit=100):
        """Get backlinks for a URL"""
        try:
            print(f"\n🔍 Fetching backlinks for {url}...")
            
            auth_params = self.generate_auth_string()
            
            # Scope: page_to_page, Sort: page_authority
            params = {
                'Scope': 'page_to_page',
                'Sort': 'page_authority',
                'Limit': limit,
                'SourceCols': '536870916',  # Get source URL metrics
                'TargetCols': '4',  # Get target URL
                'LinkCols': '2',  # Get anchor text
                'AccessID': auth_params['AccessID'],
                'Expires': auth_params['Expires'],
                'Signature': auth_params['Signature']
            }
            
            encoded_url = urllib.parse.quote(url, safe='')
            query_string = urllib.parse.urlencode(params)
            full_url = f"{self.links_endpoint}{encoded_url}?{query_string}"
            
            req = urllib.request.Request(full_url)
            
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode('utf-8'))
            
            # Result is an array of links
            print(f"✅ Successfully fetched {len(result)} backlinks")
            return result
            
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8')
            print(f"❌ HTTP Error {e.code}: {error_body}")
            return None
        except Exception as e:
            print(f"❌ Error fetching backlinks: {e}")
            return None
    
    def get_anchor_text(self, url):
        """Get anchor text data for a URL"""
        try:
            print(f"\n🔍 Fetching anchor text data for {url}...")
            
            auth_params = self.generate_auth_string()
            
            # Get anchor text endpoint
            anchor_endpoint = "https://lsapi.seomoz.com/linkscape/anchor-text/"
            
            params = {
                'Scope': 'phrase_to_page',
                'Sort': 'domains_linking_page',
                'Cols': '2',  # Anchor text
                'AccessID': auth_params['AccessID'],
                'Expires': auth_params['Expires'],
                'Signature': auth_params['Signature']
            }
            
            encoded_url = urllib.parse.quote(url, safe='')
            query_string = urllib.parse.urlencode(params)
            full_url = f"{anchor_endpoint}{encoded_url}?{query_string}"
            
            req = urllib.request.Request(full_url)
            
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode('utf-8'))
            
            print(f"✅ Successfully fetched anchor text data")
            return result
            
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8')
            print(f"❌ HTTP Error {e.code}: {error_body}")
            return None
        except Exception as e:
            print(f"❌ Error fetching anchor text: {e}")
            return None

def generate_moz_report(domain, url_metrics, backlinks, anchor_text):
    """Generate comprehensive Moz backlink report"""
    report = []
    report.append("=" * 80)
    report.append("MOZ BACKLINK ANALYSIS REPORT")
    report.append("=" * 80)
    report.append(f"\nDomain: {domain}")
    report.append(f"Analysis Date: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("")
    
    # URL Metrics
    if url_metrics:
        report.append("\n" + "=" * 80)
        report.append("DOMAIN METRICS")
        report.append("=" * 80)
        report.append(f"\nDomain Authority (DA): {url_metrics.get('pda', 'N/A')}")
        report.append(f"Page Authority (PA): {url_metrics.get('upa', 'N/A')}")
        report.append(f"MozRank: {url_metrics.get('umrp', 'N/A')}")
        report.append(f"MozTrust: {url_metrics.get('utrp', 'N/A')}")
        report.append(f"External Links: {url_metrics.get('ueid', 'N/A')}")
        report.append(f"Links to Root Domain: {url_metrics.get('uid', 'N/A')}")
    
    # Backlinks
    if backlinks and isinstance(backlinks, list):
        report.append("\n" + "=" * 80)
        report.append(f"BACKLINKS ({len(backlinks)} found)")
        report.append("=" * 80)
        
        for i, link in enumerate(backlinks[:50], 1):  # Show first 50
            report.append(f"\n{i}. Source: {link.get('uu', 'N/A')}")
            report.append(f"   Target: {link.get('lu', 'N/A')}")
            report.append(f"   Anchor Text: {link.get('lt', 'N/A')}")
            report.append(f"   Source Page Authority: {link.get('upa', 'N/A')}")
            report.append(f"   Source Domain Authority: {link.get('pda', 'N/A')}")
        
        if len(backlinks) > 50:
            report.append(f"\n... and {len(backlinks) - 50} more backlinks")
    
    # Anchor Text
    if anchor_text and isinstance(anchor_text, list):
        report.append("\n" + "=" * 80)
        report.append(f"TOP ANCHOR TEXTS ({len(anchor_text)} found)")
        report.append("=" * 80)
        
        for i, anchor in enumerate(anchor_text[:20], 1):  # Show top 20
            report.append(f"\n{i}. \"{anchor.get('apmt', 'N/A')}\"")
            report.append(f"   Internal Pages: {anchor.get('aimp', 'N/A')}")
            report.append(f"   External Pages: {anchor.get('aemp', 'N/A')}")
    
    return "\n".join(report)

def main():
    print("=" * 80)
    print("MOZ API BACKLINK CHECKER")
    print("=" * 80)
    
    # Get API credentials from user
    print("\nPlease enter your Moz API credentials:")
    print("(You can find these at: https://moz.com/products/api/keys)")
    
    access_id = input("\nMoz Access ID: ").strip()
    secret_key = input("Moz Secret Key: ").strip()
    
    if not access_id or not secret_key:
        print("\n❌ Error: Both Access ID and Secret Key are required!")
        return
    
    domain = "https://simplybeyond.dk"
    
    # Initialize Moz API
    moz = MozAPI(access_id, secret_key)
    
    # Fetch data
    print("\n" + "=" * 80)
    print("FETCHING DATA FROM MOZ API")
    print("=" * 80)
    
    url_metrics = moz.get_url_metrics(domain)
    time.sleep(1)  # Rate limiting
    
    backlinks = moz.get_backlinks(domain, limit=100)
    time.sleep(1)  # Rate limiting
    
    anchor_text = moz.get_anchor_text(domain)
    
    # Generate report
    if url_metrics or backlinks or anchor_text:
        report = generate_moz_report(domain, url_metrics, backlinks, anchor_text)
        
        # Save report
        with open("moz_backlink_report.txt", "w", encoding="utf-8") as f:
            f.write(report)
        
        # Save raw JSON data
        with open("moz_backlink_data.json", "w", encoding="utf-8") as f:
            json.dump({
                "url_metrics": url_metrics,
                "backlinks": backlinks,
                "anchor_text": anchor_text
            }, f, indent=2)
        
        print("\n" + "=" * 80)
        print("✅ MOZ BACKLINK ANALYSIS COMPLETE!")
        print("=" * 80)
        print("\n📄 Reports saved:")
        print("   - moz_backlink_report.txt (Human-readable report)")
        print("   - moz_backlink_data.json (Raw JSON data)")
        
        # Print summary
        if url_metrics:
            print("\n📊 Quick Summary:")
            print(f"   Domain Authority: {url_metrics.get('pda', 'N/A')}")
            print(f"   Page Authority: {url_metrics.get('upa', 'N/A')}")
            print(f"   MozRank: {url_metrics.get('umrp', 'N/A')}")
        
        if backlinks and isinstance(backlinks, list):
            print(f"   Total Backlinks Found: {len(backlinks)}")
    else:
        print("\n❌ Failed to fetch data from Moz API")
        print("Please check your API credentials and try again")

if __name__ == "__main__":
    main()
