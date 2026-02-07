#!/usr/bin/env python3
"""
Base web scraper utilities and `WebScraper` class.
"""
import requests
import logging
import time
from bs4 import BeautifulSoup
from typing import Optional

# Configure logging for package
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

    def fetch_page(self, url: str, timeout: int = 10) -> Optional[requests.Response]:
        """
        Fetch a page with error handling.

        Args:
            url: URL to fetch
            timeout: Request timeout in seconds

        Returns:
            Response object or None on error
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
