# scraper.py
import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_edmunds(zip_code="94103", max_price=10000, limit=10):
    url = (
        f"https://www.edmunds.com/used-cars-for-sale/"
        f"?price={max_price}&radius=50&zip={zip_code}"
    )
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
    except requests.RequestException as e:
        raise Exception(f"Request failed: {e}")

    soup = BeautifulSoup(response.text, "html.parser")
    cars = soup.select("div.inventory-listing")[:limit]

    listings = []
    for car in cars:
        title_tag = car.select_one("h2")
        price_tag = car.select_one("span[class*='price']")
        link_tag = car.select_one("a[href*='/used-cars-for-sale/vehicle/']")

        title = title_tag.text.strip() if title_tag else "N/A"
        price = price_tag.text.strip() if price_tag else "N/A"
        link = f"https://www.edmunds.com{link_tag['href']}" if link_tag else "N/A"

        listings.append({
            "Title": title,
            "Price": price,
            "Link": link
        })

    return pd.DataFrame(listings)


