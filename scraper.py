"""
Scraper module for collecting problems from various online forums.
Supports Reddit, Stack Overflow, and GitHub Issues.
"""
import requests
from bs4 import BeautifulSoup
import json
import os
from typing import List, Dict
from datetime import datetime


class ForumScraper:
    """Base class for forum scrapers."""
    
    def __init__(self, config: dict):
        self.config = config
        self.problems = []
    
    def scrape(self) -> List[Dict]:
        """Scrape problems from the forum."""
        raise NotImplementedError("Subclasses must implement scrape()")


class RedditScraper(ForumScraper):
    """Scraper for Reddit posts."""
    
    def __init__(self, config: dict):
        super().__init__(config)
        self.subreddits = config.get('subreddits', [])
        self.max_posts = config.get('max_posts_per_source', 100)
    
    def scrape(self) -> List[Dict]:
        """Scrape problems from Reddit subreddits."""
        problems = []
        
        for subreddit in self.subreddits:
            try:
                # Using Reddit JSON API (no auth required for public posts)
                url = f"https://www.reddit.com/r/{subreddit}/hot.json"
                headers = {'User-Agent': 'AutonomousAppBuilder/1.0'}
                
                response = requests.get(url, headers=headers, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    posts = data.get('data', {}).get('children', [])
                    
                    for post in posts[:self.max_posts // len(self.subreddits)]:
                        post_data = post.get('data', {})
                        problem = {
                            'source': 'reddit',
                            'subreddit': subreddit,
                            'title': post_data.get('title', ''),
                            'text': post_data.get('selftext', ''),
                            'url': f"https://reddit.com{post_data.get('permalink', '')}",
                            'score': post_data.get('score', 0),
                            'num_comments': post_data.get('num_comments', 0),
                            'created_utc': post_data.get('created_utc', 0),
                            'timestamp': datetime.now().isoformat()
                        }
                        problems.append(problem)
                        
            except Exception as e:
                print(f"Error scraping r/{subreddit}: {str(e)}")
                continue
        
        return problems


class StackOverflowScraper(ForumScraper):
    """Scraper for Stack Overflow questions."""
    
    def __init__(self, config: dict):
        super().__init__(config)
        self.tags = config.get('stackoverflow_tags', [])
        self.max_posts = config.get('max_posts_per_source', 100)
    
    def scrape(self) -> List[Dict]:
        """Scrape problems from Stack Overflow."""
        problems = []
        
        for tag in self.tags:
            try:
                # Stack Overflow API (no auth required for basic queries)
                url = f"https://api.stackexchange.com/2.3/questions"
                params = {
                    'order': 'desc',
                    'sort': 'activity',
                    'tagged': tag,
                    'site': 'stackoverflow',
                    'pagesize': min(100, self.max_posts // len(self.tags))
                }
                
                response = requests.get(url, params=params, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    questions = data.get('items', [])
                    
                    for question in questions:
                        problem = {
                            'source': 'stackoverflow',
                            'tag': tag,
                            'title': question.get('title', ''),
                            'text': '',  # Would need separate API call for body
                            'url': question.get('link', ''),
                            'score': question.get('score', 0),
                            'view_count': question.get('view_count', 0),
                            'answer_count': question.get('answer_count', 0),
                            'created_utc': question.get('creation_date', 0),
                            'timestamp': datetime.now().isoformat()
                        }
                        problems.append(problem)
                        
            except Exception as e:
                print(f"Error scraping Stack Overflow tag '{tag}': {str(e)}")
                continue
        
        return problems


class GitHubScraper(ForumScraper):
    """Scraper for GitHub issues."""
    
    def __init__(self, config: dict):
        super().__init__(config)
        self.topics = config.get('github_topics', [])
        self.max_posts = config.get('max_posts_per_source', 100)
    
    def scrape(self) -> List[Dict]:
        """Scrape problems from GitHub issues."""
        problems = []
        
        # Search for issues across all repositories
        try:
            for topic in self.topics:
                url = "https://api.github.com/search/issues"
                params = {
                    'q': f'is:issue is:open label:{topic}',
                    'sort': 'updated',
                    'order': 'desc',
                    'per_page': min(100, self.max_posts // len(self.topics))
                }
                headers = {'Accept': 'application/vnd.github.v3+json'}
                
                response = requests.get(url, params=params, headers=headers, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    issues = data.get('items', [])
                    
                    for issue in issues:
                        problem = {
                            'source': 'github',
                            'topic': topic,
                            'title': issue.get('title', ''),
                            'text': issue.get('body', ''),
                            'url': issue.get('html_url', ''),
                            'comments': issue.get('comments', 0),
                            'created_at': issue.get('created_at', ''),
                            'timestamp': datetime.now().isoformat()
                        }
                        problems.append(problem)
                        
        except Exception as e:
            print(f"Error scraping GitHub issues: {str(e)}")
        
        return problems


def scrape_all_sources(config: dict) -> List[Dict]:
    """Scrape all enabled sources and return combined problems."""
    all_problems = []
    enabled_sources = config.get('scraping', {}).get('enabled_sources', [])
    scraping_config = config.get('scraping', {})
    
    if 'reddit' in enabled_sources:
        print("Scraping Reddit...")
        reddit_scraper = RedditScraper(scraping_config)
        all_problems.extend(reddit_scraper.scrape())
    
    if 'stackoverflow' in enabled_sources:
        print("Scraping Stack Overflow...")
        stackoverflow_scraper = StackOverflowScraper(scraping_config)
        all_problems.extend(stackoverflow_scraper.scrape())
    
    if 'github' in enabled_sources:
        print("Scraping GitHub...")
        github_scraper = GitHubScraper(scraping_config)
        all_problems.extend(github_scraper.scrape())
    
    print(f"Total problems scraped: {len(all_problems)}")
    return all_problems
