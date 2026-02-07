from typing import List, Dict, Any
from web_scraper_base import WebScraper, logger


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
