from playwright.sync_api import sync_playwright

def run():
    # 'with' statement handles the cleanup/closing automatically
    with sync_playwright() as p:
        # Launch browser - headless=False so we can see the magic
        browser = p.chromium.launch(headless=False)
        
        page = browser.new_page()
        page.goto("https://news.ycombinator.com")

        
        # first_headline =  page.locator(".titleline > a").first
        # print(f"The top story is : {first_headline.inner_text()}")

        # link = first_headline.get_attribute('href')
        # print(f'The link is : {link}')

        headlines = page.locator(".titleline > a").all()
        print(f'the length of headlines list is {len(headlines)}')

        for i, item in enumerate(headlines, start = 1):
            text = item.inner_text()
            link = item.get_attribute('href')
            print(f'{i}: {text} ')


    
        
        browser.close()

if __name__ == "__main__":
    run()