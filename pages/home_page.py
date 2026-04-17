from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from pages.base_page import BasePage

class HomePage(BasePage):
    URL              = 'https://www.agoda.com'
    SEARCH_INPUT     = '#textInput'
    FIRST_SUGGESTION = '[data-testid="autosuggest-item"][data-element-index="0"]'
    CHECK_IN_BOX     = '[data-element-name="check-in-box"]'
    DATE_ATTRIBUTE   = 'data-selenium-date'
    NEXT_MONTH_BTN   = '[data-selenium="calendar-next-month-button"]'

    def __init__(self, page):
        super().__init__(page)

    def open(self):
        self.goto(self.URL)

    def search_destination(self, destination: str):
        self.page.locator(self.SEARCH_INPUT).fill(destination)
        self.page.locator(self.FIRST_SUGGESTION).wait_for(state="visible")
        self.page.locator(self.FIRST_SUGGESTION).click()

    def _navigate_to_month(self, date: str, max_clicks: int = 12):
        for _ in range(max_clicks):
            if self.page.locator(f'[{self.DATE_ATTRIBUTE}="{date}"]').is_visible():
                return
            self.page.locator(self.NEXT_MONTH_BTN).wait_for(state="visible")
            self.page.evaluate(
                "(selector) => document.querySelector(selector).click()",
                self.NEXT_MONTH_BTN 
            )
            self.page.wait_for_timeout(500)
        raise Exception(f'Date not found after {max_clicks} clicks')

    def select_date(self, date: str):
        self._navigate_to_month(date)
        self.page.locator(f'[{self.DATE_ATTRIBUTE}="{date}"]').click()