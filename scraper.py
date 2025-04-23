# scraper.py
import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_craigslist(city: str, max_price: int, limit: int = 30):
    base_url = f"https://{city}.craigslist.org/search/cta?max_price={max_price}&hasPic=1"
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    listings = []
    for row in soup.find_all("li", class_="result-row")[:limit]:
        title_elem = row.find("a", class_="result-title")
        price_elem = row.find("span", class_="result-price")
        hood_elem = row.find("span", class_="result-hood")
        link = title_elem["href"] if title_elem else ""
        
        title = title_elem.text.strip() if title_elem else "N/A"
        price = price_elem.text.strip() if price_elem else "N/A"
        location = hood_elem.text.strip(" ()") if hood_elem else "N/A"
        
        listings.append({
            "Title": title,
            "Price": price,
            "Location": location,
            "Link": link
        })
    
    return pd.DataFrame(listings)

