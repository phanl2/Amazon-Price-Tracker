import requests
from bs4 import BeautifulSoup
from database import init_db, get_or_create_product, insert_price
from config import HEADERS, TIMEOUT

# Helper functions

def fetch_product_page(url: str) -> tuple[str, str]:
    """
    Fetch the product page HTML and return both HTML and final URL.
    """
    response = requests.get(
        url,
        headers=HEADERS,
        timeout=TIMEOUT,
        allow_redirects=True
    )
    response.raise_for_status()
    return response.text, response.url  # HTML and final URL

def parse_title(soup: BeautifulSoup) -> str:
    """
    Parse the product title. Fallback to first <h1> if productTitle not found.
    """
    title_tag = soup.find(id="productTitle")
    if not title_tag:
        title_tag = soup.find("h1")
        if not title_tag:
            return "Unknown Product Title"
    return title_tag.get_text(strip=True)

def parse_price(soup: BeautifulSoup) -> float:
    """
    Parse the product price using multiple common selectors.
    """
    price_selectors = [
        "span.a-offscreen",      # most reliable
        "span.a-price-whole"
    ]

    for selector in price_selectors:
        price_tag = soup.select_one(selector)
        if price_tag:
            price_text = price_tag.get_text().replace("$", "").replace(",", "").strip()
            try:
                return float(price_text)
            except ValueError:
                continue  # try next selector

    raise ValueError("Could not find product price")

def scrape_amazon_product(url: str) -> dict:
    """
    Fetch and parse Amazon product data.
    Returns a dictionary with title, price, and final URL.
    """
    html, final_url = fetch_product_page(url)
    soup = BeautifulSoup(html, "lxml")
    title = parse_title(soup)
    price = parse_price(soup)
    return {"title": title, "price": price, "url": final_url}

# Main Program

if __name__ == "__main__":
    init_db()

    url = input("Enter Amazon product URL: ").strip()

    try:
        product = scrape_amazon_product(url)

        # Save using the expanded/final URL
        product_id = get_or_create_product(product["title"], product["url"])
        insert_price(product_id, product["price"])

        print("\nProduct Found & Saved")
        print("----------------------")
        print(f"Title     : {product['title']}")
        print(f"Price     : ${product['price']:.2f}")

    except Exception as e:
        print(f"Error: {e}")
