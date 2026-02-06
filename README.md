# SideEyes - Web Scraper for Public Test Sites

A Python-based web scraper designed to extract data from publicly available test websites that are specifically designed for web scraping practice.

## Features

- **Multiple Scrapers**: Includes scrapers for different test websites
- **Rate Limiting**: Respects site load by implementing delays between requests
- **Error Handling**: Robust error handling and logging throughout
- **Data Export**: Saves scraped data to JSON format
- **Modular Design**: Easy to extend with new scrapers

## Supported Test Sites

1. **quotes.toscrape.com** - Quote scraping

   - Extracts quotes, authors, and tags
   - Paginated content support
2. **books.toscrape.com** - Book scraping

   - Extracts book titles, prices, availability, and ratings
   - Pagination support
3. **scrapethissite.com** - Hockey statistics

   - Extracts hockey team data and statistics
   - Multiple pages of data

## Installation

### Prerequisites

- Python 3.7+
- pip (Python package manager)

### Setup

1. Clone or download the repository:

```bash
cd c:\Workspace\SideEyes
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Run the scraper with default settings (1 page from each site):

```bash
python web_scraper.py
```

### Advanced Usage

To modify the number of pages to scrape, edit the `main()` function in `web_scraper.py`:

```python
# Scrape 3 pages instead of 1
results = manager.run_all_scrapers(num_pages=3)
```

### Using Individual Scrapers

```python
from web_scraper import QuoteScraper, BookScraper

# Scrape quotes
quote_scraper = QuoteScraper()
quotes = quote_scraper.scrape_quotes(pages=2)

# Scrape books
book_scraper = BookScraper()
books = book_scraper.scrape_books(pages=3)
```

## Output

The scraper generates a `scraped_data.json` file with the following structure:

```json
{
  "timestamp": "2026-02-06T10:30:45.123456",
  "data": {
    "quotes": [
      {
        "text": "Quote text here",
        "author": "Author Name",
        "tags": ["tag1", "tag2"],
        "source": "http://quotes.toscrape.com"
      }
    ],
    "books": [
      {
        "title": "Book Title",
        "price": "10.59",
        "availability": "In stock",
        "rating": "Four",
        "source": "http://books.toscrape.com"
      }
    ],
    "hockey_teams": [
      {
        "name": "Team Name",
        "year": "2022",
        "wins": "50",
        "losses": "32",
        "source": "https://scrapethissite.com"
      }
    ]
  }
}
```

## Architecture

### Class Structure

- **WebScraper**: Base class with common scraping functionality

  - `fetch_page()`: Fetch URL with error handling
  - `parse_html()`: Parse HTML content
  - `respect_rate_limit()`: Add delays between requests
- **QuoteScraper**: Extends WebScraper for quotes.toscrape.com

  - `scrape_quotes()`: Extract quote data
- **BookScraper**: Extends WebScraper for books.toscrape.com

  - `scrape_books()`: Extract book data
- **ScrapesiteScraper**: Extends WebScraper for scrapethissite.com

  - `scrape_hockey_stats()`: Extract hockey statistics
- **MultiSiteScraperManager**: Orchestrates all scrapers

  - `run_all_scrapers()`: Execute all scraping tasks
  - `save_results()`: Export data to JSON
  - `print_summary()`: Display summary statistics

## Configuration

### Rate Limiting

Adjust the delay between requests by modifying the scraper initialization:

```python
quote_scraper = QuoteScraper()  # Default: 1 second delay
# or
scraper = WebScraper('http://example.com', delay=2.0)  # 2 second delay
```

### Request Timeout

Modify the timeout in the `fetch_page()` method:

```python
response = self.fetch_page(url, timeout=15)  # 15 seconds
```

## Best Practices

1. **Respect Rate Limits**: The scraper includes 1-2 second delays by default. Increase if needed to avoid overloading target sites.
2. **Check robots.txt**: Always check the target site's `robots.txt` file before scraping.
3. **User Agent**: The scraper uses a standard User-Agent header. Some sites may require modifications.
4. **Error Handling**: Check the logs for any errors or warnings during scraping.
5. **Legal Considerations**: Only scrape sites that permit scraping in their terms of service. These test sites are specifically designed for practice.

## Logging

The scraper outputs detailed logs showing:

- URL being scraped
- Number of items extracted
- Any errors or warnings
- Session start/end

Example log output:

```
2026-02-06 10:30:45,123 - INFO - ==================================================
2026-02-06 10:30:45,456 - INFO - Starting multi-site web scraping session
2026-02-06 10:30:45,789 - INFO - Scraping Quotes...
2026-02-06 10:30:46,012 - INFO - Scraping http://quotes.toscrape.com
2026-02-06 10:30:47,234 - INFO - Successfully scraped 10 quotes
```

## Extending the Scraper

To add a new scraper for a different website:

1. Create a new class that extends `WebScraper`:

```python
class NewSiteScraper(WebScraper):
    def __init__(self):
        super().__init__('https://example.com', delay=1.0)
  
    def scrape_data(self) -> List[Dict[str, Any]]:
        # Implementation here
        pass
```

2. Add it to the `MultiSiteScraperManager.run_all_scrapers()` method
3. Update the manager's `print_summary()` method to include results

## Troubleshooting

### Connection Errors

- Check internet connection
- Verify target site is accessible
- Check if rate limiting is too aggressive

### Missing Data

- Verify website structure hasn't changed
- Check CSS selectors in the parsing code
- Review error logs for parsing issues

### Timeout Errors

- Increase timeout value in `fetch_page()`
- Check network connection speed
- Reduce number of pages to scrape

## Legal Notice

These test sites are publicly available and designed specifically for web scraping practice:

- quotes.toscrape.com
- books.toscrape.com
- scrapethissite.com

Respect each site's terms of service and robots.txt. Do not use this scraper on websites that do not permit scraping.

## License

This project is created for educational purposes.
