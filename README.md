🔋 Jol Energy - Business Control Tower

📌 Project Overview
This repository contains a full-stack data analytics dashboard and supply chain management tool built for the **Jol Energy SDE Assessment**. 

Rather than relying on off-the-shelf software like Tableau or Power BI, this is a **Custom Application** engineered from scratch to demonstrate backend architecture, data pipeline generation, and frontend visualization skills.

# ⚙️ Tech Stack
* **Frontend/UI:** Python (Streamlit), Plotly
* **Backend Database:** PostgreSQL
* **Data Engineering:** Python (Pandas, Faker, psycopg2)

---

## 🚀 How to Run This Project Locally

1. Prerequisites
You must have Python installed and a local instance of PostgreSQL running on port `5432`. Ensure your Postgres user is `postgres` and password is `0712` (or update the credentials in `setup_database.py` and `app.py` to match your local setup).

2. Install Dependencies
Open your terminal and install the required Python libraries:
```bash
pip install streamlit pandas psycopg2 plotly faker

3. Generate the Datasets
Run the data generation script to create localized supply chain data (Suppliers, Buyers, and Collection Hubs in South India):

Bash
python generate_data.py

4. Setup the Database
Execute the database script. This will automatically create the required tables in PostgreSQL and perform a bulk insert of the generated CSV data for optimized performance:

Bash
python setup_database.py

5. Launch the Dashboard
Start the Streamlit server to view the live interactive UI:

Bash
streamlit run app.py

or you can use ->

python -m streamlit run app.py