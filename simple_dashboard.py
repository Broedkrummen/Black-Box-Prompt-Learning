"""
Simple Streamlit Dashboard - Minimal Version
For testing if Streamlit works properly
"""

import streamlit as st

# Set page config
st.set_page_config(
    page_title="Simple SEO Dashboard",
    page_icon="🔍",
    layout="wide"
)

# Header
st.title("🔍 Simple SEO Dashboard")
st.markdown("### A minimal version to test if Streamlit is working")

# Input form
st.markdown("## Enter Domain to Analyze")
with st.form("domain_form"):
    domain = st.text_input("Domain (e.g., example.com)")
    location = st.selectbox("Location", ["DK", "US", "GB", "DE", "SE", "NO"])
    language = st.selectbox("Language", ["da", "en", "de", "sv", "no"])
    
    analyze_button = st.form_submit_button("Analyze")

# Display when form is submitted
if analyze_button and domain:
    st.success(f"Form submitted successfully! Would analyze {domain} in {location} with language {language}")
    
    # Display metrics
    st.markdown("## Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Domain Authority", "42")
    
    with col2:
        st.metric("Domain Rating", "38")
    
    with col3:
        st.metric("Monthly Visits", "12,500")
    
    with col4:
        st.metric("Pages Indexed", "158")
    
    # Display a chart
    st.markdown("## Sample Chart")
    chart_data = {
        'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
        'Visits': [1200, 1800, 2400, 2100, 2800]
    }
    
    st.line_chart(
        {
            'Visits': chart_data['Visits']
        }
    )
    
    # Display a table
    st.markdown("## Sample Data")
    st.table({
        'Keyword': ['example keyword 1', 'example keyword 2', 'example keyword 3'],
        'Volume': [1500, 800, 2200],
        'Position': [3, 8, 12]
    })

# Footer
st.markdown("---")
st.markdown("This is a simple test dashboard to verify Streamlit is working correctly.")
