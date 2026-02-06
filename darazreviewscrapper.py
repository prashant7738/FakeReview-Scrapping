from playwright.sync_api import sync_playwright
import pandas as pd
from datetime import datetime
import time
import random

def get_star(data):
    # More specific: count filled star paths within the rating structure
    filled_stars = data.locator('.i-rate-star .i-rate-star-item svg path[style*="fill: rgb(255, 200, 60);"]').count()
    return filled_stars

def daraz_scrapper():

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
        page.goto("https://www.daraz.com.np/products/aluminium-alloy-metal-adjustable-laptop-stand-for-10-to-17-inches-mackbooklaptopstab-i105711486-s2280473603.html?c=&channelLpJumpArgs=&clickTrackInfo=query%253Alaptop%252Bstand%253Bnid%253A105711486%253Bsrc%253ALazadaMainSrp%253Brn%253A8a8454919c1f5ac0e342432a064b4bb5%253Bregion%253Anp%253Bsku%253A105711486_NP%253Bprice%253A499%253Bclient%253Amobile%253Bsupplier_id%253A900152409121%253Bsession_id%253A%253Bbiz_source%253Ah5_external%253Bslot%253A1%253Butlog_bucket_id%253A470687%253Basc_category_id%253A99%253Bitem_id%253A105711486%253Bsku_id%253A2280473603%253Bshop_id%253A47403%253BtemplateInfo%253A&freeshipping=0&fs_ab=1&fuse_fs=&lang=en&location=Bagmati%20Province&price=499&priceCompare=skuId%3A2280473603%3Bsource%3Alazada-search-voucher%3Bsn%3A8a8454919c1f5ac0e342432a064b4bb5%3BunionTrace%3A2102eca017703729339531727e8714%3BoriginPrice%3A49900%3BsubsidyPrice%3A49900%3BshopPrice%3A49900%3BvoucherPrice%3A49900%3BdisplayPrice%3A49900%3BsinglePromotionId%3A50000034846001%3BsingleToolCode%3ApromPrice%3BvoucherPricePlugin%3A1%3BbuyerId%3A0%3BnewBuyer%3Afalse%3Btimestamp%3A1770372934173%3BisPreHeat%3Afalse%3BitemType%3A0&ratingscore=4.456768558951965&request_id=8a8454919c1f5ac0e342432a064b4bb5&review=1145&sale=5056&search=1&source=search&spm=a2a0e.searchlist.list.1&stock=1")

        reviews_data = []

        try:
            page.wait_for_selector(".item", timeout=10000)
            while True:
                # Fetch reviews on current page
                datas = page.locator(".item").all()
                
                for data in datas:
                    try:
                        review_text = data.locator(".content").first.inner_text()
                        review_date = data.locator(".top .title.right").inner_text()
                        review_star = get_star(data.locator(".i-rate"))
                    
                        reviews_data.append({"review": review_text, "review_date": review_date, "review_star": review_star})
                        print(review_text)
                    except Exception as e:
                        print(f'error in this line due to {e}')
                
                #Check if next button exists and is enabled
                next_button = page.locator("#module_product_review .next-pagination-item.next")
                if next_button.count() == 0:
                    break
                
                # Add random delay between 3-7 seconds
                delay = random.uniform(3, 7)
                print(f"Waiting {delay:.2f} seconds before next page...")
                time.sleep(delay)
                
                # Click next and wait for new content
                try:
                    next_button.click(timeout=5000)
                except Exception as e:
                    print(f"Could not click next button: {e}")
                    break
                page.wait_for_load_state("networkidle")  # Wait for page to load

        except Exception as e:
            print(f"Scraping interrupted: {e}")
        
        finally:
            # Save data to CSV (runs whether scraping succeeds or fails)
            if reviews_data:
                df = pd.DataFrame(reviews_data)
                csv_filename = 'darazlaptopstandreviews.csv'
                
                try:
                    existing_df = pd.read_csv(csv_filename)
                    df = pd.concat([existing_df, df], ignore_index=True)
                except FileNotFoundError:
                    pass
                
                df.to_csv(csv_filename, index=False)
                print(f"Total reviews scraped: {len(reviews_data)}")

            context.close()

daraz_scrapper()