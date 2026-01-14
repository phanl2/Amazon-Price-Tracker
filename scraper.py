import requests
from bs4 import BeautifulSoup
from config import HEADERS, TIMEOUT
from database import init_db, get_or_create_product, insert_price


def fetch_product_page(url: str) -> str:
    response = requests.get(
        url,
        headers=HEADERS,
        timeout=TIMEOUT,
        allow_redirects=True
    )
    response.raise_for_status()
    return response.text


def parse_title(soup: BeautifulSoup) -> str:
    title_tag = soup.find(id="productTitle")
    if not title_tag:
        raise ValueError("Could not find product title")
    return title_tag.get_text(strip=True)


def parse_price(soup: BeautifulSoup) -> float:
    price_selectors = [
        "span.a-offscreen",      # most reliable
        "span.a-price-whole"
    ]

    for selector in price_selectors:
        price_tag = soup.select_one(selector)
        if price_tag:
            price_text = (
                price_tag.get_text()
                .replace("$", "")
                .replace(",", "")
                .strip()
            )
            return float(price_text)

    raise ValueError("Could not find product price")


def scrape_amazon_product(url: str) -> dict:
    html = fetch_product_page(url)
    soup = BeautifulSoup(html, "lxml")

    title = parse_title(soup)
    price = parse_price(soup)

    return {
        "title": title,
        "price": price
    }


if __name__ == "__main__":
    init_db()

    url = input("Enter Amazon product URL: ").strip()

    try:
        product = scrape_amazon_product(url)

        product_id = get_or_create_product(
            product["title"],
            url
        )

        insert_price(product_id, product["price"])

        print("\nProduct Found & Saved")
        print("----------------------")
        print(f"Title : {product['title']}")
        print(f"Price : ${product['price']:.2f}")

    except Exception as e:
        print(f"Error: {e}")

