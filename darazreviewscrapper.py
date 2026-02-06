from playwright.sync_api import sync_playwright
import pandas as pd
from datetime import datetime
import time
import random

url = "https://www.daraz.com.np/products/stainless-steel-cordless-electric-jug-18-ltr-1500-watts-i502504267-s2250144682.html?pvid=b154de8a-7dd4-455a-88d9-1cfa01dc25be&search=jfy&scm=1007.51705.413671.0&spm=a2a0e.tm80335409.just4u.d_502504267"
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
        page.goto(url=url)
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