#!/usr/bin/env python3
"""
Web Scraper Script for Public Test Sites
Scrapes data from publicly available test websites designed for web scraping practice.
"""

import requests
import logging
import time
from typing import List, Dict, Any
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# User agent to identify the scraper
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'

class WebScraper:
    """Base web scraper class with common functionality."""
    
    def __init__(self, base_url: str, delay: float = 1.0):
        """
        Initialize the scraper.
        
        Args:
            base_url: Base URL to scrape
            delay: Delay between requests in seconds (respect rate limiting)
        """
        self.base_url = base_url
        self.delay = delay
        self.session = self._create_session()
        
    def _create_session(self) -> requests.Session:
        """Create a requests session with proper headers."""
        session = requests.Session()
        session.headers.update({'User-Agent': USER_AGENT})
        return session
    
    def fetch_page(self, url: str, timeout: int = 10) -> requests.Response:
        """
        Fetch a page with error handling.
        
        Args:
            url: URL to fetch
            timeout: Request timeout in seconds
            
        Returns:
            Response object
        """
        try:
            response = self.session.get(url, timeout=timeout)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            logger.error(f"Error fetching {url}: {e}")
            return None
    
    def parse_html(self, html_content: str) -> BeautifulSoup:
        """Parse HTML content with BeautifulSoup."""
        return BeautifulSoup(html_content, 'html.parser')
    
    def respect_rate_limit(self):
        """Add delay between requests to respect rate limiting."""
        time.sleep(self.delay)


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


class ScrapesiteScraper(WebScraper):
    """Scraper for scrapethissite.com"""
    
    def __init__(self):
        """Initialize Scrapesite scraper."""
        super().__init__('https://scrapethissite.com', delay=1.0)
        
    def scrape_hockey_stats(self, pages: int = 1) -> List[Dict[str, Any]]:
        """
        Scrape hockey statistics from the website.
        
        Args:
            pages: Number of pages to scrape
            
        Returns:
            List of hockey team dictionaries
        """
        teams = []
        
        for page in range(0, pages):
            url = f"{self.base_url}/pages/forms/?page={page}"
            logger.info(f"Scraping {url}")
            response = self.fetch_page(url)
            
            if not response:
                continue
                
            soup = self.parse_html(response.content)
            
            # Find all team rows
            team_rows = soup.find_all('tr', class_='team')
            
            for row in team_rows:
                try:
                    cells = row.find_all('td')
                    if len(cells) >= 4:
                        teams.append({
                            'name': cells[0].get_text().strip(),
                            'year': cells[1].get_text().strip(),
                            'wins': cells[2].get_text().strip(),
                            'losses': cells[3].get_text().strip(),
                            'source': self.base_url
                        })
                except (IndexError, AttributeError) as e:
                    logger.warning(f"Error parsing team data: {e}")
                    
            self.respect_rate_limit()
            
        logger.info(f"Successfully scraped {len(teams)} team records")
        return teams


class MultiSiteScraperManager:
    """Manages scraping from multiple test sites."""
    
    def __init__(self):
        """Initialize the manager."""
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'data': {}
        }
        
    def run_all_scrapers(self, num_pages: int = 1) -> Dict[str, Any]:
        """
        Run all configured scrapers.
        
        Args:
            num_pages: Number of pages to scrape from each site
            
        Returns:
            Dictionary containing all scraped data
        """
        logger.info("=" * 50)
        logger.info("Starting multi-site web scraping session")
        logger.info("=" * 50)
        
        # Scrape quotes
        logger.info("\nScraping Quotes...")
        quote_scraper = QuoteScraper()
        self.results['data']['quotes'] = quote_scraper.scrape_quotes(pages=num_pages)
        
        # Scrape books
        logger.info("\nScraping Books...")
        book_scraper = BookScraper()
        self.results['data']['books'] = book_scraper.scrape_books(pages=num_pages)
        
        # Scrape hockey stats
        logger.info("\nScraping Hockey Statistics...")
        hockey_scraper = ScrapesiteScraper()
        self.results['data']['hockey_teams'] = hockey_scraper.scrape_hockey_stats(pages=num_pages)
        
        logger.info("\n" + "=" * 50)
        logger.info("Scraping session completed")
        logger.info("=" * 50)
        
        return self.results
    
    def save_results(self, filename: str = 'scraped_data.json'):
        """
        Save results to a JSON file.
        
        Args:
            filename: Output filename
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, indent=2, ensure_ascii=False)
            logger.info(f"Results saved to {filename}")
        except IOError as e:
            logger.error(f"Error saving results: {e}")
    
    def print_summary(self):
        """Print a summary of scraped data."""
        print("\n" + "=" * 60)
        print("SCRAPING SUMMARY")
        print("=" * 60)
        
        if 'quotes' in self.results['data']:
            print(f"\nQuotes: {len(self.results['data']['quotes'])} items scraped")
            if self.results['data']['quotes']:
                print(f"  Example: \"{self.results['data']['quotes'][0]['text'][:50]}...\"")
        
        if 'books' in self.results['data']:
            print(f"\nBooks: {len(self.results['data']['books'])} items scraped")
            if self.results['data']['books']:
                print(f"  Example: {self.results['data']['books'][0]['title']}")
        
        if 'hockey_teams' in self.results['data']:
            print(f"\nHockey Teams: {len(self.results['data']['hockey_teams'])} records scraped")
            if self.results['data']['hockey_teams']:
                print(f"  Example: {self.results['data']['hockey_teams'][0]['name']}")
        
        print("\n" + "=" * 60 + "\n")


def main():
    """Main function to run the web scraper."""
    manager = MultiSiteScraperManager()
    
    # Run scrapers (1 page each as default)
    results = manager.run_all_scrapers(num_pages=1)
    
    # Save results
    manager.save_results('scraped_data.json')
    
    # Print summary
    manager.print_summary()


if __name__ == '__main__':
    main()
