# Daraz Review Scraper

A robust web scraping tool using Playwright to extract product reviews from Daraz.com.np. This project is designed for collecting authentic and fake reviews to build machine learning models for **fake review detection**.

## Overview

This scraper automates the collection of product reviews, ratings, and metadata from Daraz product pages. It includes anti-bot detection mechanisms, intelligent pagination handling, and persistent data storage for building comprehensive datasets.

## Features

- 🤖 **Advanced Bot Detection Evasion**
  - Chrome persistent user context to maintain session
  - Navigator property spoofing (webdriver, plugins, languages)
  - Realistic Chromium user agent
  - Non-headless browsing mode
  
- 📊 **Intelligent Data Collection**
  - Extracts review text, dates, and star ratings
  - Parses SVG-based star rating visualizations
  - Robust error handling for incomplete reviews
  
- ⏱️ **Smart Rate Limiting**
  - Random delays (3-7 seconds) between page navigation
  - Prevents IP blocking and server throttling
  - Network idle detection for reliable page loading
  
- 🔄 **Automatic Pagination**
  - Detects and navigates through all review pages
  - Gracefully handles pagination boundaries
  
- 💾 **Persistent Data Storage**
  - Appends data to CSV without overwriting
  - Creates new file on first run
  - Pandas-based data management

## Requirements

- **Python 3.8+**
- **Playwright** - Headless browser automation
- **Pandas** - Data manipulation and CSV handling

## Installation

### Step 1: Clone/Navigate to project
```bash
cd Daraz-Review-Scrapper
```

### Step 2: Install dependencies
```bash
pip install -r requirements.txt
```

Or manually install:
```bash
pip install playwright pandas
playwright install chromium
```

### Step 3: Configure user data directory
Update the `user_data_dir` path in `darazreviewscrapper.py` if needed:
```python
context = p.chromium.launch_persistent_context(
    user_data_dir=r"/path/to/User",  # Update this path
    ...
)
```

## Usage

### Basic Usage
1. **Update the product URL** in `darazreviewscrapper.py`:
   ```python
   url = "https://www.daraz.com.np/products/your-product-url-here"
   ```

2. **Run the scraper**:
   ```bash
   python darazreviewscrapper.py
   ```

3. **View results**: Check the generated CSV file (e.g., `darazlaptopstandreviews.csv`)

### Output Format

The scraper generates a CSV file with the following columns:

| Column | Description | Example |
|--------|-------------|---------|
| `review` | Full review text | "Great product, highly recommend!" |
| `review_date` | Date review was posted | "2 Feb 2024" |
| `review_star` | Star rating (1-5) | 5 |

## Project Structure

```
Daraz-Review-Scrapper/
├── darazreviewscrapper.py    # Main scraper script
├── darazreviewdataset.csv    # Output data (CSV)
├── requirements.txt          # Python dependencies
├── README.md                 # This file
└── learning/                 # Learning/exploration scripts
    ├── learning1.py
    ├── learning2.py
    ├── main.py
    └── darazreviews.csv
```

## How It Works

1. **Launches a Chrome browser** with persistent user context for session management
2. **Injects anti-detection scripts** to bypass Daraz bot protection
3. **Navigates to the product page** and waits for reviews to load
4. **Extracts review data** from each visible review element:
   - Review text from `.content` selector
   - Date from `.top .title.right` selector
   - Star rating by counting filled SVG paths
5. **Handles pagination** by detecting and clicking the next button
6. **Applies random delays** (3-7 seconds) between page navigation
7. **Appends data to CSV** file, preserving previous runs

## Key Technical Details

### Star Rating Detection
Uses SVG path selectors to count filled stars:
```python
filled_stars = data.locator('.i-rate-star .i-rate-star-item svg path[style*="fill: rgb(255, 200, 60);"]').count()
```

### Bot Detection Evasion
Injects JavaScript to spoof navigator properties:
```javascript
Object.defineProperty(navigator,'webdriver',{get:() => undefined});
window.chrome = {runtime:{}};
```

### Error Resilience
- Continues scraping if individual reviews fail to parse
- Gracefully handles missing next button (end of pagination)
- Saves collected data even if scraping is interrupted

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "User data directory not found" | Update the `user_data_dir` path in the script |
| Reviews not loading | Increase `page.wait_for_selector()` timeout or check URL validity |
| Slow scraping | Check your internet connection; random delays are intentional |
| CSV file errors | Ensure the output directory is writable |
| Daraz blocking requests | The bot detection evasion may have become outdated; check Daraz website for changes |

## Important Notes

⚠️ **Ethical Considerations:**
- Use scraped data responsibly and in compliance with Daraz's Terms of Service
- Consider the legal implications of web scraping in your jurisdiction
- Respect rate limiting and server resources

## Future Improvements

- [ ] Multi-product batch scraping
- [ ] Proxy rotation support
- [ ] Database storage (SQLite/MongoDB)
- [ ] Scheduled scraping with cron jobs
- [ ] Review sentiment analysis integration
- [ ] Real-time data validation

## License

This project is for educational and research purposes.
