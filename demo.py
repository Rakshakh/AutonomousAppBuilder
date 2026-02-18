"""
Demo script that generates mock data to demonstrate the application functionality.
This is useful for testing when external APIs are not accessible.
"""
import json
from datetime import datetime
from analyzer import ProblemAnalyzer


def generate_mock_data():
    """Generate mock problem data for demonstration."""
    # Generate problems with duplicates to show grouping
    mock_problems = [
        # Problem 1: JavaScript undefined errors (4 occurrences)
        {
            'source': 'reddit',
            'subreddit': 'learnprogramming',
            'title': 'How to fix "Cannot read property of undefined" in JavaScript',
            'text': 'I keep getting this error when trying to access object properties. Any help?',
            'url': 'https://reddit.com/r/learnprogramming/example1',
            'score': 45,
            'num_comments': 12,
            'created_utc': 1708260000,
            'timestamp': datetime.now().isoformat()
        },
        {
            'source': 'stackoverflow',
            'tag': 'javascript',
            'title': 'Cannot read property undefined JavaScript',
            'text': 'Getting undefined property error in my JavaScript code',
            'url': 'https://stackoverflow.com/questions/example1',
            'score': 78,
            'view_count': 2345,
            'answer_count': 8,
            'created_utc': 1708260050,
            'timestamp': datetime.now().isoformat()
        },
        {
            'source': 'github',
            'topic': 'bug',
            'title': 'Fix: Cannot read property of undefined',
            'text': 'Users reporting undefined property errors',
            'url': 'https://github.com/example/repo/issues/1',
            'comments': 15,
            'created_at': '2024-02-18T10:00:00Z',
            'timestamp': datetime.now().isoformat()
        },
        {
            'source': 'reddit',
            'subreddit': 'javascript',
            'title': 'Undefined property error - need help',
            'text': 'How to prevent cannot read property of undefined?',
            'url': 'https://reddit.com/r/javascript/example1',
            'score': 56,
            'num_comments': 19,
            'created_utc': 1708260075,
            'timestamp': datetime.now().isoformat()
        },
        # Problem 2: Django authentication (4 occurrences)
        {
            'source': 'stackoverflow',
            'tag': 'python',
            'title': 'Django authentication not working after deployment',
            'text': 'My Django app works locally but authentication fails in production',
            'url': 'https://stackoverflow.com/questions/example2',
            'score': 123,
            'view_count': 4567,
            'answer_count': 12,
            'created_utc': 1708260100,
            'timestamp': datetime.now().isoformat()
        },
        {
            'source': 'reddit',
            'subreddit': 'django',
            'title': 'Django authentication failing in production',
            'text': 'Auth works locally but not after deployment',
            'url': 'https://reddit.com/r/django/example1',
            'score': 89,
            'num_comments': 23,
            'created_utc': 1708260125,
            'timestamp': datetime.now().isoformat()
        },
        {
            'source': 'github',
            'topic': 'bug',
            'title': 'Authentication not working after deploy',
            'text': 'Django authentication broken in production environment',
            'url': 'https://github.com/django/django/issues/1',
            'comments': 34,
            'created_at': '2024-02-18T10:30:00Z',
            'timestamp': datetime.now().isoformat()
        },
        {
            'source': 'stackoverflow',
            'tag': 'django',
            'title': 'Production authentication issues Django',
            'text': 'Cannot authenticate users after deploying to AWS',
            'url': 'https://stackoverflow.com/questions/example3',
            'score': 67,
            'view_count': 2345,
            'answer_count': 7,
            'created_utc': 1708260150,
            'timestamp': datetime.now().isoformat()
        },
        # Problem 3: React component not re-rendering (5 occurrences)
        {
            'source': 'reddit',
            'subreddit': 'webdev',
            'title': 'React component not re-rendering after state change',
            'text': 'State is updating but component does not re-render',
            'url': 'https://reddit.com/r/webdev/example2',
            'score': 167,
            'num_comments': 45,
            'created_utc': 1708260200,
            'timestamp': datetime.now().isoformat()
        },
        {
            'source': 'stackoverflow',
            'tag': 'react',
            'title': 'Component not updating after setState',
            'text': 'React component not re-rendering when state changes',
            'url': 'https://stackoverflow.com/questions/example4',
            'score': 234,
            'view_count': 8901,
            'answer_count': 15,
            'created_utc': 1708260225,
            'timestamp': datetime.now().isoformat()
        },
        {
            'source': 'github',
            'topic': 'question',
            'title': 'React not re-rendering on state update',
            'text': 'Component state changes but UI does not update',
            'url': 'https://github.com/facebook/react/issues/1',
            'comments': 56,
            'created_at': '2024-02-18T11:00:00Z',
            'timestamp': datetime.now().isoformat()
        },
        {
            'source': 'reddit',
            'subreddit': 'reactjs',
            'title': 'useState not triggering re-render',
            'text': 'State updates but component does not re-render',
            'url': 'https://reddit.com/r/reactjs/example1',
            'score': 145,
            'num_comments': 38,
            'created_utc': 1708260250,
            'timestamp': datetime.now().isoformat()
        },
        {
            'source': 'stackoverflow',
            'tag': 'react',
            'title': 'React hooks not causing re-render',
            'text': 'Using useState but component not updating',
            'url': 'https://stackoverflow.com/questions/example5',
            'score': 98,
            'view_count': 3456,
            'answer_count': 9,
            'created_utc': 1708260275,
            'timestamp': datetime.now().isoformat()
        },
        # Problem 4: Database connection timeout (4 occurrences)
        {
            'source': 'github',
            'topic': 'bug',
            'title': 'Database connection timeout in production',
            'text': 'Getting timeout errors when connecting to PostgreSQL database',
            'url': 'https://github.com/example/repo/issues/2',
            'comments': 28,
            'created_at': '2024-02-18T11:30:00Z',
            'timestamp': datetime.now().isoformat()
        },
        {
            'source': 'stackoverflow',
            'tag': 'postgresql',
            'title': 'PostgreSQL connection timeouts under load',
            'text': 'Database connection timing out in production',
            'url': 'https://stackoverflow.com/questions/example6',
            'score': 156,
            'view_count': 5678,
            'answer_count': 11,
            'created_utc': 1708260300,
            'timestamp': datetime.now().isoformat()
        },
        {
            'source': 'reddit',
            'subreddit': 'webdev',
            'title': 'Database timeout errors in production',
            'text': 'PostgreSQL connections timing out under high traffic',
            'url': 'https://reddit.com/r/webdev/example3',
            'score': 123,
            'num_comments': 34,
            'created_utc': 1708260325,
            'timestamp': datetime.now().isoformat()
        },
        {
            'source': 'github',
            'topic': 'bug',
            'title': 'Connection pool timeout PostgreSQL',
            'text': 'Database connections timing out under load',
            'url': 'https://github.com/example/app/issues/1',
            'comments': 19,
            'created_at': '2024-02-18T12:00:00Z',
            'timestamp': datetime.now().isoformat()
        },
        # Problem 5: CORS errors (3 occurrences)
        {
            'source': 'stackoverflow',
            'tag': 'web-development',
            'title': 'CORS error when calling API from frontend',
            'text': 'Getting blocked by CORS policy when making requests',
            'url': 'https://stackoverflow.com/questions/example7',
            'score': 289,
            'view_count': 12345,
            'answer_count': 18,
            'created_utc': 1708260350,
            'timestamp': datetime.now().isoformat()
        },
        {
            'source': 'reddit',
            'subreddit': 'webdev',
            'title': 'CORS policy blocking my API requests',
            'text': 'How to fix CORS errors in production?',
            'url': 'https://reddit.com/r/webdev/example4',
            'score': 198,
            'num_comments': 47,
            'created_utc': 1708260375,
            'timestamp': datetime.now().isoformat()
        },
        {
            'source': 'github',
            'topic': 'question',
            'title': 'CORS error calling backend API',
            'text': 'Frontend blocked by CORS policy',
            'url': 'https://github.com/example/api/issues/1',
            'comments': 23,
            'created_at': '2024-02-18T12:30:00Z',
            'timestamp': datetime.now().isoformat()
        },
        # Problem 6: API rate limiting (3 occurrences)
        {
            'source': 'reddit',
            'subreddit': 'programming',
            'title': 'API rate limiting best practices',
            'text': 'How do you implement rate limiting for REST APIs?',
            'url': 'https://reddit.com/r/programming/example5',
            'score': 234,
            'num_comments': 67,
            'created_utc': 1708260400,
            'timestamp': datetime.now().isoformat()
        },
        {
            'source': 'stackoverflow',
            'tag': 'api',
            'title': 'Implementing API rate limiting',
            'text': 'Best way to add rate limiting to REST API',
            'url': 'https://stackoverflow.com/questions/example8',
            'score': 178,
            'view_count': 6789,
            'answer_count': 13,
            'created_utc': 1708260425,
            'timestamp': datetime.now().isoformat()
        },
        {
            'source': 'github',
            'topic': 'feature-request',
            'title': 'Add rate limiting to API endpoints',
            'text': 'Need to implement rate limiting for production',
            'url': 'https://github.com/example/api/issues/2',
            'comments': 31,
            'created_at': '2024-02-18T13:00:00Z',
            'timestamp': datetime.now().isoformat()
        },
        # Problem 7: Async/await error handling (3 occurrences)
        {
            'source': 'stackoverflow',
            'tag': 'javascript',
            'title': 'How to properly handle async/await errors in Node.js',
            'text': 'Best practices for error handling with async/await',
            'url': 'https://stackoverflow.com/questions/example9',
            'score': 245,
            'view_count': 9876,
            'answer_count': 16,
            'created_utc': 1708260450,
            'timestamp': datetime.now().isoformat()
        },
        {
            'source': 'reddit',
            'subreddit': 'node',
            'title': 'Error handling with async/await',
            'text': 'How to catch async errors in Node.js?',
            'url': 'https://reddit.com/r/node/example1',
            'score': 134,
            'num_comments': 42,
            'created_utc': 1708260475,
            'timestamp': datetime.now().isoformat()
        },
        {
            'source': 'github',
            'topic': 'question',
            'title': 'Async/await error handling patterns',
            'text': 'Need guidance on handling async errors',
            'url': 'https://github.com/nodejs/node/issues/1',
            'comments': 27,
            'created_at': '2024-02-18T13:30:00Z',
            'timestamp': datetime.now().isoformat()
        },
        # Additional variety problems (1-2 occurrences each)
        {
            'source': 'stackoverflow',
            'tag': 'react',
            'title': 'React hooks dependency array confusion',
            'text': 'When should I include functions in the dependency array?',
            'url': 'https://stackoverflow.com/questions/example10',
            'score': 167,
            'view_count': 5432,
            'answer_count': 10,
            'created_utc': 1708260500,
            'timestamp': datetime.now().isoformat()
        },
        {
            'source': 'reddit',
            'subreddit': 'webdev',
            'title': 'Slow database queries in production',
            'text': 'Queries are fast locally but slow in production',
            'url': 'https://reddit.com/r/webdev/example6',
            'score': 112,
            'num_comments': 29,
            'created_utc': 1708260525,
            'timestamp': datetime.now().isoformat()
        },
        {
            'source': 'github',
            'topic': 'bug',
            'title': 'Memory leak in React application',
            'text': 'App slows down over time, memory usage keeps increasing',
            'url': 'https://github.com/example/app/issues/2',
            'comments': 18,
            'created_at': '2024-02-18T14:00:00Z',
            'timestamp': datetime.now().isoformat()
        },
        {
            'source': 'stackoverflow',
            'tag': 'docker',
            'title': 'Docker deployment configuration issues',
            'text': 'App works locally but fails in Docker container',
            'url': 'https://stackoverflow.com/questions/example11',
            'score': 145,
            'view_count': 4321,
            'answer_count': 9,
            'created_utc': 1708260550,
            'timestamp': datetime.now().isoformat()
        },
    ]
    
    return mock_problems


