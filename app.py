import streamlit as st
from supabase import create_client, Client
import os
import pandas as pd

# ------------------------------
# Supabase Connection
# ------------------------------
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    st.error("❌ Missing Supabase credentials. Please set SUPABASE_URL and SUPABASE_KEY in .env")
else:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ------------------------------
# Streamlit Config
# ------------------------------
st.set_page_config(page_title="Supabase SQL Editor", page_icon="🛠", layout="wide")

st.title("🛠 Supabase SQL Editor")
st.write("Run SQL queries directly on your Supabase database")

# ------------------------------
# SQL Input Box
# ------------------------------
sql_query = st.text_area("Enter SQL query:", height=200, placeholder="SELECT * FROM patients;")

if st.button("Run Query"):
    if not sql_query.strip():
        st.warning("⚠️ Please enter a SQL query")
    else:
        try:
            # Supabase has RPC calls, not raw SQL.
            # For direct SQL, you need Supabase Postgres connection string + psycopg2/sqlalchemy.
            # Let's use psycopg2 here for flexibility.
            import psycopg2

            conn = psycopg2.connect(
                host=os.getenv("SUPABASE_DB_HOST"),
                dbname=os.getenv("SUPABASE_DB_NAME"),
                user=os.getenv("SUPABASE_DB_USER"),
                password=os.getenv("SUPABASE_DB_PASSWORD"),
                port=5432
            )
            cur = conn.cursor()
            cur.execute(sql_query)

            # If SELECT, fetch results
            if sql_query.strip().lower().startswith("select"):
                rows = cur.fetchall()
                colnames = [desc[0] for desc in cur.description]
                df = pd.DataFrame(rows, columns=colnames)
                st.dataframe(df, use_container_width=True)
            else:
                conn.commit()
                st.success("✅ Query executed successfully")

            cur.close()
            conn.close()

        except Exception as e:
            st.error(f"❌ Error executing query: {e}")
