# AutonomousAppBuilder 🚀

An end-to-end application that discovers real-world problems by scraping online forums (Reddit, Stack Overflow, GitHub Issues), analyzes them, and presents the top 50 problems with user counts and priorities. This tool helps identify the most pressing issues that developers and users face, enabling data-driven product development.

## Features

- 🔍 **Multi-Source Scraping**: Automatically scrapes problems from Reddit, Stack Overflow, and GitHub Issues
- 📊 **Problem Analysis**: Uses NLP to extract keywords, categorize problems, and identify patterns
- 🎯 **Smart Prioritization**: Ranks problems based on frequency and user engagement
- 🌐 **Web Dashboard**: Beautiful, interactive dashboard to visualize discovered problems
- 🔄 **Real-time Updates**: Refresh data and trigger new scrapes from the UI
- 📈 **Category Breakdown**: Automatically categorizes problems into domains (API, Database, Frontend, etc.)

## Architecture

The application consists of three main components:

1. **Scraper Module** (`scraper.py`): Collects data from various online forums
2. **Analyzer Module** (`analyzer.py`): Processes and prioritizes problems using NLP
3. **Web Application** (`app.py`): Flask-based API and dashboard for visualization

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/Rakshakh/AutonomousAppBuilder.git
cd AutonomousAppBuilder
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) Configure API keys:
```bash
cp .env.example .env
# Edit .env with your API keys (optional - app works without them)
```

## Usage

### Running the Application

1. Start the web server:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

3. Click "Start Scraping & Analysis" to begin discovering problems

### Configuration

Edit `config.json` to customize:

- **Sources to scrape**: Enable/disable Reddit, Stack Overflow, or GitHub
- **Subreddits**: Which subreddits to monitor
- **Tags**: Stack Overflow tags to search
- **Analysis parameters**: Minimum mentions, top problems count, etc.

Example configuration:
```json
{
  "scraping": {
    "enabled_sources": ["reddit", "stackoverflow", "github"],
    "max_posts_per_source": 100,
    "subreddits": ["learnprogramming", "webdev", "programming"]
  },
  "analysis": {
    "min_problem_mentions": 3,
    "top_problems_count": 50
  }
}
```

## API Endpoints

The application provides several REST API endpoints:

- `POST /api/scrape` - Trigger a new scraping operation
- `GET /api/analysis` - Get complete analysis results
- `GET /api/top-problems?limit=50` - Get top N problems
- `GET /api/categories` - Get problem categories breakdown
- `GET /api/keywords` - Get top keywords
- `GET /api/stats` - Get overall statistics

## How It Works

1. **Scraping**: The app queries public APIs from Reddit, Stack Overflow, and GitHub to collect recent posts, questions, and issues

2. **Analysis**: 
   - Extracts keywords using NLP (NLTK)
   - Groups similar problems together
   - Categorizes problems into domains
   - Calculates engagement scores

3. **Prioritization**:
   - Priority = (Frequency × 10) + (Engagement / 10)
   - Filters problems with minimum mentions threshold
   - Ranks by priority score

4. **Visualization**: Displays results in an interactive dashboard with real-time updates

## Data Sources

### Reddit
- Scrapes hot posts from configured subreddits
- Uses public JSON API (no authentication required)
- Captures: title, text, score, comments, timestamp

### Stack Overflow
- Queries questions by tags
- Uses Stack Exchange API v2.3
- Captures: title, score, views, answers, tags

### GitHub
- Searches open issues across all repositories
- Uses GitHub Search API
- Captures: title, body, comments, labels

## Categories

Problems are automatically categorized into:

- Authentication
- Database
- API
- Frontend
- Backend
- Deployment
- Performance
- Error Handling
- Testing
- Security
- General

## Requirements

See `requirements.txt` for all dependencies:
- Flask - Web framework
- requests - HTTP library
- beautifulsoup4 - HTML parsing
- praw - Reddit API wrapper
- nltk - Natural Language Toolkit
- pandas - Data analysis
- numpy - Numerical operations

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - feel free to use this project for any purpose

## Future Enhancements

- [ ] Add more data sources (Hacker News, Discord, Slack)
- [ ] Implement machine learning for better categorization
- [ ] Add sentiment analysis
- [ ] Create automated solution suggestions
- [ ] Build database persistence
- [ ] Add user authentication
- [ ] Export reports to PDF/CSV
- [ ] Implement trend tracking over time

## Troubleshooting

**Error: NLTK data not found**
- The app will automatically download required NLTK data on first run
- If issues persist, manually run: `python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"`

**Error: API rate limiting**
- The app uses public APIs which have rate limits
- Reduce `max_posts_per_source` in config.json
- Add API keys in .env for higher limits

**No problems found**
- Check your internet connection
- Verify config.json has valid subreddits/tags
- Try reducing `min_problem_mentions` threshold

## Contact

For questions or issues, please open an issue on GitHub.
