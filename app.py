#app.py
import streamlit as st
import importlib
import scraper  # Make sure scraper.py is in the same directory
import pandas as pd

# Force reload of scraper in case of changes
importlib.reload(scraper)
from scraper import scrape_craigslist

# Optional debug print to confirm reload
# print("✅ scraper.py reloaded successfully")

# Page setup
st.set_page_config(page_title="Used Car Finder", layout="centered")

# Title and instructions
st.title("🚗 Used Car Finder (Craigslist MVP)")
st.markdown("Find car listings from Craigslist by city and price.")

# Search form
with st.form("car_search"):
    city = st.text_input("Craigslist City Code (e.g., sfbay, losangeles, newyork)", value="sfbay")
    max_price = st.number_input("Max Price ($)", min_value=1000, max_value=100000, step=500, value=10000)
    limit = st.slider("Max Results to Display", min_value=10, max_value=100, step=10, value=30)
    submit = st.form_submit_button("Search Cars")

# Handle search
if submit:
    st.info(f"Searching Craigslist in **{city}** for cars under **${max_price}**...")
    
    # Fetch results
    try:
        results_df = scrape_craigslist(city, max_price, limit)
    except Exception as e:
        st.error(f"❌ Error during scraping: {e}")
        results_df = pd.DataFrame()

    # Display results
    if not results_df.empty:
        st.success(f"✅ Found {len(results_df)} results!")
        for _, row in results_df.iterrows():
            st.markdown(f"**{row['Title']}** — {row['Price']} ({row['Location']})")
            st.markdown(f"[View Listing]({row['Link']})")
            st.markdown("---")
    else:
        st.warning("No results found. Try a different city or price range.")