def run_demo():
    """Run the demo with mock data."""
    print("🎭 Running Demo with Mock Data")
    print("=" * 60)
    
    # Load configuration
    with open('config.json', 'r') as f:
        config = json.load(f)
    
    # Generate mock problems
    print("\n1. Generating mock problems...")
    problems = generate_mock_data()
    print(f"   ✅ Generated {len(problems)} mock problems")
    
    # Analyze problems
    print("\n2. Analyzing problems...")
    analyzer = ProblemAnalyzer(config)
    analysis = analyzer.analyze_problems(problems)
    print(f"   ✅ Analysis complete")
    
    # Display results
    print("\n3. Results:")
    print(f"   📊 Total problems: {analysis['total_problems']}")
    print(f"   🔥 Top problems identified: {len(analysis['top_problems'])}")
    print(f"   📁 Categories: {len(analysis['categories'])}")
    print(f"   🌐 Sources: {len(analysis['sources'])}")
    
    # Show top 10 problems
    print("\n4. Top 10 Problems (by priority):")
    print("   " + "-" * 56)
    for i, problem in enumerate(analysis['top_problems'][:10], 1):
        print(f"\n   {i}. {problem['title'][:50]}...")
        print(f"      Category: {problem['category']}")
        print(f"      Users affected: {problem['users_affected']}")
        print(f"      Priority score: {int(problem['priority'])}")
        print(f"      Total engagement: {int(problem['total_engagement'])}")
    
    # Show categories
    print("\n5. Problem Categories:")
    print("   " + "-" * 56)
    for category, count in sorted(analysis['categories'].items(), key=lambda x: x[1], reverse=True):
        print(f"   {category:.<40} {count:>3} problems")
    
    # Show sources
    print("\n6. Data Sources:")
    print("   " + "-" * 56)
    for source, count in analysis['sources'].items():
        print(f"   {source:.<40} {count:>3} items")
    
    # Save demo data for the web app
    print("\n7. Saving demo data for web application...")
    demo_data = {
        'analysis': analysis,
        'timestamp': datetime.now().isoformat()
    }
    with open('demo_data.json', 'w') as f:
        json.dump(demo_data, f, indent=2)
    print("   ✅ Demo data saved to demo_data.json")
    
    print("\n" + "=" * 60)
    print("✅ Demo completed successfully!")
    print("\n💡 This demonstrates how the application would work with real data.")
    print("   In a production environment, it would scrape live data from:")
    print("   - Reddit (subreddits)")
    print("   - Stack Overflow (questions)")
    print("   - GitHub (issues)")
    

if __name__ == "__main__":
    run_demo()
