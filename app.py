import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px

# 1. Page Configuration
st.set_page_config(page_title="Jol Energy Analytics", layout="wide")
st.title("🔋 Jol Energy - Business Control Tower")
st.markdown("### *Data Analytics & Supply Chain Pipeline Dashboard*")
st.write("---")

# 2. Secure Database Connection & Data Fetching
@st.cache_data(ttl=600) # Caches the data for 10 minutes so the app stays lightning fast
def load_data():
    try:
        connection = psycopg2.connect(
            host="localhost",
            database="jol_energy_db",
            user="postgres",
            password="0712",
            port="5432"
        )
        
        # Pull data directly from your PostgreSQL tables
        suppliers = pd.read_sql_query("SELECT * FROM supplier_pipeline;", connection)
        buyers = pd.read_sql_query("SELECT * FROM buyer_pipeline;", connection)
        collection = pd.read_sql_query("SELECT * FROM collection_points;", connection)
        
        connection.close()
        return suppliers, buyers, collection
    
    except Exception as e:
        st.error(f"Database Connection Error: {e}")
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

df_suppliers, df_buyers, df_collection = load_data()

# Check if data loaded properly
if df_suppliers.empty:
    st.warning("No data found. Please ensure your database is running and setup_database.py was executed.")
    st.stop()

# 3. Sidebar Filters
st.sidebar.header("🎯 Regional Filters")
selected_city = st.sidebar.multiselect(
    "Select Target Cities", 
    options=df_suppliers['city'].unique(), 
    default=df_suppliers['city'].unique()
)

# Apply filters
filtered_suppliers = df_suppliers[df_suppliers['city'].isin(selected_city)]
filtered_buyers = df_buyers[df_buyers['city'].isin(selected_city)]

# 4. Top Row: Market Intelligence Module
st.header("📈 1. Market Intelligence (Critical Mineral Pricing)")
col1, col2, col3, col4 = st.columns(4)
col1.metric(label="Lithium Carbonate (per Metric Ton)", value="$14,200", delta="-2.4% (Weekly)")
col2.metric(label="Cobalt Sulphate (per Ton)", value="$28,500", delta="+1.1% (Weekly)")
col3.metric(label="Nickel Sulphate (per Ton)", value="$16,800", delta="+0.5% (Weekly)")
col4.metric(label="Battery Scrap / Black Mass (per Kg)", value="₹180", delta="+₹5 (Weekly)")
st.write("---")

# 5. Middle Row: Funnel Visualizations for Pipelines
st.header("⏳ 2. Commercial Funnel Pipelines")
left_col, right_col = st.columns(2)

with left_col:
    st.subheader("Supplier Pipeline Status")
    # Count the statuses for the funnel
    sup_counts = filtered_suppliers['status'].value_counts().reindex(
        ['Leads Generated', 'Contacted', 'Qualified', 'Interested', 'LOI Received']
    ).fillna(0).reset_index()
    sup_counts.columns = ['Status', 'Count']
    
    fig_sup = px.funnel(sup_counts, x='Count', y='Status', title="Supplier Lead Conversion")
    st.plotly_chart(fig_sup, use_container_width=True)

with right_col:
    st.subheader("Buyer Pipeline Status")
    buy_counts = filtered_buyers['status'].value_counts().reindex(
        ['Leads Generated', 'Contacted', 'Sample Requested', 'Discussion Stage', 'LOI Received']
    ).fillna(0).reset_index()
    buy_counts.columns = ['Status', 'Count']
    
    fig_buy = px.funnel(buy_counts, x='Count', y='Status', title="Buyer Procurement Conversion")
    st.plotly_chart(fig_buy, use_container_width=True)

st.write("---")

# 6. Bottom Row: Geographic Collection Network Map
st.header("🗺️ 3. Geographic Collection Network")
st.markdown("Live plot of designated battery collection hubs across South India.")

# Streamlit's built-in map automatically looks for 'latitude' and 'longitude' columns!
st.map(df_collection, zoom=5, use_container_width=True)

# Data Table view for quick inspection
st.write("---")
st.subheader("📋 Live Database Feed: Supplier Directory")
st.dataframe(filtered_suppliers[['company_name', 'city', 'battery_type', 'est_monthly_kg', 'status']])