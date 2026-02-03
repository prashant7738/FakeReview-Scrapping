import csv
from datetime import datetime
from playwright.sync_api import sync_playwright

PRODUCT_URL = ""  # Step 1: paste a full Amazon product URL here.
MAX_PAGES = 5     # Step 5: limit pages while testing; increase later.
OUTPUT_CSV = "amazon_reviews.csv"


def safe_text(locator) -> str:
    return locator.first.inner_text().strip() if locator.count() > 0 else ""


with sync_playwright() as p:
    context = p.chromium.launch_persistent_context(
        user_data_dir=r"/home/prashant/Coding/Projects/FakeReviewScrapping/User",
        channel="chrome",
        no_viewport=True,
        headless=False,
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6422.112 Safari/537.36",
        locale="en-US",
        args=["--start-maximized"]
    )

    context.add_init_script("""
        Object.defineProperty(navigator,'webdriver',{get:() => undefined});
        window.chrome = {runtime:{}};
        Object.defineProperty(navigator,'plugins',{get:() => [1,2,3,4,5]});
        Object.defineProperty(navigator,'languages',{get:() => ['en-US','en']});
    """)

    page = context.new_page()

    if not PRODUCT_URL:
        raise ValueError("Set PRODUCT_URL to a valid Amazon product URL before running.")

    # Step 2: open product page.
    page.goto(PRODUCT_URL, wait_until="domcontentloaded", timeout=60000)

    # Step 3: open the "See all reviews" page.
    see_all = page.locator("a[data-hook='see-all-reviews-link-foot']")
    if see_all.count() == 0:
        see_all = page.locator("a[data-hook='see-all-reviews-link-foot'] , a[data-hook='see-all-reviews-link']")
    see_all.first.click()
    page.wait_for_load_state("domcontentloaded")

    # Step 4: scrape review cards + paginate.
    rows = []
    page_num = 1
    while page_num <= MAX_PAGES:
        page.wait_for_selector("div[data-hook='review']", timeout=60000)
        cards = page.locator("div[data-hook='review']")
        for i in range(cards.count()):
            card = cards.nth(i)
            rows.append({
                "product_url": PRODUCT_URL,
                "page": page_num,
                "title": safe_text(card.locator("span[data-hook='review-title']")),
                "rating": safe_text(card.locator("i[data-hook='review-star-rating'] span")),
                "body": safe_text(card.locator("span[data-hook='review-body']")),
                "date": safe_text(card.locator("span[data-hook='review-date']")),
                "verified": safe_text(card.locator("span[data-hook='avp-badge']")),
                "author": safe_text(card.locator("span.a-profile-name")),
                "scraped_at": datetime.utcnow().isoformat()
            })

        next_btn = page.locator("li.a-last a")
        if next_btn.count() == 0 or not next_btn.first.is_enabled():
            break
        next_btn.first.click()
        page.wait_for_load_state("domcontentloaded")
        page_num += 1

    # Step 6: save to CSV.
    if rows:
        with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)

    context.close()