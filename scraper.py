import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_cargurus(zip_code="95035", max_price=10000, limit=10):
    url = (
        f"https://www.cargurus.com/Cars/inventorylisting/viewDetailsFilterViewInventoryListing.action"
        f"?sourceContext=untrackedExternal_false_0&distance=50&inventorySearchWidgetType=AUTO"
        f"&zip={zip_code}&isDeliveryEnabled=true"
    )
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    # Optional: Adding cookies (you might need to extract cookies from your browser)
    cookies = {
        "csrftoken": "your_cookie_here",
        # Add more cookies if necessary (inspect using browser developer tools)
    }

    try:
        response = requests.get(url, headers=headers, cookies=cookies, timeout=20)
        response.raise_for_status()
    except requests.RequestException as e:
        raise Exception(f"Request failed: {e}")

    soup = BeautifulSoup(response.text, "html.parser")

    car_cards = soup.find_all("div", class_="vehicle-card")[:limit]
    if not car_cards:
        raise Exception("No listings found on CarGurus. Their layout may have changed.")

    listings = []
    for car in car_cards:
        title_tag = car.select_one("h4")
        price_tag = car.select_one("span[class*='price']")
        link_tag = car.select_one("a[href*='/Cars/inventorylisting/viewDetails']")

        title = title_tag.get_text(strip=True) if title_tag else "N/A"
        price = price_tag.get_text(strip=True) if price_tag else "N/A"
        link = f"https://www.cargurus.com{link_tag['href']}" if link_tag else "N/A"

        listings.append({
            "Title": title,
            "Price": price,
            "Link": link
        })

    return pd.DataFrame(listings)




