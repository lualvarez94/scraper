import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_craigslist(city: str, max_price: int, limit: int = 30):
    base_url = f"https://{city}.craigslist.org/search/cta?max_price={max_price}&hasPic=1"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }

    time.sleep(1)  # respectful delay

    response = requests.get(base_url, headers=headers)

    print("Status code:", response.status_code)
    print("First 500 characters of HTML:")
    print(response.text[:500])  # Check if Craigslist is showing a CAPTCHA or block

    soup = BeautifulSoup(response.text, 'html.parser')

    listings = []
    rows = soup.find_all("li", class_="result-row")
    
    print(f"Found {len(rows)} results")  # Should be >0

    for row in rows[:limit]:
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


