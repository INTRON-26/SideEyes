from typing import List, Dict, Any
from web_scraper_base import WebScraper, logger


class QuoteScraper(WebScraper):
    """Scraper for quotes.toscrape.com"""

    def __init__(self):
        """Initialize Quote scraper."""
        super().__init__('http://quotes.toscrape.com', delay=1.0)

    def scrape_quotes(self, pages: int = 1) -> List[Dict[str, Any]]:
        """
        Scrape quotes from the website.

        Args:
            pages: Number of pages to scrape

        Returns:
            List of quote dictionaries
        """
        quotes = []

        for page in range(1, pages + 1):
            if page == 1:
                url = self.base_url
            else:
                url = f"{self.base_url}/page/{page}/"

            logger.info(f"Scraping {url}")
            response = self.fetch_page(url)

            if not response:
                continue

            soup = self.parse_html(response.content)

            # Find all quote containers
            quote_divs = soup.find_all('div', class_='quote')

            for quote_div in quote_divs:
                try:
                    text = quote_div.find('span', class_='text').get_text()[1:-1]  # Remove quotes
                    author = quote_div.find('small', class_='author').get_text()[3:]  # Remove "by "
                    tags = [tag.get_text() for tag in quote_div.find_all('a', class_='tag')]

                    quotes.append({
                        'text': text,
                        'author': author,
                        'tags': tags,
                        'source': self.base_url
                    })
                except AttributeError as e:
                    logger.warning(f"Error parsing quote: {e}")

            self.respect_rate_limit()

        logger.info(f"Successfully scraped {len(quotes)} quotes")
        return quotes
