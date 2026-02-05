from playwright.sync_api import sync_playwright
import pandas as pd
from datetime import datetime
import time
import random

with sync_playwright() as p:
    context = p.chromium.launch_persistent_context(
        user_data_dir=r"/home/prashant/Coding/Projects/FakeReviewScrapping/User",
        channel="chrome",
        no_viewport=True,
        headless=False,
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6422.112 Safari/537.36",
        locale="en-US",
        args=["--start-maximized"],
        proxy=None  # Add proxy support if needed
    )

    context.add_init_script("""
        Object.defineProperty(navigator,'webdriver',{get:() => undefined});
        window.chrome = {runtime:{}};
        Object.defineProperty(navigator,'plugins',{get:() => [1,2,3,4,5]});
        Object.defineProperty(navigator,'languages',{get:() => ['en-US','en']});
    """)

    page = context.new_page()
    page.goto("https://www.daraz.com.np/products/x-age-conve-up-beat-w1-wired-headphone-xwh01-ergonomic-design-comfortable-headphone-i127967479-s1034997798.html?c=&channelLpJumpArgs=&clickTrackInfo=query%253Aheadphone%253Bnid%253A127967479%253Bsrc%253ALazadaMainSrp%253Brn%253A034178512d1ccfd3db16f6c13ed1dcc5%253Bregion%253Anp%253Bsku%253A127967479_NP%253Bprice%253A904%253Bclient%253Adesktop%253Bsupplier_id%253A900158184147%253Bbiz_source%253Ahttps%253A%252F%252Fwww.daraz.com.np%252F%253Bslot%253A1%253Butlog_bucket_id%253A470687%253Basc_category_id%253A157%253Bitem_id%253A127967479%253Bsku_id%253A1034997798%253Bshop_id%253A99481%253BtemplateInfo%253A&freeshipping=0&fs_ab=1&fuse_fs=&lang=en&location=Bagmati%20Province&price=904&priceCompare=skuId%3A1034997798%3Bsource%3Alazada-search-voucher%3Bsn%3A034178512d1ccfd3db16f6c13ed1dcc5%3BoriginPrice%3A90400%3BdisplayPrice%3A90400%3BsinglePromotionId%3A50000034846001%3BsingleToolCode%3ApromPrice%3BvoucherPricePlugin%3A0%3Btimestamp%3A1770302656060&ratingscore=4.251428571428572&request_id=034178512d1ccfd3db16f6c13ed1dcc5&review=700&sale=1828&search=1&source=search&spm=a2a0e.searchlist.list.1&stock=1")

    reviews_data = []

    while True:
        # Fetch reviews on current page
        datas = page.locator(".item-content .content").all()
        
        for data in datas:
            try:
                review_text = data.inner_text()
                reviews_data.append({"review": review_text, "scrapped_date": datetime.now()})
                print(review_text)
            except Exception as e:
                print(f'error in this line due to {e}')
        
        # Check if next button exists and is enabled
        next_button = page.locator("#module_product_review .next-pagination-item.next")
        if next_button.count() == 0:
            break
        
        # Add random delay between 3-7 seconds
        delay = random.uniform(3, 7)
        print(f"Waiting {delay:.2f} seconds before next page...")
        time.sleep(delay)
        
        # Click next and wait for new content
        next_button.click()
        page.wait_for_load_state("networkidle")  # Wait for page to load
    
    # Save data to CSV
    if reviews_data:
        df = pd.DataFrame(reviews_data)
        csv_filename = 'darazreviews.csv'
        
        try:
            existing_df = pd.read_csv(csv_filename)
            df = pd.concat([existing_df, df], ignore_index=True)
        except FileNotFoundError:
            pass
        
        df.to_csv(csv_filename, index=False)
        print(f"Total reviews scraped: {len(reviews_data)}")
    
    context.close()