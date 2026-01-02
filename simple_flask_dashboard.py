"""
Simple Flask Dashboard - Minimal Version
For testing if Flask works properly
"""

from flask import Flask, render_template_string, request


app = Flask(__name__)

# HTML template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Simple SEO Dashboard</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #1f77b4;
            text-align: center;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        input, select {
            width: 100%;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        button {
            background-color: #1f77b4;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 4px;
            cursor: pointer;
            font-weight: bold;
        }
        .metrics {
            display: flex;
            justify-content: space-between;
            margin: 20px 0;
        }
        .metric-card {
            background-color: #1f77b4;
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            width: 22%;
        }
        .metric-value {
            font-size: 24px;
            font-weight: bold;
            margin: 10px 0;
        }
        .metric-title {
            font-size: 14px;
            opacity: 0.9;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        th, td {
            padding: 10px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background-color: #f2f2f2;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 Simple SEO Dashboard</h1>
        <p style="text-align: center;">A minimal version to test if Flask is working</p>
        
        <h2>Enter Domain to Analyze</h2>
        <form method="post">
            <div class="form-group">
                <label for="domain">Domain (e.g., example.com)</label>
                <input type="text" id="domain" name="domain" required>
            </div>
            
            <div class="form-group">
                <label for="location">Location</label>
                <select id="location" name="location">
                    <option value="DK">Denmark (DK)</option>
                    <option value="US">United States (US)</option>
                    <option value="GB">United Kingdom (GB)</option>
                    <option value="DE">Germany (DE)</option>
                    <option value="SE">Sweden (SE)</option>
                    <option value="NO">Norway (NO)</option>
                </select>
            </div>
            
            <div class="form-group">
                <label for="language">Language</label>
                <select id="language" name="language">
                    <option value="da">Danish (da)</option>
                    <option value="en">English (en)</option>
                    <option value="de">German (de)</option>
                    <option value="sv">Swedish (sv)</option>
                    <option value="no">Norwegian (no)</option>
                </select>
            </div>
            
            <button type="submit">Analyze</button>
        </form>
        
        {% if domain %}
        <div style="margin-top: 30px;">
            <div style="background-color: #d4edda; color: #155724; padding: 10px; border-radius: 4px; margin-bottom: 20px;">
                Form submitted successfully! Would analyze {{ domain }} in {{ location }} with language {{ language }}
            </div>
            
            <h2>Metrics</h2>
            <div class="metrics">
                <div class="metric-card">
                    <div class="metric-value">42</div>
                    <div class="metric-title">Domain Authority</div>
                </div>
                
                <div class="metric-card">
                    <div class="metric-value">38</div>
                    <div class="metric-title">Domain Rating</div>
                </div>
                
                <div class="metric-card">
                    <div class="metric-value">12,500</div>
                    <div class="metric-title">Monthly Visits</div>
                </div>
                
                <div class="metric-card">
                    <div class="metric-value">158</div>
                    <div class="metric-title">Pages Indexed</div>
                </div>
            </div>
            
            <h2>Sample Data</h2>
            <table>
                <thead>
                    <tr>
                        <th>Keyword</th>
                        <th>Volume</th>
                        <th>Position</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>example keyword 1</td>
                        <td>1,500</td>
                        <td>3</td>
                    </tr>
                    <tr>
                        <td>example keyword 2</td>
                        <td>800</td>
                        <td>8</td>
                    </tr>
                    <tr>
                        <td>example keyword 3</td>
                        <td>2,200</td>
                        <td>12</td>
                    </tr>
                </tbody>
            </table>
        </div>
        {% endif %}
        
        <hr>
        <p style="text-align: center;">This is a simple test dashboard to verify Flask is working correctly.</p>
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    domain = None
    location = 'DK'
    language = 'da'
    
    if request.method == 'POST':
        domain = request.form.get('domain')
        location = request.form.get('location')
        language = request.form.get('language')
    
    return render_template_string(HTML_TEMPLATE, domain=domain, location=location, language=language)

if __name__ == '__main__':
    app.run(debug=True, port=5050)
