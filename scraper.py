from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import logging
from models import Listing

def fetch_listings(url: str, limit: int = 10) -> list:
    options = Options()
    options.add_argument("--headless")
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    except Exception as e:
        logging.error(f"Driver Error: {e}")
        return []

    for attempt in range(3):
        try:
            driver.get(url)
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "article.product_pod"))
            )
            break
        except Exception as e:
            if attempt == 2:
                logging.error(f"Page Load failed after 3 attempts: {e}")
                driver.quit()
                return []
            time.sleep(1)

    html = driver.page_source
    driver.quit()

    try:
        soup = BeautifulSoup(html, "html.parser")
        cards = soup.select("article.product_pod")[:limit]
    except Exception as e:
        logging.error(f"Parsing Error: {e}")
        return []

    listings = []
    for card in cards:
        try:
            title_tag = card.select_one("h3 a")
            title = title_tag.get("title", "No title") if title_tag else "No title"

            price_tag = card.select_one(".price_color")
            # Secure float information
            try:
                price_text = price_tag.get_text().replace("£", "").strip() if price_tag else "0"
                price = float(price_text)
            except (ValueError, AttributeError):
                price = 0

            img_tag = card.select_one("img")
            images = [img_tag["src"]] if img_tag and img_tag.has_attr("src") else []

            listings.append(Listing(title, price, description="BooksToScrape", images=images))
        except Exception as e:
            logging.error(f"Skipping card due to parsing error: {e}")
            continue

    return listings

