# app.py
import streamlit as st
from scraper import scrape_craigslist

st.set_page_config(page_title="Used Car Finder", layout="centered")

st.title("🚗 Used Car Finder (Craigslist MVP)")
st.write("Find car listings from Craigslist by city and price.")

with st.form("car_search"):
    city = st.text_input("Craigslist City Code (e.g., sfbay, losangeles, newyork)", value="sfbay")
    max_price = st.number_input("Max Price ($)", min_value=1000, max_value=100000, step=500, value=10000)
    submit = st.form_submit_button("Search Cars")

if submit:
    st.info(f"Searching Craigslist in **{city}** for cars under **${max_price}**...")
    results_df = scrape_craigslist(city, max_price)
    
    if not results_df.empty:
        st.success(f"Found {len(results_df)} results!")
        for _, row in results_df.iterrows():
            st.markdown(f"**{row['Title']}** — {row['Price']} ({row['Location']})")
            st.markdown(f"[View Listing]({row['Link']})\n---")
    else:
        st.warning("No results found. Try a different city or price range.")
