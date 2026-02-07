from typing import List, Dict, Any
from web_scraper_base import WebScraper, logger


class BookScraper(WebScraper):
    """Scraper for books.toscrape.com"""

    def __init__(self):
        """Initialize Book scraper."""
        super().__init__('http://books.toscrape.com', delay=1.0)

    def scrape_books(self, pages: int = 1) -> List[Dict[str, Any]]:
        """
        Scrape books from the website.

        Args:
            pages: Number of pages to scrape

        Returns:
            List of book dictionaries
        """
        books = []

        for page in range(1, pages + 1):
            if page == 1:
                url = self.base_url
            else:
                url = f"{self.base_url}/catalogue/page-{page}.html"

            logger.info(f"Scraping {url}")
            response = self.fetch_page(url)

            if not response:
                continue

            soup = self.parse_html(response.content)

            # Find all book articles
            book_articles = soup.find_all('article', class_='product_pod')

            for book in book_articles:
                try:
                    title = book.find('h3').find('a')['title']
                    price = book.find('p', class_='price_color').get_text()
                    availability = book.find('p', class_='instock availability').get_text().strip()
                    rating = book.find('p', class_='star-rating')['class'][1]  # e.g., "Three"

                    books.append({
                        'title': title,
                        'price': price,
                        'availability': availability,
                        'rating': rating,
                        'source': self.base_url
                    })
                except (AttributeError, KeyError, TypeError) as e:
                    logger.warning(f"Error parsing book: {e}")

            self.respect_rate_limit()

        logger.info(f"Successfully scraped {len(books)} books")
        return books
