import pandas as pd
import random
from faker import Faker

fake = Faker('en_IN')

# Assessment Target Cities
cities = ['Chennai', 'Coimbatore', 'Bengaluru', 'Kochi', 'Hyderabad', 'Visakhapatnam', 'Hosur']

# --- 1. GENERATE SUPPLIER PIPELINE DATA ---
def generate_suppliers(num_records=100):
    supplier_stages = ['Leads Generated', 'Contacted', 'Qualified', 'Interested', 'LOI Received']
    battery_types = ['Mobile Phone', 'Laptop', 'E-Bike', 'E-Scooter', 'EV Battery Packs']
    
    data = []
    for _ in range(num_records):
        data.append({
            'Company_Name': f"{fake.company()} E-Waste Solutions",
            'City': random.choice(cities),
            'Battery_Type': random.choice(battery_types),
            'Est_Monthly_Kg': random.randint(100, 1500),
            'Status': random.choices(supplier_stages, weights=[40, 30, 15, 10, 5], k=1)[0]
        })
    df = pd.DataFrame(data)
    df.to_csv('supplier_pipeline_data.csv', index=False)
    print("✅ Generated supplier_pipeline_data.csv (100 leads)")

# --- 2. GENERATE BUYER PIPELINE DATA ---
def generate_buyers(num_records=50):
    buyer_stages = ['Leads Generated', 'Contacted', 'Sample Requested', 'Discussion Stage', 'LOI Received']
    chemicals = ['Nickel Sulphate', 'Cobalt Sulphate', 'Lithium Carbonate', 'Manganese Sulphate']
    
    data = []
    for _ in range(num_records):
        data.append({
            'Company_Name': f"{fake.company()} Refineries",
            'City': random.choice(cities),
            'Product_Requirement': random.choice(chemicals),
            'Est_Consumption_Kg': random.randint(500, 5000),
            'Status': random.choices(buyer_stages, weights=[35, 30, 15, 15, 5], k=1)[0]
        })
    df = pd.DataFrame(data)
    df.to_csv('buyer_pipeline_data.csv', index=False)
    print("✅ Generated buyer_pipeline_data.csv (50 leads)")

# --- 3. GENERATE COLLECTION NETWORK DATA ---
def generate_collection_network(num_records=30):
    # Generating slight variations in coordinates around South India hubs
    base_coords = {
        'Chennai': (13.0827, 80.2707),
        'Bengaluru': (12.9716, 77.5946),
        'Hyderabad': (17.3850, 78.4867),
        'Kochi': (9.9312, 76.2673)
    }
    
    data = []
    for _ in range(num_records):
        city = random.choice(list(base_coords.keys()))
        base_lat, base_lon = base_coords[city]
        
        data.append({
            'Business_Name': f"{fake.first_name()} Mobile & EV Repairs",
            'City': city,
            'Latitude': base_lat + random.uniform(-0.05, 0.05),
            'Longitude': base_lon + random.uniform(-0.05, 0.05),
            'Est_Monthly_Qty': random.randint(20, 200)
        })
    df = pd.DataFrame(data)
    df.to_csv('collection_network_data.csv', index=False)
    print("✅ Generated collection_network_data.csv (30 collection hubs)")

# Execute all functions
if __name__ == "__main__":
    print("Starting massive data generation for Jol Energy Load Test...")
    generate_suppliers(num_records=10000)        # 10,000 Suppliers
    generate_buyers(num_records=5000)          # 5,000 Buyers
    generate_collection_network(num_records=1000) # 1,000 Collection Hubs
    print("🎉 16,000 total datasets generated successfully!")