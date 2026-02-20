# Quick Start Guide

## Installation & Running

1. **Clone and install dependencies:**
```bash
git clone https://github.com/Rakshakh/AutonomousAppBuilder.git
cd AutonomousAppBuilder
pip install -r requirements.txt
```

2. **Run the demo (generates mock data):**
```bash
python demo.py
```

3. **Start the web server:**
```bash
python app.py
```

4. **Open your browser:**
Navigate to http://localhost:5000

5. **Click "Start Scraping & Analysis"** to load data

## What You'll See

- **Total Problems**: Count of all scraped problems
- **Top Problems Identified**: Number of high-priority problems with multiple mentions
- **Categories**: Problem domains (API, Database, Frontend, etc.)
- **Data Sources**: Number of sources (Reddit, Stack Overflow, GitHub)
- **Top 50 Problems**: Ranked list of most common issues with:
  - Problem title
  - Category
  - Users affected
  - Priority score
- **Problem Categories**: Breakdown of problems by domain

## Configuration

Edit `config.json` to customize:
- Which sources to scrape
- Subreddits to monitor
- Stack Overflow tags
- Minimum problem mentions threshold

## Demo Mode

The app includes demo mode which loads pre-generated mock data when external APIs are unavailable. This is useful for:
- Testing the application
- Demonstrations
- Environments with network restrictions

Simply run `python demo.py` first to generate demo data, then the app will automatically use it when external APIs fail.

## API Endpoints

- `POST /api/scrape` - Trigger scraping
- `GET /api/analysis` - Get full analysis
- `GET /api/top-problems?limit=50` - Get top N problems
- `GET /api/categories` - Get category breakdown
- `GET /api/keywords` - Get top keywords
- `GET /api/stats` - Get overall statistics

## Testing

Run the test suite:
```bash
python test_app.py
```

This will:
1. Check server connectivity
2. Trigger scraping
3. Verify all API endpoints
4. Display sample results
