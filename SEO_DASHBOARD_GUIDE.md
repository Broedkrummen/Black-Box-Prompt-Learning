# SEO Dashboard Guide

This guide provides instructions for running and using the various SEO dashboards created for analyzing domains.

## Available Dashboards

We've created four different versions of the SEO dashboard using different technologies:

1. **Streamlit Dashboard** - Interactive web-based dashboard with a clean UI
2. **Flask Dashboard** - Web-based dashboard with a traditional HTML/CSS interface
3. **Dash Dashboard** - Interactive dashboard using Plotly Dash
4. **Tkinter Dashboard** - Desktop application

## Running the Dashboards

### Streamlit Dashboard

```bash
# Install dependencies
pip install -r requirements_streamlit.txt

# Run the dashboard
streamlit run seo_dashboard_streamlit.py
```

The dashboard will be available at: http://localhost:8501

### Flask Dashboard

```bash
# Install dependencies
pip install -r requirements_flask.txt

# Run the dashboard
python seo_dashboard_flask.py
```

The dashboard will be available at: http://localhost:5000

### Dash Dashboard

```bash
# Install dependencies
pip install -r requirements_dash.txt

# Run the dashboard
python seo_dashboard_dash.py
```

The dashboard will be available at: http://localhost:8050

### Tkinter Dashboard

```bash
# Install dependencies
pip install -r requirements_tkinter.txt

# Run the dashboard
python seo_dashboard_tkinter.py
```

This will open a desktop application window.

## Using the Dashboards

All dashboards provide similar functionality:

1. Enter a domain to analyze (e.g., simplybeyond.dk)
2. Select location and language options
3. Click "Analyze" to process the domain
4. View the results in various tabs/sections:
   - Domain Overview
   - Backlinks Analysis
   - Keyword Rankings
   - Traffic Analysis
   - Technical SEO
   - Recommendations

## Troubleshooting

If you encounter any issues:

1. **Port conflicts**: If a port is already in use, try changing the port number in the respective dashboard file.
2. **Missing dependencies**: Ensure all required packages are installed using the requirements files.
3. **Connection issues**: Check your internet connection as the dashboards need to fetch data from various APIs.
4. **API limits**: Some APIs have usage limits. If you encounter errors, you might need to wait before making more requests.

## Example Domain Analysis

For testing purposes, you can use the domain "simplybeyond.dk" which has been confirmed to work well with the dashboards.

## Additional Resources

- Check the `DASHBOARD_GUIDE.md` file for more detailed information about each dashboard's features
- Refer to `START_DASHBOARDS.md` for quick start instructions
- See `test_dashboard.py` for API testing functionality
