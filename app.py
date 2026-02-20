"""
Web application for displaying problem analysis results.
"""
from flask import Flask, render_template, jsonify, request
import json
import os
from datetime import datetime
from scraper import scrape_all_sources
from analyzer import ProblemAnalyzer


app = Flask(__name__)

# Load configuration
with open('config.json', 'r') as f:
    config = json.load(f)

# Global storage for analysis results
latest_analysis = None
latest_scrape_time = None


@app.route('/')
def index():
    """Main dashboard page."""
    return render_template('index.html')


@app.route('/api/scrape', methods=['POST'])
def scrape():
    """Trigger a new scraping operation."""
    global latest_analysis, latest_scrape_time
    
    try:
        # Check if demo data exists (for when external APIs are not accessible)
        if os.path.exists('demo_data.json'):
            print("Loading demo data...")
            with open('demo_data.json', 'r') as f:
                demo_data = json.load(f)
                latest_analysis = demo_data['analysis']
                latest_scrape_time = datetime.now().isoformat()
                return jsonify({
                    'success': True,
                    'message': f'Loaded demo data with {latest_analysis["total_problems"]} problems',
                    'timestamp': latest_scrape_time
                })
        
        # Scrape all sources
        problems = scrape_all_sources(config)
        
        # Analyze problems
        analyzer = ProblemAnalyzer(config)
        analysis = analyzer.analyze_problems(problems)
        
        # Store results
        latest_analysis = analysis
        latest_scrape_time = datetime.now().isoformat()
        
        return jsonify({
            'success': True,
            'message': f'Scraped {len(problems)} problems',
            'timestamp': latest_scrape_time
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/analysis')
def get_analysis():
    """Get the latest analysis results."""
    if latest_analysis is None:
        return jsonify({
            'error': 'No analysis available. Please run scrape first.'
        }), 404
    
    return jsonify({
        'analysis': latest_analysis,
        'timestamp': latest_scrape_time
    })


@app.route('/api/top-problems')
def get_top_problems():
    """Get the top problems."""
    if latest_analysis is None:
        return jsonify({
            'error': 'No analysis available. Please run scrape first.'
        }), 404
    
    limit = request.args.get('limit', 50, type=int)
    top_problems = latest_analysis.get('top_problems', [])[:limit]
    
    return jsonify({
        'top_problems': top_problems,
        'total': len(top_problems),
        'timestamp': latest_scrape_time
    })


@app.route('/api/categories')
def get_categories():
    """Get problem categories breakdown."""
    if latest_analysis is None:
        return jsonify({
            'error': 'No analysis available. Please run scrape first.'
        }), 404
    
    return jsonify({
        'categories': latest_analysis.get('categories', {}),
        'timestamp': latest_scrape_time
    })


@app.route('/api/keywords')
def get_keywords():
    """Get top keywords."""
    if latest_analysis is None:
        return jsonify({
            'error': 'No analysis available. Please run scrape first.'
        }), 404
    
    limit = request.args.get('limit', 50, type=int)
    keywords = latest_analysis.get('top_keywords', [])[:limit]
    
    return jsonify({
        'keywords': keywords,
        'timestamp': latest_scrape_time
    })


@app.route('/api/stats')
def get_stats():
    """Get overall statistics."""
    if latest_analysis is None:
        return jsonify({
            'error': 'No analysis available. Please run scrape first.'
        }), 404
    
    return jsonify({
        'total_problems': latest_analysis.get('total_problems', 0),
        'sources': latest_analysis.get('sources', {}),
        'categories_count': len(latest_analysis.get('categories', {})),
        'top_problems_count': len(latest_analysis.get('top_problems', [])),
        'timestamp': latest_scrape_time
    })


if __name__ == '__main__':
    port = int(os.getenv('FLASK_PORT', 5000))
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    debug = os.getenv('DEBUG', 'True').lower() == 'true'
    
    print(f"Starting Autonomous App Builder server on {host}:{port}")
    print(f"Access the dashboard at http://localhost:{port}")
    app.run(host=host, port=port, debug=debug)
