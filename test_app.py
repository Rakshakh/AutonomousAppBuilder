#!/usr/bin/env python
"""
Test script to verify the application functionality.
"""
import json
import requests
import time


def test_scraping():
    """Test the scraping and analysis functionality."""
    base_url = "http://localhost:5000"
    
    print("🧪 Testing Autonomous App Builder")
    print("=" * 50)
    
    # Test 1: Check if server is running
    print("\n1. Testing server connection...")
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✅ Server is running")
        else:
            print(f"❌ Server returned status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to server: {e}")
        return False
    
    # Test 2: Trigger scraping
    print("\n2. Testing scraping functionality...")
    print("   (This may take a few minutes...)")
    try:
        response = requests.post(f"{base_url}/api/scrape", timeout=300)
        data = response.json()
        
        if data.get('success'):
            print(f"✅ Scraping completed: {data.get('message')}")
        else:
            print(f"❌ Scraping failed: {data.get('error')}")
            return False
    except Exception as e:
        print(f"❌ Scraping test failed: {e}")
        return False
    
    # Wait a moment for data to be processed
    time.sleep(2)
    
    # Test 3: Check stats
    print("\n3. Testing stats endpoint...")
    try:
        response = requests.get(f"{base_url}/api/stats")
        stats = response.json()
        
        print(f"   Total problems scraped: {stats.get('total_problems', 0)}")
        print(f"   Top problems identified: {stats.get('top_problems_count', 0)}")
        print(f"   Categories found: {stats.get('categories_count', 0)}")
        print(f"   Sources: {', '.join(stats.get('sources', {}).keys())}")
        print("✅ Stats endpoint working")
    except Exception as e:
        print(f"❌ Stats test failed: {e}")
        return False
    
    # Test 4: Check top problems
    print("\n4. Testing top problems endpoint...")
    try:
        response = requests.get(f"{base_url}/api/top-problems?limit=5")
        data = response.json()
        
        top_problems = data.get('top_problems', [])
        if top_problems:
            print(f"   Found {len(top_problems)} top problems")
            print("\n   Sample problems:")
            for i, problem in enumerate(top_problems[:3], 1):
                print(f"   {i}. {problem.get('title', 'N/A')[:60]}...")
                print(f"      Category: {problem.get('category', 'N/A')}")
                print(f"      Users affected: {problem.get('users_affected', 0)}")
                print(f"      Priority: {int(problem.get('priority', 0))}")
            print("✅ Top problems endpoint working")
        else:
            print("⚠️  No top problems found (this might be okay if scraping didn't find duplicates)")
    except Exception as e:
        print(f"❌ Top problems test failed: {e}")
        return False
    
    # Test 5: Check categories
    print("\n5. Testing categories endpoint...")
    try:
        response = requests.get(f"{base_url}/api/categories")
        data = response.json()
        
        categories = data.get('categories', {})
        if categories:
            print(f"   Found {len(categories)} categories:")
            for category, count in list(categories.items())[:5]:
                print(f"   - {category}: {count} problems")
            print("✅ Categories endpoint working")
        else:
            print("⚠️  No categories found")
    except Exception as e:
        print(f"❌ Categories test failed: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("✅ All tests passed successfully!")
    print("\n📊 You can now view the dashboard at http://localhost:5000")
    return True


if __name__ == "__main__":
    success = test_scraping()
    exit(0 if success else 1)
