from browser_manager import BrowserManager
from pages.base_page import BasePage

class HomePage(BasePage):
    URL = 'https://www.agoda.com'
    SEARCH_INPUT = '[data-selenium="icon-box-child"]'
    def __init__(self, page):
        super().__init__(page)

    def open(self):
        self.goto(self.URL)

    def search_hotel(self, destination: str):
        self.page.locator(self.SEARCH_INPUT).fill(destination)