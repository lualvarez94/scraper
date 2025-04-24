# app.py
import streamlit as st
import importlib
import scraper
import pandas as pd

importlib.reload(scraper)
from scraper import scrape_edmunds

st.set_page_config(page_title="🚗 Used Car Finder - Edmunds", layout="centered")

st.title("🚗 Used Car Finder (Edmunds Edition)")
st.write("Find used car listings by ZIP code and price from Edmunds.com.")

with st.form("search_form"):
    zip_code = st.text_input("ZIP Code", value="94103")
    max_price = st.number_input("Max Price ($)", min_value=1000, max_value=100000, value=10000, step=500)
    limit = st.slider("Number of Results", min_value=5, max_value=50, step=5, value=10)
    submitted = st.form_submit_button("Search")

if submitted:
    with st.spinner(f"Searching Edmunds for cars under ${max_price} in {zip_code}..."):
        try:
            results = scrape_edmunds(zip_code, max_price, limit)
            if not results.empty:
                st.success(f"✅ Found {len(results)} results")
                for _, row in results.iterrows():
                    st.markdown(f"**{row['Title']}** — {row['Price']}")
                    st.markdown(f"[View Listing]({row['Link']})")
                    st.markdown("---")
            else:
                st.warning("No results found. Try a different ZIP or price.")
        except Exception as e:
            st.error(f"❌ Error: {e}")



