import time
from behave import given, when, then
from pages.home_page import HomePage
from utils.date_helper import get_future_date

@given('I navigate to Agoda home page')
def navigate_to_agoda_home_page(context):
    context.home_page = HomePage(context.page)
    context.home_page.open()

@when('I search for "{destination}" as destination')
def search_for_hotel(context, destination: str):
    context.home_page.search_destination(destination)

@when('I select check-in date {days:d} days from now')
def select_check_in_date(context, days: int):
    date = get_future_date(days)
    context.home_page.select_date(date)

@when('I select check-out date {days:d} days from now')
def select_check_in_date(context, days: int):
    date = get_future_date(days)
    context.home_page.select_date(date)

@when('I set rooms to {rooms:d}')
def set_room(context, rooms: int):
    context.home_page.set_rooms(rooms)

@when('I set adults to {adults:d}')
def set_adults(context, adults: int):
    context.home_page.set_adults(adults)

@when('I set children to {children:d}')
def set_children(context, children: int):
    context.home_page.set_children(children)

@when('I click on the search button')
def click_search_button(context):
    context.home_page.click_search_button()