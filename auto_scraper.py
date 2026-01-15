from scraper import scrape_amazon_product
from database import init_db, get_or_create_product, insert_price

# List of products to track
PRODUCT_URLS = [
    "https://a.co/d/jlm9KUa",
    "https://www.amazon.com/dp/B0CNVCQZG1"
]

if __name__ == "__main__":
    init_db()

    for url in PRODUCT_URLS:
        try:
            product = scrape_amazon_product(url)
            product_id = get_or_create_product(product["title"], product["url"])
            insert_price(product_id, product["price"])
            print(f"[+] Saved {product['title']} - ${product['price']:.2f}")
        except Exception as e:
            print(f"[!] Failed to scrape {url}: {e}")
