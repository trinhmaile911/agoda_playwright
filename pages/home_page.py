from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from pages.base_page import BasePage

class HomePage(BasePage):
    URL              = 'https://www.agoda.com'
    SEARCH_INPUT     = '#textInput'
    FIRST_SUGGESTION = '[data-testid="autosuggest-item"][data-element-index="0"]'
    CHECK_IN_BOX     = '[data-element-name="check-in-box"]'
    SEARCH_BTN = '[data-element-name="search-button"]'
    DATE_ATTRIBUTE   = 'data-selenium-date'
    NEXT_MONTH_BTN   = '[data-selenium="calendar-next-month-button"]'
    ADD_ROOM_BTN = '[data-element-name="occupancy-selector-panel-rooms"][data-selenium="plus"]'
    ADD_ADULT_BTN = '[data-element-name="occupancy-selector-panel-adult"][data-selenium="plus"]'
    ADD_CHILD_BTN = '[data-element-name="occupancy-selector-panel-children"][data-selenium="plus"]'
    REMOVE_ROOM_BTN = '[data-element-name="occupancy-selector-panel-rooms"][data-selenium="minus"]'
    REMOVE_ADULT_BTN = '[data-element-name="occupancy-selector-panel-adult"][data-selenium="minus"]'
    REMOVE_CHILD_BTN = '[data-element-name="occupancy-selector-panel-children"][data-selenium="minus"]'
    ROOM_COUNT = '[data-selenium="desktop-occ-room-value"] p'
    ADULT_COUNT = '[data-selenium="desktop-occ-adult-value"] p'
    CHILD_COUNT = '[data-selenium="desktop-occ-children-value"] p'

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

    def set_rooms(self, room: int):
        current = int(self.page.locator(self.ROOM_COUNT).text_content().strip())

        while current < room:
            self.page.locator(self.ADD_ROOM_BTN).click()
            self.page.wait_for_timeout(500)
            current += 1

        while current > room:
            self.page.locator(self.REMOVE_ROOM_BTN).click()
            self.page.wait_for_timeout(500)
            current -= 1

    def set_adults(self, adult: int):
        current = int(self.page.locator(self.ADULT_COUNT).text_content().strip())

        while current < adult:
            self.page.locator(self.ADD_ADULT_BTN).click()
            self.page.wait_for_timeout(500)
            current += 1

        while current > adult:
            self.page.locator(self.REMOVE_ADULT_BTN).click()
            self.page.wait_for_timeout(500)
            current -= 1

    def set_children(self, children: int):
        current = int(self.page.locator(self.CHILD_COUNT).text_content().strip())

        while current < children:
            self.page.locator(self.ADD_CHILD_BTN).click()
            self.page.wait_for_timeout(500)
            current += 1

        while current > children:
            self.page.locator(self.REMOVE_CHILD_BTN).click()
            self.page.wait_for_timeout(500)
            current -= 1

    def click_search_button(self):
        with self.page.expect_popup() as popup_info:
            self.page.locator(self.SEARCH_BTN).click()
        new_page = popup_info.value
        new_page.wait_for_load_state("networkidle")
        return new_page