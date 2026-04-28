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
