from datetime import date

def get_day_of_week(date: date) -> str:
    return date.strftime('%A')
