# scraper.py
import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_cars_com(zip_code: str = "94103", max_price: int = 10000, limit: int = 20):
    url = f"https://www.cars.com/shopping/results/?list_price_max={max_price}&maximum_distance=50&zip={zip_code}&stock_type=used"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch Cars.com data: {response.status_code}")
    
    soup = BeautifulSoup(response.text, "html.parser")
    listings = []

    cars = soup.find_all("div", class_="vehicle-card")[:limit]
    for car in cars:
        title = car.find("h2")
        price = car.find("span", class_="primary-price")
        link_tag = car.find("a", class_="vehicle-card-link")

        listings.append({
            "Title": title.text.strip() if title else "N/A",
            "Price": price.text.strip() if price else "N/A",
            "Link": f"https://www.cars.com{link_tag['href']}" if link_tag else "N/A"
        })

    return pd.DataFrame(listings)
