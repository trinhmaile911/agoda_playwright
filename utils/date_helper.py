from datetime import datetime, timedelta

def get_future_date(days_from_now):
    date = datetime.today() + timedelta(days=days_from_now)
    return date.strftime('%Y-%m-%d')