from pages.base_page import BasePage

import re

class SearchHotelResultPage(BasePage):
    PROPERTY_AVAILABLE_TEXT = '[data-element-name="properties-available-text"]'

    def __init__(self, page):
        super().__init__(page)

    def get_property_count(self):
        text = self.page.locator(self.PROPERTY_AVAILABLE_TEXT).text_content()
        match = re.search(r'(\d+)', text)
        return int(match.group()) if match else 0
