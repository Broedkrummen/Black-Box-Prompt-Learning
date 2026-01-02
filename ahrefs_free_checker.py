import urllib.request
import urllib.parse
import json
import time
import re
from html.parser import HTMLParser

class AhrefsBacklinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.backlinks = []
        self.current_backlink = {}
        self.in_backlink_row = False
        self.current_tag = None
        self.current_data = ""
        
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        
        # Detect backlink rows
        if 'class' in attrs_dict and 'backlink' in attrs_dict.get('class', '').lower():
            self.in_backlink_row = True
            self.current_backlink = {}
        
        # Capture links
        if tag == 'a' and self.in_backlink_row:
            href = attrs_dict.get('href', '')
            if href and not href.startswith('#'):
                if 'url_from' not in self.current_backlink:
                    self.current_backlink['url_from'] = href
                elif 'url_to' not in self.current_backlink:
                    self.current_backlink['url_to'] = href
        
        self.current_tag = tag
    
    def handle_data(self, data):
        if self.in_backlink_row and data.strip():
            self.current_data += data.strip() + " "
    
    def handle_endtag(self, tag):
        if self.in_backlink_row and tag == 'tr':
            if self.current_backlink:
                self.current_backlink['data'] = self.current_data.strip()
                self.backlinks.append(self.current_backlink)
            self.in_backlink_row = False
            self.current_data = ""

def fetch_ahrefs_free_backlinks(domain):
    """
    Fetch backlinks from Ahrefs free backlink checker
    Note: This uses browser_action tool for automation
    """
    print(f"\n🔍 Fetching backlinks from Ahrefs Free Backlink Checker...")
    print(f"   Target: {domain}")
    print("\n⚠️  Note: This requires browser automation")
    print("   The free checker shows top 100 backlinks")
    
    # Instructions for manual use
    print("\n" + "=" * 80)
    print("AUTOMATED BROWSER APPROACH")
    print("=" * 80)
    print("\nThis script will use browser automation to:")
    print("1. Open https://ahrefs.com/backlink-checker")
    print("2. Enter the domain")
    print("3. Wait for results to load")
    print("4. Extract backlink data")
    print("5. Save to file")
    
    return None

def manual_instructions(domain):
    """Provide manual instructions for using Ahrefs free checker"""
    print("\n" + "=" * 80)
    print("MANUAL INSTRUCTIONS")
    print("=" * 80)
    print(f"\n1. Visit: https://ahrefs.com/backlink-checker")
    print(f"2. Enter domain: {domain}")
    print("3. Click 'Check backlinks'")
    print("4. Wait for results (shows top 100 backlinks)")
    print("5. You'll see:")
    print("   - Domain Rating (DR)")
    print("   - Total backlinks")
    print("   - Referring domains")
    print("   - Top 100 backlinks with:")
    print("     * Source URL")
    print("     * Domain Rating")
    print("     * URL Rating")
    print("     * Anchor text")
    print("     * Traffic")
    print("\n💡 TIP: For automated access, use Ahrefs Webmaster Tools API")
    print("   Sign up at: https://ahrefs.com/webmaster-tools")

def create_browser_automation_script(domain):
    """Create a browser automation script"""
    script = f'''
# Browser Automation Script for Ahrefs Free Backlink Checker
# This script uses the browser_action tool

Steps:
1. Launch browser at https://ahrefs.com/backlink-checker
2. Wait for page to load
3. Find input field and enter: {domain}
4. Click "Check backlinks" button
5. Wait for results to load (may take 10-30 seconds)
6. Extract data from results table
7. Save to file

Note: This requires the browser_action tool which is available in the main conversation.
'''
    return script

def main():
    print("=" * 80)
    print("AHREFS FREE BACKLINK CHECKER")
    print("=" * 80)
    
    # Get domain from user
    domain = input("\nEnter domain to check (e.g., simplybeyond.dk): ").strip()
    
    if not domain:
        domain = "simplybeyond.dk"
        print(f"Using default domain: {domain}")
    
    print("\n📋 OPTIONS:")
    print("1. Use browser automation (requires browser_action tool)")
    print("2. Show manual instructions")
    print("3. Create automation script for later use")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        print("\n⚠️  Browser automation requires the browser_action tool")
        print("   This tool is available in the main BLACKBOX AI conversation")
        print("\n💡 To use browser automation:")
        print("   1. Return to the main conversation")
        print("   2. Ask: 'Use browser automation to check backlinks on Ahrefs'")
        print("   3. The AI will use browser_action to automate the process")
        
        fetch_ahrefs_free_backlinks(domain)
    
    elif choice == "2":
        manual_instructions(domain)
    
    elif choice == "3":
        script = create_browser_automation_script(domain)
        
        with open("ahrefs_automation_script.txt", "w", encoding="utf-8") as f:
            f.write(script)
        
        print("\n✅ Automation script saved to: ahrefs_automation_script.txt")
        print("\n📝 To use this script:")
        print("   1. Return to main BLACKBOX AI conversation")
        print("   2. Share the script content")
        print("   3. Ask AI to execute it using browser_action tool")
    
    else:
        print("\n❌ Invalid choice")
    
    print("\n" + "=" * 80)
    print("ALTERNATIVE: AHREFS WEBMASTER TOOLS (RECOMMENDED)")
    print("=" * 80)
    print("\nFor full automated access with more data:")
    print("1. Sign up: https://ahrefs.com/webmaster-tools")
    print("2. Verify domain ownership")
    print("3. Get API token")
    print("4. Run: python ahrefs_backlink_checker.py")
    print("\nBenefits:")
    print("- Unlimited backlink checks")
    print("- Complete backlink data (not just top 100)")
    print("- Historical data")
    print("- Broken link detection")
    print("- And much more!")

if __name__ == "__main__":
    main()
