"""
Problem analyzer module for identifying, categorizing, and prioritizing problems.
"""
import re
from collections import Counter
from typing import List, Dict
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


class ProblemAnalyzer:
    """Analyze and prioritize problems from scraped data."""
    
    def __init__(self, config: dict):
        self.config = config
        self.analysis_config = config.get('analysis', {})
        self.min_mentions = self.analysis_config.get('min_problem_mentions', 3)
        self.top_count = self.analysis_config.get('top_problems_count', 50)
        
        # Download NLTK data if not already present
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            print("Downloading NLTK punkt tokenizer...")
            nltk.download('punkt', quiet=True)
        
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            print("Downloading NLTK stopwords...")
            nltk.download('stopwords', quiet=True)
    
    def extract_keywords(self, text: str) -> List[str]:
        """Extract meaningful keywords from text."""
        if not text:
            return []
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+', '', text)
        
        # Remove special characters but keep spaces
        text = re.sub(r'[^a-z0-9\s]', ' ', text)
        
        # Tokenize
        try:
            tokens = word_tokenize(text)
        except:
            tokens = text.split()
        
        # Remove stopwords
        try:
            stop_words = set(stopwords.words('english'))
        except:
            stop_words = set(['the', 'is', 'at', 'which', 'on', 'a', 'an', 'and', 'or', 'but'])
        
        keywords = [word for word in tokens if word not in stop_words and len(word) > 2]
        
        return keywords
    
    def categorize_problem(self, problem: Dict) -> str:
        """Categorize a problem based on keywords."""
        text = f"{problem.get('title', '')} {problem.get('text', '')}".lower()
        
        categories = {
            'Authentication': ['login', 'auth', 'authentication', 'password', 'oauth', 'jwt', 'token'],
            'Database': ['database', 'sql', 'mysql', 'postgres', 'mongodb', 'query', 'orm'],
            'API': ['api', 'rest', 'graphql', 'endpoint', 'request', 'response'],
            'Frontend': ['react', 'vue', 'angular', 'css', 'html', 'ui', 'component', 'dom'],
            'Backend': ['server', 'node', 'express', 'django', 'flask', 'backend'],
            'Deployment': ['deploy', 'deployment', 'docker', 'kubernetes', 'ci/cd', 'hosting'],
            'Performance': ['slow', 'performance', 'speed', 'optimization', 'cache', 'memory'],
            'Error Handling': ['error', 'exception', 'crash', 'bug', 'fail', 'broken'],
            'Testing': ['test', 'testing', 'unit test', 'integration', 'jest', 'pytest'],
            'Security': ['security', 'vulnerability', 'xss', 'csrf', 'injection', 'encryption']
        }
        
        for category, keywords in categories.items():
            if any(keyword in text for keyword in keywords):
                return category
        
        return 'General'
    
    def analyze_problems(self, problems: List[Dict]) -> Dict:
        """Analyze problems and return insights."""
        if not problems:
            return {
                'total_problems': 0,
                'top_problems': [],
                'categories': {},
                'sources': {}
            }
        
        # Extract all keywords and titles
        all_keywords = []
        problem_titles = []
        categories = Counter()
        sources = Counter()
        
        for problem in problems:
            # Extract keywords
            title = problem.get('title', '')
            text = problem.get('text', '')
            combined_text = f"{title} {text}"
            keywords = self.extract_keywords(combined_text)
            all_keywords.extend(keywords)
            
            # Store title for problem identification
            if title:
                problem_titles.append({
                    'title': title,
                    'keywords': keywords,
                    'category': self.categorize_problem(problem),
                    'source': problem.get('source', 'unknown'),
                    'url': problem.get('url', ''),
                    'score': problem.get('score', 0),
                    'engagement': self._calculate_engagement(problem)
                })
            
            # Count categories
            category = self.categorize_problem(problem)
            categories[category] += 1
            
            # Count sources
            source = problem.get('source', 'unknown')
            sources[source] += 1
        
        # Find most common keywords
        keyword_counts = Counter(all_keywords)
        
        # Group similar problems
        grouped_problems = self._group_similar_problems(problem_titles)
        
        # Rank problems by frequency and engagement
        ranked_problems = self._rank_problems(grouped_problems)
        
        return {
            'total_problems': len(problems),
            'top_problems': ranked_problems[:self.top_count],
            'top_keywords': keyword_counts.most_common(50),
            'categories': dict(categories.most_common()),
            'sources': dict(sources)
        }
    
    def _calculate_engagement(self, problem: Dict) -> int:
        """Calculate engagement score for a problem."""
        score = 0
        
        # Different scoring based on source
        if problem.get('source') == 'reddit':
            score += problem.get('score', 0)
            score += problem.get('num_comments', 0) * 2
        elif problem.get('source') == 'stackoverflow':
            score += problem.get('score', 0)
            score += problem.get('answer_count', 0) * 3
            score += problem.get('view_count', 0) // 100
        elif problem.get('source') == 'github':
            score += problem.get('comments', 0) * 2
        
        return score
    
    def _group_similar_problems(self, problems: List[Dict]) -> List[Dict]:
        """Group similar problems together."""
        grouped = {}
        
        for problem in problems:
            # Use first 5 keywords as a signature
            signature = ' '.join(sorted(problem['keywords'][:5]))
            
            if signature in grouped:
                grouped[signature]['count'] += 1
                grouped[signature]['total_engagement'] += problem['engagement']
                grouped[signature]['examples'].append({
                    'title': problem['title'],
                    'url': problem['url'],
                    'source': problem['source']
                })
            else:
                grouped[signature] = {
                    'title': problem['title'],
                    'keywords': problem['keywords'][:5],
                    'category': problem['category'],
                    'count': 1,
                    'total_engagement': problem['engagement'],
                    'examples': [{
                        'title': problem['title'],
                        'url': problem['url'],
                        'source': problem['source']
                    }]
                }
        
        return list(grouped.values())
    
    def _rank_problems(self, grouped_problems: List[Dict]) -> List[Dict]:
        """Rank problems by frequency and engagement."""
        # Calculate priority score
        for problem in grouped_problems:
            # Priority = (frequency * 10) + (engagement / 10)
            frequency_score = problem['count'] * 10
            engagement_score = problem['total_engagement'] / 10
            problem['priority'] = frequency_score + engagement_score
            problem['users_affected'] = problem['count']
        
        # Sort by priority
        ranked = sorted(grouped_problems, key=lambda x: x['priority'], reverse=True)
        
        # Filter by minimum mentions
        ranked = [p for p in ranked if p['count'] >= self.min_mentions]
        
        return ranked
