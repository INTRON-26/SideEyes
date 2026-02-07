from datetime import datetime
import json
from typing import Dict, Any
from concurrent.futures import ThreadPoolExecutor

from web_scraper_base import logger
from quote_scraper import QuoteScraper
from book_scraper import BookScraper
from scrapethissite_scraper import ScrapesiteScraper


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

        # Initialize scrapers
        quote_scraper = QuoteScraper()
        book_scraper = BookScraper()
        hockey_scraper = ScrapesiteScraper()

        # Run scrapers in parallel using threads (I/O-bound)
        logger.info("\nLaunching scrapers in parallel...")
        with ThreadPoolExecutor(max_workers=3) as ex:
            future_to_key = {
                ex.submit(quote_scraper.scrape_quotes, num_pages): 'quotes',
                ex.submit(book_scraper.scrape_books, num_pages): 'books',
                ex.submit(hockey_scraper.scrape_hockey_stats, num_pages): 'hockey_teams'
            }

            for fut, key in future_to_key.items():
                try:
                    result = fut.result()
                except Exception as e:
                    logger.error(f"Error running scraper for {key}: {e}")
                    self.results['data'][key] = []
                else:
                    self.results['data'][key] = result

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
