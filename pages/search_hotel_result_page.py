import re
from pages.base_page import BasePage

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
    SORT_DROPDOWN = 'button[data-react-aria-pressable="true"][aria-haspopup="true"]'
    SORT_OPTION = 'role=option'
    PROPERTY_PRICE = '[data-element-name="final-price"] [data-selenium="display-price"]'

    def __init__(self, page):
        super().__init__(page)

    def get_property_count(self):
        text = self.page.locator(self.PROPERTY_AVAILABLE_TEXT).text_content()
        match = re.search(r'(\d+)', text)
        return int(match.group()) if match else 0

    def _drag_slider_handle(self, handle_locator, target_x, target_y):
        handle_box = handle_locator.bounding_box()
        center_x = handle_box['x'] + handle_box['width'] / 2
        center_y = handle_box['y'] + handle_box['height'] / 2

        self.page.mouse.move(center_x, center_y)
        self.page.mouse.down()
        self.page.mouse.move(target_x, target_y, steps=10)
        self.page.mouse.up()

    def set_budget_range(self, min_percent, max_percent):
        slider = self.page.locator(self.SLIDER_CONTAINER).first
        box = slider.bounding_box()

        min_target_x = box['x'] + (box['width'] * float(min_percent) / 100)
        max_target_x = box['x'] + (box['width'] * float(max_percent) / 100)
        center_y = box['y'] + (box['height'] / 2)

        min_handle = self.page.locator(self.MIN_HANDLE).first
        max_handle = self.page.locator(self.MAX_HANDLE).first

        self._drag_slider_handle(min_handle, min_target_x, center_y)
        self._drag_slider_handle(max_handle, max_target_x, center_y)

    def _parse_price_value(self, locator):
        value = locator.input_value()
        return int(value.replace(',', ''))

    def get_min_price(self):
        return self._parse_price_value(self.page.locator(self.MIN_PRICE).last)

    def get_max_price(self):
        return self._parse_price_value(self.page.locator(self.MAX_PRICE).last)

    def select_property_type(self, property_type):
        checkbox = self.page.get_by_role('checkbox', name=property_type).first
        checkbox.click()
        checkbox.wait_for(state='attached', timeout=5000)

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
            except Exception:
                continue

        return None

    def click_sort_dropdown(self):
        dropdown = self.page.locator(self.SORT_DROPDOWN)
        dropdown.click()
        self.page.get_by_role('option').first.wait_for(state='visible', timeout=5000)

    def select_sort_option(self, option_name):
        self.click_sort_dropdown()
        option = self.page.locator(self.SORT_OPTION).filter(has_text=option_name)
        option.click()
        option.wait_for(state='detached', timeout=5000)
        self.page.wait_for_load_state('networkidle', timeout=10000)

    def get_current_sort_option(self):
        return self.page.locator(self.SORT_OPTION).text_content()

    def get_all_sort_options(self):
        options = self.page.get_by_role('option').all_text_contents()
        self.page.keyboard.press('Escape')
        return options

    def get_all_property_prices(self):
        self.page.locator(self.PROPERTY_PRICE).first.wait_for(state='visible', timeout=10000)
        price_elements = self.page.locator(self.PROPERTY_PRICE).all()
        prices = []

        for price_element in price_elements[:10]:
            try:
                text = price_element.text_content()
                match = re.search(r'[\d,]+', text)
                if match:
                    price_str = match.group().replace(',', '')
                    prices.append(int(price_str))
            except Exception:
                continue

        return prices