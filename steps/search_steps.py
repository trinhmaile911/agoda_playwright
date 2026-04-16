from behave import given, when, then
from pages.home_page import HomePage

@given('I navigate to Agoda home page')
def navigate_to_agoda_home_page(context):
    context.home_page = HomePage(context.page)
    context.home_page.open()

@when('I search for "{destination}" as destination')
def search_for_hotel(context, destination: str):
    context.home_page.search_hotel(destination)