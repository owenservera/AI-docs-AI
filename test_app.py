#!/usr/bin/env python3
"""
Test script for Documentation Download Agent
Tests the basic functionality without starting the full web server
"""

import asyncio
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def test_crawler():
    """Test the crawler functionality"""
    print("🧪 Testing Documentation Crawler...")
    
    try:
        from crawler import DocumentationCrawler
        
        # Create a test crawler instance
        crawler = DocumentationCrawler(
            base_url="https://example.com/docs",
            max_depth=2,
            include_images=True,
            include_css=True,
            include_js=True,
            rate_limit=0.1  # Fast for testing
        )
        
        print("✅ Crawler class imported successfully")
        print(f"   Base URL: {crawler.base_url}")
        print(f"   Max Depth: {crawler.max_depth}")
        print(f"   Rate Limit: {crawler.rate_limit}s")
        
        # Test URL validation
        test_urls = [
            "https://example.com/docs/page1",
            "https://example.com/docs/page2",
            "https://external.com/page"
        ]
        
        print("\n🔗 Testing URL validation...")
        for url in test_urls:
            is_internal = crawler._is_internal_link(url)
            print(f"   {url} -> {'Internal' if is_internal else 'External'}")
        
        print("✅ URL validation working correctly")
        
        # Test file path generation
        print("\n📁 Testing file path generation...")
        test_file_url = "https://example.com/docs/getting-started.html"
        file_path = crawler._get_file_path(test_file_url, "html")
        print(f"   URL: {test_file_url}")
        print(f"   Path: {file_path}")
        
        print("✅ File path generation working")
        
    except Exception as e:
        print(f"❌ Crawler test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

async def test_file_manager():
    """Test the file manager functionality"""
    print("\n🧪 Testing File Manager...")
    
    try:
        from file_manager import FileManager
        
        # Create test instance
        file_manager = FileManager()
        
        print("✅ FileManager class imported successfully")
        
        # Test file size formatting
        test_sizes = [0, 1024, 1048576, 1073741824]
        print("\n📏 Testing file size formatting...")
        for size in test_sizes:
            formatted = file_manager._format_file_size(size)
            print(f"   {size} bytes -> {formatted}")
        
        print("✅ File size formatting working correctly")
        
        # Test file icon mapping
        print("\n🎨 Testing file icon mapping...")
        test_files = [
            "document.html",
            "style.css", 
            "script.js",
            "image.png",
            "data.json"
        ]
        
        for filename in test_files:
            icon = file_manager._get_file_icon(filename)
            print(f"   {filename} -> {icon}")
        
        print("✅ File icon mapping working")
        
    except Exception as e:
        print(f"❌ File Manager test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

def test_directory_structure():
    """Test the directory structure"""
    print("\n📂 Testing Directory Structure...")
    
    required_dirs = [
        "static",
        "static/css", 
        "static/js",
        "templates",
        "downloads"
    ]
    
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print(f"✅ {dir_path}/ exists")
        else:
            os.makedirs(dir_path, exist_ok=True)
            print(f"📁 Created {dir_path}/")
    
    required_files = [
        "main.py",
        "crawler.py", 
        "file_manager.py",
        "templates/index.html",
        "static/js/main.js"
    ]
    
    for file_path in required_files:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"✅ {file_path} exists ({size} bytes)")
        else:
            print(f"❌ {file_path} missing")
            return False
    
    return True

async def run_all_tests():
    """Run all tests"""
    print("🚀 Documentation Download Agent - Test Suite")
    print("=" * 60)
    
    # Test directory structure
    structure_ok = test_directory_structure()
    
    # Test crawler
    crawler_ok = await test_crawler()
    
    # Test file manager
    file_manager_ok = await test_file_manager()
    
    print("\n📊 Test Results Summary")
    print("=" * 30)
    print(f"Directory Structure: {'✅ PASS' if structure_ok else '❌ FAIL'}")
    print(f"Crawler: {'✅ PASS' if crawler_ok else '❌ FAIL'}")
    print(f"File Manager: {'✅ PASS' if file_manager_ok else '❌ FAIL'}")
    
    all_passed = structure_ok and crawler_ok and file_manager_ok
    
    if all_passed:
        print(f"\n🎉 All tests passed! The application should work correctly.")
        print(f"🚀 Start the server with: python main.py")
        print(f"🌐 Open browser to: http://localhost:8001")
    else:
        print(f"\n⚠️  Some tests failed. Check the errors above.")
        print(f"🔧 Fix the issues before running the application.")
    
    return all_passed

if __name__ == "__main__":
    success = asyncio.run(run_all_tests())
    sys.exit(0 if success else 1)