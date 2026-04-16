from browser_manager import BrowserManager
import os

def before_all(context):
    context.bm = BrowserManager()
    context.bm.start(headless = False)

def before_scenario(context, scenario):
    context.page = context.bm.new_page()

def after_scenario(context, scenario):
    context.page.close()

def after_all(context):
    context.bm.stop()