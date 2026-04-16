from playwright.sync_api import sync_playwright, Page

class BrowserManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(BrowserManager, cls).__new__(cls)
            cls._instance._playwright = None
            cls._instance._browser = None
        return cls._instance

    def start(self, headless: bool = False):
        if self._browser is None:
            self._playwright = sync_playwright().start()
            self._browser = self._playwright.chromium.launch(headless=headless)

    def new_page(self):
        return self._browser.new_page()

    def stop(self):
        if self._browser:
            self._browser.close()
            self._playwright.stop()
            self._browser = None
            BrowserManager._instance = None
