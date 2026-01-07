# Quick Start Guide - Documentation Download Agent

## 🚀 Getting Started (5 minutes)

### Option 1: Quick Start (Recommended)
```bash
# 1. Clone or download the files
# 2. Run the startup script
./start.sh

# Or manually:
pip3 install -r requirements.txt
python3 main.py
```

### Option 2: Using the Live Demo
Visit: https://rixf47dn27al6.ok.kimi.link

## 📖 Basic Usage

### 1. Enter Documentation URL
- Paste the root URL of any documentation site
- Examples:
  - `https://docs.python.org/3/`
  - `https://developer.mozilla.org/en-US/docs/Web`
  - `https://docs.github.com/`

### 2. Configure Options (Optional)
- **Max Depth**: How many link levels to follow (default: 3)
- **Rate Limit**: Delay between requests in seconds (default: 1.0)
- **File Types**: Choose what to download (Images, CSS, JS, Fonts)

### 3. Start Crawling
- Click "Start Crawling" button
- Watch real-time progress
- Monitor pages found/downloaded
- View current page being processed

### 4. Download Results
- Browse downloaded files in the interface
- Use search to find specific files
- Click "Download ZIP" to get everything

## 🎯 Example Workflows

### Downloading Python Documentation
1. URL: `https://docs.python.org/3/`
2. Max Depth: 3
3. Include: All file types
4. Rate Limit: 1.0 seconds
5. Expected: ~200+ pages, ~50MB

### Archiving a JavaScript Guide
1. URL: `https://javascript.info/`
2. Max Depth: 2
3. Include: HTML, CSS, JS only
4. Rate Limit: 2.0 seconds
5. Expected: ~100 pages, ~20MB

### Backing Up API Documentation
1. URL: `https://api.example.com/docs`
2. Max Depth: 4
3. Include: All file types
4. Rate Limit: 0.5 seconds
5. Expected: Varies by site size

## ⚙️ Configuration Options

### Max Depth Levels
- **1**: Only the starting page
- **2**: Starting page + direct links
- **3**: Comprehensive coverage (recommended)
- **4-5**: Deep crawling (large sites)

### Rate Limiting
- **0.5s**: Fast crawling (your own sites)
- **1.0s**: Normal speed (recommended)
- **2.0s**: Respectful crawling
- **5.0s**: Very conservative

### File Type Filters
- **Images**: PNG, JPG, SVG, GIF files
- **CSS**: Stylesheets for appearance
- **JavaScript**: Interactive features
- **Fonts**: Web fonts for typography

## 📊 Understanding the Interface

### Status Dashboard
- **Status**: Current crawling state
- **Pages Found**: Total discovered pages
- **Downloaded**: Successfully saved pages
- **Elapsed Time**: Time since start

### Progress Bar
- Shows percentage complete
- Animated with shimmer effect
- Updates in real-time

### File Browser
- Tree view of downloaded files
- Search functionality
- File size information
- Navigation links

### Error Log
- Shows any issues encountered
- Helps troubleshoot problems
- Lists failed downloads

## 🔧 Troubleshooting

### Common Issues

#### "URL not valid"
- Make sure URL starts with http:// or https://
- Check for typos in the URL
- Ensure the site is accessible

#### "Crawl failed"
- Check internet connection
- Verify the site allows crawling
- Try increasing rate limit
- Check error log for details

#### "Slow downloads"
- Reduce max depth level
- Increase rate limit
- Filter unnecessary file types
- Try during off-peak hours

#### "Missing files"
- Enable all file type filters
- Increase max depth
- Check if files are on different domains

### Performance Tips
- Start with depth 2 for testing
- Use rate limit 1.0+ for stability
- Filter file types to reduce size
- Monitor memory usage for large sites

## 🛠️ Advanced Usage

### Command Line Testing
```bash
# Test with demo script
python3 demo.py

# Run comprehensive tests
python3 test_app.py
```

### API Usage
```python
import requests

# Start crawl
response = requests.post('http://localhost:8001/api/start_crawl', json={
    'url': 'https://docs.example.com/',
    'max_depth': 3,
    'include_images': True
})

crawl_id = response.json()['crawl_id']

# Check status
status = requests.get(f'http://localhost:8001/api/crawl_status/{crawl_id}')

# Download ZIP
zip_file = requests.get(f'http://localhost:8001/api/download_zip/{crawl_id}')
```

### Custom Configuration
Edit `main.py` to change:
- Default port (currently 8001)
- Timeout settings
- User agent string
- Maximum file sizes

## 📁 Output Structure

Downloaded documentation is organized as:
```
downloads/
└── example_com_20260102_043015/
    ├── index.html              # Navigation index
    ├── getting-started.html    # Downloaded pages
    ├── api-reference.html
    ├── css/
    │   └── styles.css
    ├── js/
    │   └── main.js
    └── images/
        └── logo.png
```

## 🎨 Features

### Real-time Monitoring
- Live progress updates
- Current page display
- Error tracking
- Speed metrics

### Smart Organization
- Maintains site structure
- Generates navigation index
- Asset dependency tracking
- Path correction

### Modern Interface
- Dark theme for developers
- Smooth animations
- Responsive design
- Keyboard shortcuts

### Robust Crawling
- Rate limiting
- Error recovery
- Duplicate detection
- URL normalization

## 🌐 Browser Support
- Chrome 88+ (Recommended)
- Firefox 85+
- Safari 14+
- Edge 88+

## 💡 Tips
1. **Test First**: Start with a small site to verify everything works
2. **Be Patient**: Large sites can take several minutes
3. **Monitor Progress**: Watch the status dashboard for issues
4. **Check Results**: Browse downloaded files before creating ZIP
5. **Respect Limits**: Use appropriate rate limits for target sites

## 🚀 Next Steps
1. Try the live demo: https://rixf47dn27al6.ok.kimi.link
2. Test with your favorite documentation site
3. Experiment with different settings
4. Create your first documentation archive
5. Share with your team!

## 📞 Support
- Check the README.md for detailed documentation
- Run tests with `python3 test_app.py`
- Review troubleshooting section above
- Check browser console for errors

---

**Happy Documentation Archiving! 📚✨**