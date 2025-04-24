# app.py
import streamlit as st
import importlib
import scraper
import pandas as pd

importlib.reload(scraper)
from scraper import scrape_cars_com

st.set_page_config(page_title="Used Car Finder", layout="centered")

st.title("🚘 Used Car Finder V2 (Cars.com Edition)")
st.write("Search used car listings near your zip code with price filters.")

with st.form("search"):
    zip_code = st.text_input("Zip Code", value="94103")
    max_price = st.number_input("Max Price ($)", min_value=1000, max_value=100000, value=10000, step=500)
    limit = st.slider("Number of Results", min_value=5, max_value=50, step=5, value=10)
    submitted = st.form_submit_button("Search")

if submitted:
    with st.spinner(f"Searching Cars.com for cars under ${max_price} in {zip_code}..."):
        try:
            df = scrape_cars_com(zip_code, max_price, limit)
            if not df.empty:
                st.success(f"✅ Found {len(df)} listings!")
                for _, row in df.iterrows():
                    st.markdown(f"**{row['Title']}** — {row['Price']}")
                    st.markdown(f"[View Listing]({row['Link']})")
                    st.markdown("---")
            else:
                st.warning("No listings found. Try a different zip or price.")
        except Exception as e:
            st.error(f"❌ Error: {e}")



