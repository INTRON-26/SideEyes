#!/usr/bin/env python3
"""
Top-level runner for the scraping package. Imports split classes from modules
and provides the `main()` entrypoint.
"""

from manager import MultiSiteScraperManager


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
