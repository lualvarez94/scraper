# app.py
import streamlit as st
from scraper import scrape_cargurus

st.set_page_config(page_title="🚗 CarGurus Used Car Finder", layout="centered")

st.title("🚗 CarGurus Used Car Finder")
st.write("Find car listings from CarGurus by ZIP code and price.")

with st.form("search_form"):
    zip_code = st.text_input("ZIP Code", value="95035")
    max_price = st.number_input("Max Price ($)", min_value=1000, max_value=100000, value=10000, step=500)
    limit = st.slider("Number of Results", min_value=5, max_value=50, step=5, value=10)
    submitted = st.form_submit_button("Search")

if submitted:
    with st.spinner(f"Searching CarGurus for cars under ${max_price} in {zip_code}..."):
        try:
            results = scrape_cargurus(zip_code, max_price, limit)
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




