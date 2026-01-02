"""
Ahrefs Free Backlink Checker with Browser Automation
This script will be executed by BLACKBOX AI using the browser_action tool
"""

def check_ahrefs_backlinks(domain):
    """
    Instructions for BLACKBOX AI to automate Ahrefs backlink checking
    """
    instructions = f"""
Please use the browser_action tool to check backlinks for {domain} on Ahrefs:

1. Launch browser at: https://ahrefs.com/backlink-checker

2. Wait for page to load (look for input field)

3. Click on the input field (usually centered on page)
   - Look for input with placeholder like "Enter domain"
   - Coordinates will be around center of page (450, 300)

4. Type the domain: {domain}

5. Click the "Check backlinks" button
   - Usually to the right of input field
   - Look for blue/green button

6. Wait for results to load (10-30 seconds)
   - Page will show loading indicator
   - Results will appear in a table

7. Take screenshot of results showing:
   - Domain Rating (DR)
   - Total backlinks count
   - Referring domains count
   - Top backlinks table with:
     * Source URLs
     * Domain Rating
     * Anchor text
     * Traffic data

8. Scroll down to see more backlinks (if needed)

9. Extract the data and save to file

10. Close browser when done
"""
    return instructions

def main():
    print("=" * 80)
    print("AHREFS BROWSER AUTOMATION CHECKER")
    print("=" * 80)
    
    domain = input("\nEnter domain to check (default: simplybeyond.dk): ").strip()
    if not domain:
        domain = "simplybeyond.dk"
    
    print(f"\n🔍 Preparing to check backlinks for: {domain}")
    print("\n" + "=" * 80)
    print("BROWSER AUTOMATION INSTRUCTIONS")
    print("=" * 80)
    
    instructions = check_ahrefs_backlinks(domain)
    print(instructions)
    
    print("\n" + "=" * 80)
    print("NEXT STEPS")
    print("=" * 80)
    print("\n⚠️  This script provides instructions for browser automation.")
    print("   To execute, you need to:")
    print("\n1. Copy the instructions above")
    print("2. Ask BLACKBOX AI in the main conversation:")
    print(f'   "Use browser_action to check backlinks for {domain} on Ahrefs"')
    print("\n3. The AI will:")
    print("   - Launch a browser")
    print("   - Navigate to Ahrefs")
    print("   - Enter the domain")
    print("   - Extract backlink data")
    print("   - Save results to file")
    
    # Save instructions to file
    with open("ahrefs_browser_instructions.txt", "w", encoding="utf-8") as f:
        f.write(instructions)
    
    print("\n✅ Instructions saved to: ahrefs_browser_instructions.txt")

if __name__ == "__main__":
    main()
