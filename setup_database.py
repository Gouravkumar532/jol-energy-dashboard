import psycopg2
import psycopg2.extras # Importing extras for bulk insertion
import pandas as pd

try:
    connection = psycopg2.connect("postgresql://neondb_owner:npg_eimHZL0Baq2t@ep-wandering-surf-ao8m3u22.c-2.ap-southeast-1.aws.neon.tech/neondb?sslmode=require")
    cursor = connection.cursor()
    print("Database connection successful! Starting bulk insert...")

    # --- 1. SETUP SUPPLIER PIPELINE ---
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS supplier_pipeline (
        id SERIAL PRIMARY KEY,
        company_name VARCHAR(255),
        city VARCHAR(100),
        battery_type VARCHAR(100),
        est_monthly_kg INT,
        status VARCHAR(50)
    );
    TRUNCATE TABLE supplier_pipeline RESTART IDENTITY;
    """)
    
    df_suppliers = pd.read_csv('supplier_pipeline_data.csv')
    # Convert dataframe to list of tuples for bulk insert
    supplier_tuples = [tuple(x) for x in df_suppliers.to_numpy()]
    psycopg2.extras.execute_values(
        cursor,
        "INSERT INTO supplier_pipeline (company_name, city, battery_type, est_monthly_kg, status) VALUES %s",
        supplier_tuples
    )
    print(f"✅ Bulk inserted {len(df_suppliers)} rows into supplier_pipeline!")

    # --- 2. SETUP BUYER PIPELINE ---
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS buyer_pipeline (
        id SERIAL PRIMARY KEY,
        company_name VARCHAR(255),
        city VARCHAR(100),
        product_req VARCHAR(100),
        est_consumption_kg INT,
        status VARCHAR(50)
    );
    TRUNCATE TABLE buyer_pipeline RESTART IDENTITY;
    """)
    
    df_buyers = pd.read_csv('buyer_pipeline_data.csv')
    buyer_tuples = [tuple(x) for x in df_buyers.to_numpy()]
    psycopg2.extras.execute_values(
        cursor,
        "INSERT INTO buyer_pipeline (company_name, city, product_req, est_consumption_kg, status) VALUES %s",
        buyer_tuples
    )
    print(f"✅ Bulk inserted {len(df_buyers)} rows into buyer_pipeline!")

    # --- 3. SETUP COLLECTION NETWORK ---
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS collection_points (
        id SERIAL PRIMARY KEY,
        business_name VARCHAR(255),
        city VARCHAR(100),
        latitude DECIMAL(9,6),
        longitude DECIMAL(9,6),
        est_monthly_qty INT
    );
    TRUNCATE TABLE collection_points RESTART IDENTITY;
    """)
    
    df_collection = pd.read_csv('collection_network_data.csv')
    collection_tuples = [tuple(x) for x in df_collection.to_numpy()]
    psycopg2.extras.execute_values(
        cursor,
        "INSERT INTO collection_points (business_name, city, latitude, longitude, est_monthly_qty) VALUES %s",
        collection_tuples
    )
    print(f"✅ Bulk inserted {len(df_collection)} rows into collection_points!")

    connection.commit()
    cursor.close()
    connection.close()
    print("🎉 Database setup and load testing completely finished!")

except Exception as e:
    print(f"Error: {e}")