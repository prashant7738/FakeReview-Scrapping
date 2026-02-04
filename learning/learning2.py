from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:

        browser = p.chromium.launch(headless=False)
        
        page = browser.new_page()
        page.goto("https://www.wikipedia.org/")

        page.fill('input[name = "search"]','Web Scrapping')
        page.click('button[class="pure-button pure-button-primary-progressive"]')

        page.wait_for_selector(".mw-parser-output")

        first_p = page.locator(".mw-parser-output p").first
        print(f"Result: \n{first_p.inner_text()}")
        
        
        
        browser.close()

if __name__ == "__main__":
    run()