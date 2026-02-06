# Daraz Review Scraper

Web scraping tool using Playwright to extract product reviews from Daraz.com.np for the **Fake Review Detection** dataset project.

## Features

- 🤖 **Bot Detection Evasion**: Anti-detection mechanisms to bypass Daraz bot detection
- 📊 **Automatic Data Storage**: Appends scraped reviews to CSV file
- ⏱️ **Rate Limiting**: Random delays between requests to avoid IP blocking
- 🔄 **Pagination Support**: Automatically navigates through all review pages
- 📅 **Timestamp Tracking**: Records scrape date for each review

## Requirements

- Python 3.8+
- Playwright
- Pandas

## Installation

```bash
pip install playwright pandas
playwright install chromium
```

## Usage

1. Update the product URL in `darazreviewscrapper.py`
2. Run the scraper:
```bash
python darazreviewscrapper.py
```
3. Reviews will be saved to `darazreviewdataset.csv`

## Output Format

|review|review_date|review_star
|--------|--------------|--------|
| Review text | 2 Feb 2024 | 5.0 |

## Notes

- First run creates `darazreviews.csv`
- Subsequent runs append new reviews
- Random delays (3-7 seconds) between page navigation
- Headless mode disabled to prevent detection

## Project Purpose

Collecting authentic and fake reviews from Daraz for machine learning model training to detect fraudulent reviews.
