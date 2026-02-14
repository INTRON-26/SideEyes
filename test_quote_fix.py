#!/usr/bin/env python
"""Quick test to verify quote author names are fixed"""

from quote_scraper import QuoteScraper

scraper = QuoteScraper()
quotes = scraper.scrape_quotes(pages=1)

print("✓ Quote Author Names Test")
print("=" * 60)
print(f"Scraped {len(quotes)} quotes\n")

print("First 3 quotes:")
for i, quote in enumerate(quotes[:3], 1):
    print(f"\n{i}. Author: {quote['author']}")
    print(f"   Quote: {quote['text'][:60]}...")
