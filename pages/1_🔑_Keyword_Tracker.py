"""
Keyword Tracker Page
Track keywords with search volume, intent, and comprehensive metrics
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json
import http.client
from urllib.parse import quote
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

# Page configuration
st.set_page_config(
    page_title="Keyword Tracker",
    page_icon="🔑",
    layout="wide"
)

# API Keys
RAPIDAPI_KEY = "5c359bb774msh32eed0a33c585c4p1466d6jsn5620b810b2f7"

# MongoDB Configuration
MONGODB_URI = "mongodb://localhost:27017/"  # Default local MongoDB
DB_NAME = "seo_dashboard"
COLLECTION_NAME = "keywords"

# Initialize MongoDB connection
@st.cache_resource
def init_mongodb():
    """Initialize MongoDB connection"""
    try:
        client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
        # Test connection
        client.admin.command('ping')
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]
        return collection, True, "Connected to MongoDB"
    except ConnectionFailure:
        return None, False, "MongoDB not available - using session storage"
    except Exception as e:
        return None, False, f"MongoDB error: {str(e)}"

# Initialize MongoDB
mongo_collection, mongo_available, mongo_status = init_mongodb()

# Initialize session state for keyword tracking
if 'tracked_keywords' not in st.session_state:
    if mongo_available:
        # Load keywords from MongoDB
        try:
            keywords_from_db = list(mongo_collection.find({}, {'_id': 0}))
            st.session_state.tracked_keywords = keywords_from_db
        except:
            st.session_state.tracked_keywords = []
    else:
        st.session_state.tracked_keywords = []

# Helper function to save keyword to MongoDB
def save_keyword_to_db(keyword_entry):
    """Save keyword to MongoDB"""
    if mongo_available:
        try:
            # Add unique identifier
            keyword_entry['_id'] = f"{keyword_entry['keyword']}_{keyword_entry['country']}_{keyword_entry['added_date']}"
            mongo_collection.insert_one(keyword_entry)
            return True
        except Exception as e:
            st.error(f"Failed to save to MongoDB: {str(e)}")
            return False
    return False

# Helper function to delete keyword from MongoDB
def delete_keyword_from_db(keyword, country, added_date):
    """Delete keyword from MongoDB"""
    if mongo_available:
        try:
            _id = f"{keyword}_{country}_{added_date}"
            mongo_collection.delete_one({'_id': _id})
            return True
        except Exception as e:
            st.error(f"Failed to delete from MongoDB: {str(e)}")
            return False
    return False

# Helper function to clear all keywords from MongoDB
def clear_all_keywords_from_db():
    """Clear all keywords from MongoDB"""
    if mongo_available:
        try:
            mongo_collection.delete_many({})
            return True
        except Exception as e:
            st.error(f"Failed to clear MongoDB: {str(e)}")
            return False
    return False

# Header
st.title("🔑 Keyword Tracker")
st.markdown("Track and analyze keywords with search volume, intent, and comprehensive metrics")

# Helper function to fetch keyword data
def fetch_keyword_data(keyword, country):
    """Fetch keyword data from Semrush API"""
    try:
        conn = http.client.HTTPSConnection("semrush-keyword-magic-tool.p.rapidapi.com")
        headers = {
            'x-rapidapi-key': RAPIDAPI_KEY,
            'x-rapidapi-host': "semrush-keyword-magic-tool.p.rapidapi.com"
        }
        
        conn.request("GET", f"/global-volume?keyword={quote(keyword)}&country={country}", headers=headers)
        res = conn.getresponse()
        data = res.read().decode("utf-8")
        
        try:
            keyword_data = json.loads(data)
            return {
                'volume': keyword_data.get('volume', 'N/A'),
                'cpc': keyword_data.get('cpc', 'N/A'),
                'competition': keyword_data.get('competition', 'N/A')
            }
        except:
            return {'volume': 'N/A', 'cpc': 'N/A', 'competition': 'N/A'}
    except:
        return {'volume': 'N/A', 'cpc': 'N/A', 'competition': 'N/A'}

def fetch_url_traffic(url):
    """Fetch URL traffic data from Semrush8 API"""
    try:
        conn = http.client.HTTPSConnection("semrush8.p.rapidapi.com")
        headers = {
            'x-rapidapi-key': RAPIDAPI_KEY,
            'x-rapidapi-host': "semrush8.p.rapidapi.com"
        }
        
        conn.request("GET", f"/url_traffic?url={quote(url)}", headers=headers)
        res = conn.getresponse()
        data = res.read().decode("utf-8")
        
        try:
            traffic_data = json.loads(data)
            return {
                'success': True,
                'data': traffic_data
            }
        except:
            return {'success': False, 'data': None}
    except:
        return {'success': False, 'data': None}

def fetch_ahrefs_metrics(keyword, country):
    """Fetch keyword metrics from Ahrefs API"""
    try:
        conn = http.client.HTTPSConnection("ahrefs-keyword-research.p.rapidapi.com")
        headers = {
            'x-rapidapi-key': RAPIDAPI_KEY,
            'x-rapidapi-host': "ahrefs-keyword-research.p.rapidapi.com"
        }
        
        conn.request("GET", f"/keyword-metrics?keyword={quote(keyword)}&country={country}", headers=headers)
        res = conn.getresponse()
        data = res.read().decode("utf-8")
        
        try:
            ahrefs_data = json.loads(data)
            return {
                'success': True,
                'data': ahrefs_data
            }
        except:
            return {'success': False, 'data': None}
    except:
        return {'success': False, 'data': None}

# Sidebar - Add Keywords
st.sidebar.header("➕ Add Keywords to Track")

# Tab for single vs bulk import
import_tab1, import_tab2 = st.sidebar.tabs(["Single", "Bulk Import"])

with import_tab1:
    with st.form("add_keyword_form"):
        new_keyword = st.text_input("Keyword")
        country = st.selectbox("Country", ["us", "uk", "dk", "de", "fr", "se", "no"])
        intent = st.selectbox("Search Intent", ["Informational", "Navigational", "Transactional", "Commercial"])
        notes = st.text_area("Notes (optional)")
        
        add_button = st.form_submit_button("➕ Add Keyword")
        
        if add_button and new_keyword:
            # Fetch keyword data
            keyword_data = fetch_keyword_data(new_keyword, country)
            
            # Add to tracked keywords
            keyword_entry = {
                'keyword': new_keyword,
                'country': country,
                'intent': intent,
                'volume': keyword_data['volume'],
                'cpc': keyword_data['cpc'],
                'competition': keyword_data['competition'],
                'notes': notes,
                'added_date': datetime.now().strftime("%Y-%m-%d %H:%M"),
                'status': 'Active'
            }
            
            st.session_state.tracked_keywords.append(keyword_entry)
            
            # Save to MongoDB if available
            if mongo_available:
                save_keyword_to_db(keyword_entry.copy())
            
            st.success(f"✅ Added: {new_keyword}" + (" (saved to MongoDB)" if mongo_available else ""))

with import_tab2:
    st.markdown("### 📥 Import Keywords")
    
    # File upload
    uploaded_file = st.file_uploader(
        "Upload CSV or TXT file",
        type=['csv', 'txt'],
        help="CSV: keyword,country,intent,notes | TXT: one keyword per line"
    )
    
    if uploaded_file is not None:
        # Default settings for bulk import
        default_country = st.selectbox("Default Country", ["us", "uk", "dk", "de", "fr", "se", "no"], key="bulk_country")
        default_intent = st.selectbox("Default Intent", ["Informational", "Navigational", "Transactional", "Commercial"], key="bulk_intent")
        fetch_data = st.checkbox("Fetch API data (slower)", value=False, help="Fetch volume/CPC data for each keyword")
        
        if st.button("📥 Import Keywords"):
            try:
                # Read file
                if uploaded_file.name.endswith('.csv'):
                    # CSV format
                    import io
                    content = uploaded_file.read().decode('utf-8')
                    lines = content.strip().split('\n')
                    
                    imported_count = 0
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    for idx, line in enumerate(lines):
                        if not line.strip():
                            continue
                        
                        parts = [p.strip() for p in line.split(',')]
                        keyword = parts[0] if len(parts) > 0 else ""
                        country = parts[1] if len(parts) > 1 else default_country
                        intent = parts[2] if len(parts) > 2 else default_intent
                        notes = parts[3] if len(parts) > 3 else ""
                        
                        if keyword:
                            # Fetch data if requested
                            if fetch_data:
                                status_text.text(f"Fetching data for: {keyword}")
                                keyword_data = fetch_keyword_data(keyword, country)
                            else:
                                keyword_data = {'volume': 'N/A', 'cpc': 'N/A', 'competition': 'N/A'}
                            
                            keyword_entry = {
                                'keyword': keyword,
                                'country': country,
                                'intent': intent,
                                'volume': keyword_data['volume'],
                                'cpc': keyword_data['cpc'],
                                'competition': keyword_data['competition'],
                                'notes': notes,
                                'added_date': datetime.now().strftime("%Y-%m-%d %H:%M"),
                                'status': 'Active'
                            }
                            
                            st.session_state.tracked_keywords.append(keyword_entry)
                            imported_count += 1
                        
                        progress_bar.progress((idx + 1) / len(lines))
                    
                    progress_bar.empty()
                    status_text.empty()
                    st.success(f"✅ Imported {imported_count} keywords from CSV")
                
                else:
                    # TXT format - one keyword per line
                    content = uploaded_file.read().decode('utf-8')
                    lines = content.strip().split('\n')
                    
                    imported_count = 0
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    for idx, line in enumerate(lines):
                        keyword = line.strip()
                        if keyword:
                            # Fetch data if requested
                            if fetch_data:
                                status_text.text(f"Fetching data for: {keyword}")
                                keyword_data = fetch_keyword_data(keyword, default_country)
                            else:
                                keyword_data = {'volume': 'N/A', 'cpc': 'N/A', 'competition': 'N/A'}
                            
                            keyword_entry = {
                                'keyword': keyword,
                                'country': default_country,
                                'intent': default_intent,
                                'volume': keyword_data['volume'],
                                'cpc': keyword_data['cpc'],
                                'competition': keyword_data['competition'],
                                'notes': '',
                                'added_date': datetime.now().strftime("%Y-%m-%d %H:%M"),
                                'status': 'Active'
                            }
                            
                            st.session_state.tracked_keywords.append(keyword_entry)
                            imported_count += 1
                        
                        progress_bar.progress((idx + 1) / len(lines))
                    
                    progress_bar.empty()
                    status_text.empty()
                    st.success(f"✅ Imported {imported_count} keywords from TXT")
                    
            except Exception as e:
                st.error(f"Error importing file: {str(e)}")
    
    # Show format examples
    with st.expander("📄 File Format Examples"):
        st.markdown("""
        **CSV Format:**
        ```
        keyword,country,intent,notes
        seo tools,us,Commercial,High priority
        keyword research,dk,Informational,
        backlink checker,uk,Transactional,Premium tool
        ```
        
        **TXT Format:**
        ```
        seo tools
        keyword research
        backlink checker
        content optimization
        ```
        
        **Notes:**
        - CSV: Comma-separated values
        - TXT: One keyword per line
        - Country codes: us, uk, dk, de, fr, se, no
        - Intent: Informational, Navigational, Transactional, Commercial
        """)

# Sidebar - Manage Keywords
st.sidebar.markdown("---")
st.sidebar.header("📊 Tracked Keywords")
st.sidebar.metric("Total Keywords", len(st.session_state.tracked_keywords))

if st.sidebar.button("🗑️ Clear All Keywords"):
    # Clear from MongoDB if available
    if mongo_available:
        clear_all_keywords_from_db()
    
    st.session_state.tracked_keywords = []
    st.sidebar.success("Cleared all keywords" + (" (from MongoDB)" if mongo_available else ""))

# Display MongoDB status
if mongo_available:
    st.sidebar.success(f"💾 {mongo_status}")
else:
    st.sidebar.warning(f"⚠️ {mongo_status}")

# Main Content
if st.session_state.tracked_keywords:
    # Convert to DataFrame
    df = pd.DataFrame(st.session_state.tracked_keywords)
    
    # Summary Metrics
    st.header("📊 Overview")
    col1, col2, col3, col4 = st.columns(4)
    
    col1.metric("Total Keywords", len(df))
    col2.metric("Countries", df['country'].nunique())
    col3.metric("Active Keywords", len(df[df['status'] == 'Active']))
    
    # Calculate average volume (handle N/A values)
    try:
        avg_vol = df[df['volume'] != 'N/A']['volume'].apply(lambda x: float(x) if str(x).replace('.','').replace(',','').isdigit() else 0).mean()
        col4.metric("Avg Search Volume", f"{avg_vol:,.0f}")
    except:
        col4.metric("Avg Search Volume", "N/A")
    
    # Tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(["📋 All Keywords", "📈 Analytics", "🎯 By Intent", "🌍 By Country"])
    
    with tab1:
        st.subheader("All Tracked Keywords")
        
        # Display table with actions
        for idx, row in df.iterrows():
            with st.expander(f"🔑 {row['keyword']} ({row['country'].upper()})"):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"**Search Intent:** {row['intent']}")
                    st.markdown(f"**Search Volume:** {row['volume']}")
                    st.markdown(f"**CPC:** ${row['cpc']}" if row['cpc'] != 'N/A' else f"**CPC:** {row['cpc']}")
                    st.markdown(f"**Competition:** {row['competition']}")
                    st.markdown(f"**Added:** {row['added_date']}")
                    if row['notes']:
                        st.markdown(f"**Notes:** {row['notes']}")
                    
                    st.markdown("---")
                    
                    # Ahrefs Keyword Metrics
                    if st.button(f"🔍 Get Ahrefs Metrics", key=f"ahrefs_{idx}"):
                        with st.spinner("Fetching Ahrefs data..."):
                            ahrefs_result = fetch_ahrefs_metrics(row['keyword'], row['country'])
                            if ahrefs_result['success'] and ahrefs_result['data']:
                                st.success("✅ Ahrefs data retrieved")
                                ahrefs_data = ahrefs_result['data']
                                
                                # Display Ahrefs metrics
                                st.markdown("#### 🔍 Ahrefs Keyword Metrics")
                                acol1, acol2, acol3, acol4 = st.columns(4)
                                
                                if 'keyword_difficulty' in ahrefs_data:
                                    acol1.metric("Keyword Difficulty", ahrefs_data['keyword_difficulty'])
                                if 'search_volume' in ahrefs_data:
                                    acol2.metric("Search Volume", f"{ahrefs_data['search_volume']:,}")
                                if 'cpc' in ahrefs_data:
                                    acol3.metric("CPC", f"${ahrefs_data['cpc']:.2f}")
                                if 'clicks' in ahrefs_data:
                                    acol4.metric("Clicks", f"{ahrefs_data['clicks']:,}")
                                
                                # Additional metrics
                                if 'return_rate' in ahrefs_data or 'parent_topic' in ahrefs_data:
                                    st.markdown("#### 📊 Additional Metrics")
                                    bcol1, bcol2 = st.columns(2)
                                    if 'return_rate' in ahrefs_data:
                                        bcol1.metric("Return Rate", f"{ahrefs_data['return_rate']:.1f}%")
                                    if 'parent_topic' in ahrefs_data:
                                        bcol2.info(f"**Parent Topic:** {ahrefs_data['parent_topic']}")
                                
                                # Show full data
                                with st.expander("View Full Ahrefs Data"):
                                    st.json(ahrefs_data)
                            else:
                                st.warning("⚠️ Could not fetch Ahrefs data for this keyword")
                    
                    # Add URL traffic analysis
                    url_input = st.text_input(f"Landing Page URL (optional)", key=f"url_{idx}", placeholder="https://example.com/page")
                    if url_input and st.button(f"📊 Analyze Traffic", key=f"traffic_{idx}"):
                        with st.spinner("Fetching traffic data..."):
                            traffic_result = fetch_url_traffic(url_input)
                            if traffic_result['success'] and traffic_result['data']:
                                st.success("✅ Traffic data retrieved")
                                traffic_data = traffic_result['data']
                                
                                # Display traffic metrics
                                st.markdown("#### 📈 Traffic Metrics")
                                tcol1, tcol2, tcol3 = st.columns(3)
                                
                                if 'visits' in traffic_data:
                                    tcol1.metric("Monthly Visits", f"{traffic_data['visits']:,}")
                                if 'pages_per_visit' in traffic_data:
                                    tcol2.metric("Pages/Visit", f"{traffic_data['pages_per_visit']:.2f}")
                                if 'bounce_rate' in traffic_data:
                                    tcol3.metric("Bounce Rate", f"{traffic_data['bounce_rate']:.1f}%")
                                
                                # Show full data
                                with st.expander("View Full Traffic Data"):
                                    st.json(traffic_data)
                            else:
                                st.warning("⚠️ Could not fetch traffic data for this URL")
                
                with col2:
                    if st.button(f"🗑️ Remove", key=f"remove_{idx}"):
                        # Delete from MongoDB if available
                        if mongo_available:
                            delete_keyword_from_db(row['keyword'], row['country'], row['added_date'])
                        
                        st.session_state.tracked_keywords.pop(idx)
                        st.rerun()
                    
                    if st.button(f"🔄 Refresh Data", key=f"refresh_{idx}"):
                        st.info("Refreshing keyword data...")
        
        # Download button
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download All Keywords CSV",
            data=csv,
            file_name=f"tracked_keywords_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    
    with tab2:
        st.subheader("📈 Keyword Analytics")
        
        # Search Volume Distribution
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Search Volume by Keyword")
            df_plot = df[df['volume'] != 'N/A'].copy()
            if not df_plot.empty:
                df_plot['volume_numeric'] = pd.to_numeric(df_plot['volume'], errors='coerce')
                df_plot = df_plot.dropna(subset=['volume_numeric'])
                
                if not df_plot.empty:
                    fig = px.bar(
                        df_plot.sort_values('volume_numeric', ascending=False).head(15),
                        x='keyword',
                        y='volume_numeric',
                        color='intent',
                        title='Top 15 Keywords by Search Volume'
                    )
                    fig.update_xaxis(tickangle=-45)
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No volume data available")
        
        with col2:
            st.markdown("### CPC Distribution")
            df_plot = df[df['cpc'] != 'N/A'].copy()
            if not df_plot.empty:
                df_plot['cpc_numeric'] = pd.to_numeric(df_plot['cpc'], errors='coerce')
                df_plot = df_plot.dropna(subset=['cpc_numeric'])
                
                if not df_plot.empty:
                    fig = px.scatter(
                        df_plot,
                        x='volume',
                        y='cpc_numeric',
                        size='cpc_numeric',
                        color='intent',
                        hover_data=['keyword'],
                        title='Search Volume vs CPC'
                    )
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No CPC data available")
        
        # Competition Analysis
        st.markdown("### Competition Level Distribution")
        if 'competition' in df.columns:
            competition_counts = df['competition'].value_counts()
            fig = px.pie(
                values=competition_counts.values,
                names=competition_counts.index,
                title='Keywords by Competition Level'
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("🎯 Keywords by Search Intent")
        
        intent_groups = df.groupby('intent')
        
        for intent, group in intent_groups:
            with st.expander(f"{intent} ({len(group)} keywords)"):
                st.dataframe(
                    group[['keyword', 'country', 'volume', 'cpc', 'competition']],
                    use_container_width=True,
                    hide_index=True
                )
                
                # Intent-specific metrics
                col1, col2, col3 = st.columns(3)
                col1.metric("Keywords", len(group))
                
                try:
                    avg_vol = group[group['volume'] != 'N/A']['volume'].apply(lambda x: float(x) if str(x).replace('.','').replace(',','').isdigit() else 0).mean()
                    col2.metric("Avg Volume", f"{avg_vol:,.0f}")
                except:
                    col2.metric("Avg Volume", "N/A")
                
                try:
                    avg_cpc = group[group['cpc'] != 'N/A']['cpc'].apply(lambda x: float(x) if str(x).replace('.','').isdigit() else 0).mean()
                    col3.metric("Avg CPC", f"${avg_cpc:.2f}")
                except:
                    col3.metric("Avg CPC", "N/A")
    
    with tab4:
        st.subheader("🌍 Keywords by Country")
        
        country_groups = df.groupby('country')
        
        for country_code, group in country_groups:
            with st.expander(f"{country_code.upper()} ({len(group)} keywords)"):
                st.dataframe(
                    group[['keyword', 'intent', 'volume', 'cpc', 'competition']],
                    use_container_width=True,
                    hide_index=True
                )
                
                # Country-specific metrics
                col1, col2, col3 = st.columns(3)
                col1.metric("Keywords", len(group))
                
                try:
                    total_vol = group[group['volume'] != 'N/A']['volume'].apply(lambda x: float(x) if str(x).replace('.','').replace(',','').isdigit() else 0).sum()
                    col2.metric("Total Volume", f"{total_vol:,.0f}")
                except:
                    col2.metric("Total Volume", "N/A")
                
                col3.metric("Intents", group['intent'].nunique())

else:
    st.info("👈 Add keywords using the sidebar to start tracking")
    
    st.markdown("""
    ### 🎯 How to Use Keyword Tracker
    
    1. **Add Keywords**: Use the sidebar form to add keywords
    2. **Set Country**: Choose target country for search data
    3. **Define Intent**: Categorize by search intent
    4. **Add Notes**: Optional notes for each keyword
    5. **Track Metrics**: View search volume, CPC, competition
    6. **Analyze**: Use tabs to view different perspectives
    7. **Export**: Download CSV for reporting
    
    ### 📊 Available Metrics
    
    - **Search Volume**: Monthly search volume
    - **CPC**: Cost per click
    - **Competition**: Keyword difficulty
    - **Intent**: Search intent classification
    - **Country**: Geographic targeting
    - **Status**: Tracking status
    
    ### 🎯 Search Intent Types
    
    - **Informational**: Users seeking information
    - **Navigational**: Users looking for specific site
    - **Transactional**: Users ready to buy
    - **Commercial**: Users researching products
    """)

# Footer
st.markdown("---")
if mongo_available:
    st.markdown("💾 **Storage:** Keywords are automatically saved to MongoDB and persist across sessions.")
else:
    st.markdown("💡 **Tip:** MongoDB not available. Keywords are stored in session only. Export to CSV to save permanently.")
    st.markdown("📝 **To enable MongoDB:** Install MongoDB locally and ensure it's running on mongodb://localhost:27017/")
