import time
import requests

from datetime import timedelta, date
from config import BETTER_ENDPOINT, HEADERS
from models import ActivitiesResponse, CourtDuration
from utils import get_day_of_week

def get_available_courts(duration: CourtDuration, date: str) -> str:
    response = requests.get(BETTER_ENDPOINT.format(duration), params={'date': date}, headers=HEADERS)

    if response.ok:
        data = response.json()
        if data:
            activities_response = ActivitiesResponse.model_validate(data)
            return '\n'.join(activities_response.formatted())
        else:
            return ''
    else:
        # TODO: Better error handling
        print(response.text)

def get_all_available_courts(date: str) -> str:
    all_available_courts = ''
    for duration in CourtDuration:
        available_courts = get_available_courts(duration, date)
        all_available_courts += available_courts

    return all_available_courts if all_available_courts else 'No available courts'

def main():
    current_date = date.today()

    # Check the next 6 days
    for i in range(6):
        print(f'Checking date: {current_date} ({get_day_of_week(current_date)})')
        all_available_courts = get_all_available_courts(current_date)
        print(all_available_courts)
        print()
        # Wait for 2 seconds so we don't get banned
        time.sleep(2)
        current_date += timedelta(days=1)

if __name__ == '__main__':
    main()
