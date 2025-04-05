import time
from datetime import timedelta, date

import requests

from models import ActivitiesResponse, CourtDuration

# TODO: Move this to a config file
BADMINTON_COURT_ENDPOINT = 'https://better-admin.org.uk/api/activities/venue/sugden-sports-centre/activity/{}/times'

HEADERS = {
    'Accept': 'application/json',
    'Origin': 'https://bookings.better.org.uk',
    'Referer': 'https://bookings.better.org.uk/',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0.1 Safari/605.1.15',
}

DATE_FORMAT = "%Y-%m-%d"

def get_available_courts(duration: CourtDuration, date: str) -> str:
    response = requests.get(BADMINTON_COURT_ENDPOINT.format(duration), params={'date': date}, headers=HEADERS)

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
        # TODO: Get correct hyperlink
        print(f'Checking date: {current_date.strftime(DATE_FORMAT)} ({current_date.strftime('%A')})')
        all_available_courts = get_all_available_courts(current_date.strftime(DATE_FORMAT))
        print(all_available_courts)
        print()
        # Wait for 2 seconds so we don't get banned
        time.sleep(2)
        current_date += timedelta(days=1)

if __name__ == '__main__':
    main()