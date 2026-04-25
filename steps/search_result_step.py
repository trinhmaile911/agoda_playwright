from behave import given, when, then
from pages.search_hotel_result_page import SearchHotelResultPage

@then('more than 0 properties are found')
def verify_property_count(context):
    count = context.search_hotel_result_page.get_property_count()
    assert count > 0, f"Property count = {count}"