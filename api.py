"""API server to serve scraped data."""

import json
import os
from flask import Flask, jsonify, request
from datetime import datetime
from flasgger import Swagger
from manager import MultiSiteScraperManager
from quote_scraper import QuoteScraper
from book_scraper import BookScraper
from scrapethissite_scraper import ScrapesiteScraper

app = Flask(__name__)
swagger = Swagger(app, template={
    'swagger': '2.0',
    'info': {
        'title': 'SideEyes Scraper API',
        'version': '1.0',
        'description': 'API to access scraped data from multiple websites'
    }
})

DATA_FILE = 'scraped_data.json'


def load_scraped_data():
    """Load scraped data from JSON file."""
    if not os.path.exists(DATA_FILE):
        return {'error': 'No scraped data available'}, 404
    
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        return {'error': f'Error reading data: {str(e)}'}, 500


@app.route('/api/data', methods=['GET'])
def get_all_data():
    """
    Get all scraped data
    ---
    responses:
      200:
        description: All scraped data
        schema:
          type: object
          properties:
            timestamp:
              type: string
            data:
              type: object
      404:
        description: No scraped data available
    """
    data = load_scraped_data()
    if isinstance(data, tuple):  # Error case
        return jsonify(data[0]), data[1]
    return jsonify(data)


@app.route('/api/quotes', methods=['GET'])
def get_quotes():
    """
    Get scraped quotes
    ---
    responses:
      200:
        description: Quotes data
        schema:
          type: object
          properties:
            timestamp:
              type: string
            count:
              type: integer
            quotes:
              type: array
      404:
        description: No data available
    """
    data = load_scraped_data()
    if isinstance(data, tuple):  # Error case
        return jsonify(data[0]), data[1]
    
    quotes = data.get('data', {}).get('quotes', [])
    return jsonify({
        'timestamp': data.get('timestamp'),
        'count': len(quotes),
        'quotes': quotes
    })


@app.route('/api/books', methods=['GET'])
def get_books():
    """
    Get scraped books
    ---
    responses:
      200:
        description: Books data
        schema:
          type: object
          properties:
            timestamp:
              type: string
            count:
              type: integer
            books:
              type: array
      404:
        description: No data available
    """
    data = load_scraped_data()
    if isinstance(data, tuple):  # Error case
        return jsonify(data[0]), data[1]
    
    books = data.get('data', {}).get('books', [])
    return jsonify({
        'timestamp': data.get('timestamp'),
        'count': len(books),
        'books': books
    })


@app.route('/api/hockey', methods=['GET'])
def get_hockey_stats():
    """
    Get scraped hockey team statistics
    ---
    responses:
      200:
        description: Hockey stats
        schema:
          type: object
          properties:
            timestamp:
              type: string
            count:
              type: integer
            hockey_teams:
              type: array
      404:
        description: No data available
    """
    data = load_scraped_data()
    if isinstance(data, tuple):  # Error case
        return jsonify(data[0]), data[1]
    
    hockey_teams = data.get('data', {}).get('hockey_teams', [])
    return jsonify({
        'timestamp': data.get('timestamp'),
        'count': len(hockey_teams),
        'hockey_teams': hockey_teams
    })


@app.route('/api/data/<data_type>', methods=['GET'])
def get_data_by_type(data_type):
    """
    Get specific data type by name
    ---
    parameters:
      - name: data_type
        in: path
        type: string
        required: true
        description: Type of data to retrieve (quotes, books, hockey_teams)
        example: quotes
    responses:
      200:
        description: Data of requested type
      404:
        description: Data type not found
    """
    data = load_scraped_data()
    if isinstance(data, tuple):  # Error case
        return jsonify(data[0]), data[1]
    
    available_data = data.get('data', {})
    
    if data_type not in available_data:
        return jsonify({
            'error': f'Data type "{data_type}" not found',
            'available_types': list(available_data.keys())
        }), 404
    
    items = available_data.get(data_type, [])
    return jsonify({
        'timestamp': data.get('timestamp'),
        'type': data_type,
        'count': len(items) if isinstance(items, list) else 1,
        'data': items
    })


@app.route('/api/status', methods=['GET'])
def get_status():
    """
    Get API and data status
    ---
    responses:
      200:
        description: API and data status information
        schema:
          type: object
          properties:
            status:
              type: string
            message:
              type: string
            data_timestamp:
              type: string
            available_endpoints:
              type: object
            data_summary:
              type: object
      404:
        description: No data available
    """
    if not os.path.exists(DATA_FILE):
        return jsonify({
            'status': 'no_data',
            'message': 'No scraped data available',
            'file': DATA_FILE
        }), 404
    
    data = load_scraped_data()
    if isinstance(data, tuple):  # Error case
        return jsonify(data[0]), data[1]
    
    system_data = data.get('data', {})
    return jsonify({
        'status': 'ok',
        'message': 'API is running',
        'data_timestamp': data.get('timestamp'),
        'available_endpoints': {
            '/api/data': 'Get all scraped data',
            '/api/quotes': 'Get quotes',
            '/api/books': 'Get books',
            '/api/hockey': 'Get hockey stats',
            '/api/data/<type>': 'Get specific data type',
            '/api/status': 'Get API status'
        },
        'data_summary': {key: len(value) if isinstance(value, list) else 1 
                        for key, value in system_data.items()}
    })


