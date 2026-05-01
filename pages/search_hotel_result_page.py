from pages.base_page import BasePage

import re

class SearchHotelResultPage(BasePage):
    PROPERTY_AVAILABLE_TEXT = '[data-element-name="properties-available-text"]'
    SLIDER_CONTAINER = '.rc-slider.rc-slider-horizontal'
    MIN_PRICE_INPUT = 'input[data-element-name="search-filter-price"][data-min-price]'
    MAX_PRICE_INPUT = 'input[data-element-name="search-filter-price"][data-max-price]'
    MIN_HANDLE = '.rc-slider-handle.rc-slider-handle-1'
    MAX_HANDLE = '.rc-slider-handle.rc-slider-handle-2'
    MIN_PRICE = 'input#price_box_0'
    MAX_PRICE = 'input#price_box_1'
    FILTER_ITEM_TEXT = '[data-selenium="filter-item-text"]'
    FILTER_COUNT = '[data-selenium="filter-count"]'

    def __init__(self, page):
        super().__init__(page)

    def get_property_count(self):
        text = self.page.locator(self.PROPERTY_AVAILABLE_TEXT).text_content()
        match = re.search(r'(\d+)', text)
        return int(match.group()) if match else 0

    def set_budget_range(self, min_percent, max_percent):
        slider = self.page.locator(self.SLIDER_CONTAINER).first
        box = slider.bounding_box()

        min_target = box['x'] + (box['width'] * float(min_percent)/100)
        max_target = box['x'] + (box['width'] * float(max_percent)/100)
        center_y = box['y'] + (box['height']/2)

        min_handle = self.page.locator(self.MIN_HANDLE).first
        min_box = min_handle.bounding_box()
        max_handle = self.page.locator(self.MAX_HANDLE).first
        max_box = max_handle.bounding_box()

        self.page.mouse.move(min_box['x'] + min_box['width']/2, min_box['y'] + min_box['height']/2)
        self.page.mouse.down()
        self.page.mouse.move(min_target, center_y, steps = 10)
        self.page.mouse.up()

        self.page.mouse.move(max_box['x'] + max_box['width']/2, max_box['y'] + max_box['height']/2)
        self.page.mouse.down()
        self.page.mouse.move(max_target, center_y, steps = 10)
        self.page.mouse.up()

    def get_min_price(self):
        value = self.page.locator(self.MIN_PRICE).last.input_value()
        return int(value.replace(',',''))

    def get_max_price(self):
        value = self.page.locator(self.MAX_PRICE).last.input_value()
        return int(value.replace(',',''))

    def select_property_type(self, property_type):
        self.page.get_by_text(property_type, exact=True).click()
        self.page.wait_for_load_state('networkidle')

    def is_property_checked(self, property_type):
        checkbox = self.page.get_by_role('checkbox', name=property_type).first
        return checkbox.is_checked()

    def get_filter_count_for_property_type(self, property_type):
        all_filters = self.page.locator(f'{self.FILTER_ITEM_TEXT}:text-is("{property_type}")')

        for i in range(all_filters.count()):
            try:
                filter_elem = all_filters.nth(i)
                parent_text = filter_elem.locator('..').text_content()
                match = re.search(r'(\d+)', parent_text)
                if match:
                    return int(match.group(1).replace(',', ''))
            except:
                continue