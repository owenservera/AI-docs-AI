#!/usr/bin/env python3
"""
Documentation Download Agent - Demo Script
This script demonstrates how to use the Documentation Download Agent
"""

import asyncio
import aiohttp
import json
from datetime import datetime

async def demo_crawl():
    """Demonstrate the crawling process with a sample documentation site"""
    
    print("🚀 Documentation Download Agent Demo")
    print("=" * 50)
    
    # Example: Using a public documentation site
    demo_url = "https://docs.python.org/3/"
    
    print(f"\n📚 Target URL: {demo_url}")
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Configuration
    config = {
        "url": demo_url,
        "max_depth": 2,  # Shallow crawl for demo
        "include_images": True,
        "include_css": True,
        "include_js": True,
        "rate_limit": 1.0,  # 1 second between requests
        "user_agent": "DocumentationAgent/1.0-Demo"
    }
    
    print(f"\n⚙️ Configuration:")
    for key, value in config.items():
        print(f"   {key}: {value}")
    
    print(f"\n🔄 Starting crawl process...")
    print(f"   This will take a few moments...")
    
    # Simulate the crawling process
    await asyncio.sleep(2)
    
    # Mock results for demonstration
    mock_results = {
        "status": "completed",
        "pages_found": 45,
        "pages_downloaded": 42,
        "errors": [],
        "total_size_mb": 15.7,
        "download_time_seconds": 127,
        "files_created": {
            "html_files": 42,
            "css_files": 8,
            "js_files": 5,
            "image_files": 23,
            "font_files": 4
        }
    }
    
    print(f"\n✅ Crawl completed successfully!")
    print(f"📊 Results:")
    print(f"   Pages found: {mock_results['pages_found']}")
    print(f"   Pages downloaded: {mock_results['pages_downloaded']}")
    print(f"   Total size: {mock_results['total_size_mb']} MB")
    print(f"   Download time: {mock_results['download_time_seconds']} seconds")
    print(f"   Files created:")
    for file_type, count in mock_results['files_created'].items():
        print(f"     {file_type}: {count}")
    
    print(f"\n📁 Generated files:")
    print(f"   📄 index.html - Navigation index")
    print(f"   📄 documentation_*.zip - Complete archive")
    print(f"   📁 downloads/ - Local file structure")
    
    print(f"\n🎯 Next steps:")
    print(f"   1. Open the web interface")
    print(f"   2. Browse the downloaded files")
    print(f"   3. Download the ZIP archive")
    print(f"   4. Use offline documentation")
    
    print(f"\n💡 Tips:")
    print(f"   - Use lower depth for faster downloads")
    print(f"   - Enable rate limiting for respectful crawling")
    print(f"   - Filter file types to reduce size")
    print(f"   - Check error logs for any issues")

async def demo_api_calls():
    """Demonstrate API usage"""
    
    print(f"\n🔌 API Usage Examples")
    print("=" * 30)
    
    base_url = "http://localhost:8001"
    
    examples = [
        {
            "method": "POST",
            "endpoint": "/api/start_crawl",
            "description": "Start a new documentation crawl",
            "payload": {
                "url": "https://docs.example.com/",
                "max_depth": 3,
                "include_images": True,
                "include_css": True,
                "include_js": True,
                "rate_limit": 1.0
            }
        },
        {
            "method": "GET",
            "endpoint": "/api/crawl_status/{crawl_id}",
            "description": "Check crawling progress"
        },
        {
            "method": "GET",
            "endpoint": "/api/list_files/{crawl_id}",
            "description": "List downloaded files"
        },
        {
            "method": "GET",
            "endpoint": "/api/download_zip/{crawl_id}",
            "description": "Download ZIP archive"
        }
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"\n{i}. {example['description']}")
        print(f"   {example['method']} {base_url}{example['endpoint']}")
        
        if 'payload' in example:
            print(f"   Payload: {json.dumps(example['payload'], indent=4)}")

def demo_ui_features():
    """Demonstrate UI features"""
    
    print(f"\n🎨 UI Features")
    print("=" * 20)
    
    features = [
        "Dark theme with neon accents",
        "Real-time progress tracking",
        "File browser with search",
        "Advanced configuration options",
        "Error logging and notifications",
        "Responsive design",
        "Keyboard shortcuts (Ctrl+Enter to start)",
        "Animated transitions and effects"
    ]
    
    for i, feature in enumerate(features, 1):
        print(f"{i}. {feature}")

async def main():
    """Run all demos"""
    
    await demo_crawl()
    await demo_api_calls()
    demo_ui_features()
    
    print(f"\n🎉 Demo completed!")
    print(f"📖 Check README.md for detailed documentation")
    print(f"🚀 Start the application with: python main.py")
    print(f"🌐 Open browser to: http://localhost:8001")

if __name__ == "__main__":
    asyncio.run(main())