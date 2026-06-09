import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px
import plotly.graph_objects as go

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

st.sidebar.header("🔋 Battery Filters")
selected_battery = st.sidebar.multiselect(
    "Battery Type",
    options=df_suppliers['battery_type'].unique(),
    default=df_suppliers['battery_type'].unique()
)

st.sidebar.header("📊 Pipeline Status Filters")
selected_sup_status = st.sidebar.multiselect(
    "Supplier Status",
    options=df_suppliers['status'].unique(),
    default=df_suppliers['status'].unique()
)

selected_buy_status = st.sidebar.multiselect(
    "Buyer Status",
    options=df_buyers['status'].unique(),
    default=df_buyers['status'].unique()
)

# Apply filters across multiple conditions using the & (AND) operator
filtered_suppliers = df_suppliers[
    (df_suppliers['city'].isin(selected_city)) & 
    (df_suppliers['battery_type'].isin(selected_battery)) &
    (df_suppliers['status'].isin(selected_sup_status))
]

filtered_buyers = df_buyers[
    (df_buyers['city'].isin(selected_city)) &
    (df_buyers['status'].isin(selected_buy_status))
]

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

# 6. Live Database Feeds (Tabbed View)
st.write("---")
st.header("📋 Live Database Directories")
st.markdown("Raw data feeds reflecting the currently applied sidebar filters.")

# Create interactive tabs for a cleaner UI
tab_supplier, tab_buyer = st.tabs(["🏭 Supplier Pipeline", "🤝 Buyer Pipeline"])

with tab_supplier:
    st.subheader("Supplier Directory")
    # Using use_container_width makes the table stretch nicely across the screen
    st.dataframe(
        filtered_suppliers[['company_name', 'city', 'battery_type', 'est_monthly_kg', 'status']], 
        use_container_width=True,
        hide_index=True # Hides the messy pandas index numbers for a cleaner look
    )

with tab_buyer:
    st.subheader("Buyer Directory")
    st.dataframe(
        filtered_buyers[['company_name', 'city', 'product_req', 'est_consumption_kg', 'status']], 
        use_container_width=True,
        hide_index=True
    )

# 7. Bottom Row: Supply Chain Flow (Sankey Diagram)
st.write("---")
st.header("🔄 4. Circular Economy Material Flow")
st.markdown("Visualizing the movement of battery mass (kg) from Sourcing Regions to Buyer Hubs.")

# --- SANKEY DIAGRAM LOGIC ---
# We map: Supplier Cities -> Jol Energy Central Processing -> Buyer Cities

# 1. Get unique cities from the filtered data
sup_cities = filtered_suppliers['city'].unique().tolist()
buy_cities = filtered_buyers['city'].unique().tolist()

# 2. Define all Nodes (The blocks in the diagram)
nodes = sup_cities + ["Jol Energy Central Hub"] + buy_cities
hub_index = len(sup_cities) # The index position of the Central Hub

# 3. Define Links (The connecting lines)
source = []
target = []
value = []

# Flow A: From Suppliers into the Central Hub
for i, city in enumerate(sup_cities):
    # Calculate total kg from this city
    vol = filtered_suppliers[filtered_suppliers['city'] == city]['est_monthly_kg'].sum()
    source.append(i)               # Origin: Supplier City
    target.append(hub_index)       # Destination: Central Hub
    value.append(vol)              # Thickness: Total volume

# Flow B: From the Central Hub out to Buyers
for i, city in enumerate(buy_cities):
    # Calculate total kg demanded by this city
    vol = filtered_buyers[filtered_buyers['city'] == city]['est_consumption_kg'].sum()
    source.append(hub_index)       # Origin: Central Hub
    target.append(hub_index + 1 + i) # Destination: Buyer City
    value.append(vol)              # Thickness: Total volume

# 4. Build and render the figure
fig_sankey = go.Figure(data=[go.Sankey(
    node = dict(
      pad = 20,
      thickness = 30,
      line = dict(color = "black", width = 0.5),
      label = nodes,
      color = "#1E90FF" # A clean tech-blue for the nodes
    ),
    link = dict(
      source = source,
      target = target,
      value = value,
      color = "rgba(169, 169, 169, 0.4)" # Semi-transparent grey for the flow
  ))])

fig_sankey.update_layout(
    height=500,
    font_size=12,
    margin=dict(t=20, l=20, r=20, b=20)
)

st.plotly_chart(fig_sankey, use_container_width=True)

# 8. Export Intelligence Report
st.write("---")
st.header("📥 5. Export Intelligence Report")
st.markdown("Download the currently filtered datasets for external stakeholder review.")

# Use columns to make the buttons look neat side-by-side
col_exp1, col_exp2 = st.columns(2)

with col_exp1:
    st.subheader("Supplier Data")
    st.caption(f"Ready to export {len(filtered_suppliers)} records.")
    # Convert dataframe to CSV format
    csv_sup = filtered_suppliers.to_csv(index=False).encode('utf-8')
    
    st.download_button(
        label="Download Supplier CSV",
        data=csv_sup,
        file_name="jol_energy_supplier_report.csv",
        mime="text/csv",
    )

with col_exp2:
    st.subheader("Buyer Data")
    st.caption(f"Ready to export {len(filtered_buyers)} records.")
    # Convert dataframe to CSV format
    csv_buy = filtered_buyers.to_csv(index=False).encode('utf-8')
    
    st.download_button(
        label="Download Buyer CSV",
        data=csv_buy,
        file_name="jol_energy_buyer_report.csv",
        mime="text/csv",
    )