from behave import given, when, then
from pages.search_hotel_result_page import SearchHotelResultPage

@then('more than 0 properties are found')
def verify_property_count(context):
    count = context.search_hotel_result_page.get_property_count()
    assert count > 0, f"Property count = {count}"

@when('I select minimum budget to {min_percent} percent and maximum budget percent to {max_percent}')
def set_min_budget(context, min_percent, max_percent):
    context.search_hotel_result_page.set_budget_range(min_percent, max_percent)

@then('the budget slider should be set correctly')
def verify_budget_slider(context):
    min_price = context.search_hotel_result_page.get_min_price()
    max_price = context.search_hotel_result_page.get_max_price()

    assert min_price >= 0, f"Min price = {min_price}"
    assert max_price > min_price, f"Max price = {max_price}"
    print(f"Min price = {min_price}, Max price = {max_price}")

@when('I select "{property_type}" property type')
def select_property_type(context, property_type):
    context.search_hotel_result_page.select_property_type(property_type)

@then('the "{filter_name}" filter should be selected')
def verify_filter_selected(context, filter_name):
    is_check = context.search_hotel_result_page.is_property_checked(filter_name)
    assert is_check, f"Property checked = {is_check}"

@then('the filter count for "{filter_name}" should equal the total property count')
def verify_filter_count(context, filter_name):
    filter_count = context.search_hotel_result_page.get_filter_count_for_property_type(filter_name)
    total_property_count = context.search_hotel_result_page.get_property_count()
    assert filter_count == total_property_count, f"Property count = {filter_count}"

@when('I click on the sort dropdown')
def click_on_sort_dropdown(context):
    context.search_hotel_result_page.click_sort_dropdown()

@then('the sort dropdown should contain the following options:')
def verify_sort_options(context):
    expected_options = [row['option'] for row in context.table]
    actual_options = context.search_hotel_result_page.get_all_sort_options()

    for expected in expected_options:
        assert expected in actual_options, f"Expected option '{expected}' not found in {actual_options}"

@when('I select sort option "{option_name}"')
def select_option(context, option_name):
    context.search_hotel_result_page.select_sort_option(option_name)

@then('the first property should have the lowest price')
def verify_lowest_price_first(context):
    prices = context.search_hotel_result_page.get_all_property_prices()
    assert len(prices) > 0, "No prices found"
    assert prices[0] == min(prices), f"First price {prices[0]} is not the lowest in {prices}"
