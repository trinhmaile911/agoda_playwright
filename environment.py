from browser_manager import BrowserManager
import os

def before_all(context):
    os.makedirs("screenshots", exist_ok=True)
    context.bm = BrowserManager()
    context.bm.start(headless = False)

def before_scenario(context, scenario):
    context.page = context.bm.new_page()

def after_scenario(context, scenario):
    if scenario.status == "failed":
        try:
            ts = datetime.now().strftime("%Y%m%d-%H%M%S")
            safe_name = scenario.name.replace(" ", "_")
            context.page.screenshot(path=f"screenshots/{safe_name}_{ts}.png")
        except Exception:
            pass
    context.page.close()

def after_all(context):
    context.bm.stop()