@app.route('/', methods=['GET'])
def home():
    """Welcome page with API documentation."""
    return jsonify({
        'name': 'SideEyes Scraper API',
        'version': '1.0',
        'description': 'API to access scraped data from multiple websites',
        'endpoints': {
            'GET /api/status': 'Check API and data status',
            'GET /api/data': 'Get all scraped data',
            'GET /api/quotes': 'Get quotes data',
            'GET /api/books': 'Get books data',
            'GET /api/hockey': 'Get hockey stats',
            'GET /api/data/<type>': 'Get specific data type (e.g., /api/data/quotes)',
            'POST /api/scrape': 'Scrape all data',
            'POST /api/scrape/quotes': 'Scrape quotes only',
            'POST /api/scrape/books': 'Scrape books only',
            'POST /api/scrape/hockey': 'Scrape hockey stats only'
        }
    })


@app.route('/api/scrape', methods=['POST'])
def scrape_all():
    """
    Scrape data from all sources
    ---
    parameters:
      - name: pages
        in: query
        type: integer
        default: 1
        description: Number of pages to scrape from each site
    responses:
      200:
        description: Scraping completed successfully
        schema:
          type: object
          properties:
            status:
              type: string
            message:
              type: string
            data:
              type: object
      500:
        description: Error during scraping
    """
    try:
        pages = request.args.get('pages', 1, type=int)
        if pages < 1:
            return jsonify({'error': 'pages must be greater than 0'}), 400
        
        manager = MultiSiteScraperManager()
        results = manager.run_all_scrapers(num_pages=pages)
        manager.save_results(DATA_FILE)
        
        return jsonify({
            'status': 'success',
            'message': f'Successfully scraped {pages} page(s) from all sources',
            'timestamp': results.get('timestamp'),
            'data_summary': {key: len(value) if isinstance(value, list) else 1 
                           for key, value in results.get('data', {}).items()}
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Scraping failed: {str(e)}'
        }), 500


@app.route('/api/scrape/quotes', methods=['POST'])
def scrape_quotes():
    """
    Scrape quotes only
    ---
    parameters:
      - name: pages
        in: query
        type: integer
        default: 1
        description: Number of pages to scrape
    responses:
      200:
        description: Quotes scraped successfully
      500:
        description: Error during scraping
    """
    try:
        pages = request.args.get('pages', 1, type=int)
        if pages < 1:
            return jsonify({'error': 'pages must be greater than 0'}), 400
        
        scraper = QuoteScraper()
        quotes = scraper.scrape_quotes(pages=pages)
        
        # Load existing data and update
        data = load_scraped_data()
        if not isinstance(data, tuple):
            data['data']['quotes'] = quotes
            try:
                with open(DATA_FILE, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
            except IOError:
                pass
        
        return jsonify({
            'status': 'success',
            'message': f'Successfully scraped {len(quotes)} quotes from {pages} page(s)',
            'count': len(quotes),
            'quotes': quotes
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Scraping failed: {str(e)}'
        }), 500


@app.route('/api/scrape/books', methods=['POST'])
def scrape_books():
    """
    Scrape books only
    ---
    parameters:
      - name: pages
        in: query
        type: integer
        default: 1
        description: Number of pages to scrape
    responses:
      200:
        description: Books scraped successfully
      500:
        description: Error during scraping
    """
    try:
        pages = request.args.get('pages', 1, type=int)
        if pages < 1:
            return jsonify({'error': 'pages must be greater than 0'}), 400
        
        scraper = BookScraper()
        books = scraper.scrape_books(pages=pages)
        
        # Load existing data and update
        data = load_scraped_data()
        if not isinstance(data, tuple):
            data['data']['books'] = books
            try:
                with open(DATA_FILE, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
            except IOError:
                pass
        
        return jsonify({
            'status': 'success',
            'message': f'Successfully scraped {len(books)} books from {pages} page(s)',
            'count': len(books),
            'books': books
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Scraping failed: {str(e)}'
        }), 500


@app.route('/api/scrape/hockey', methods=['POST'])
def scrape_hockey():
    """
    Scrape hockey stats only
    ---
    parameters:
      - name: pages
        in: query
        type: integer
        default: 1
        description: Number of pages to scrape
    responses:
      200:
        description: Hockey stats scraped successfully
      500:
        description: Error during scraping
    """
    try:
        pages = request.args.get('pages', 1, type=int)
        if pages < 1:
            return jsonify({'error': 'pages must be greater than 0'}), 400
        
        scraper = ScrapesiteScraper()
        stats = scraper.scrape_hockey_stats(pages=pages)
        
        # Load existing data and update
        data = load_scraped_data()
        if not isinstance(data, tuple):
            data['data']['hockey_teams'] = stats
            try:
                with open(DATA_FILE, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
            except IOError:
                pass
        
        return jsonify({
            'status': 'success',
            'message': f'Successfully scraped {len(stats)} records from {pages} page(s)',
            'count': len(stats),
            'hockey_teams': stats
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Scraping failed: {str(e)}'
        }), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        'error': 'Endpoint not found',
        'message': 'Check /api/status or / for available endpoints'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({
        'error': 'Internal server error',
        'message': str(error)
    }), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
