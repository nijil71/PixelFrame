from playwright.sync_api import sync_playwright

class BrowserManager:
    def __init__(self):
        self.playwright = None
        self.browser = None

    def start(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=True)

    def stop(self):
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()

    def new_page(self, width: int, height: int):
        return self.browser.new_page(
            viewport={"width": width, "height": height}
        )