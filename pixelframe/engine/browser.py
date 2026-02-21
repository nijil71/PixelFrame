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

    def new_page(
        self, width: int, height: int, 
        device_scale_factor: float = 1.0, 
        is_mobile: bool = False, 
        has_touch: bool = False, 
        user_agent: str = None
    ):
        options = {
            "viewport": {"width": width, "height": height},
            "device_scale_factor": device_scale_factor,
            "is_mobile": is_mobile,
            "has_touch": has_touch,
        }
        if user_agent:
            options["user_agent"] = user_agent
        return self.browser.new_page(**options)