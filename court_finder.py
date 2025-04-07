import requests
import time

from typing import List
from config import BETTER_ENDPOINT, HEADERS, VENUES
from models import ActivitiesResponse, BadmintonCourt, Activity

class CourtFinder:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(HEADERS)

    def get_all_available_badminton_courts_for_date(self, date: str):
        for slug, display_name in VENUES.items():
            courts = []
            courts.extend(self.get_available_courts(slug, Activity.BADMINTON_FORTY_MINUTES, date))
            courts.extend(self.get_available_courts(slug, Activity.BADMINTON_SIXTY_MINUTES, date))
            print(f'[{display_name}]')

            if courts:
                print('\n'.join(map(str, courts)))
            else:
                print('No courts available')

            time.sleep(1)

    def get_available_courts(self, venue: str, activity: Activity, date: str) -> ActivitiesResponse:
        response = self.session.get(BETTER_ENDPOINT.format(venue, activity), params={'date': date})

        if response.ok:
            data = response.json()
            return ActivitiesResponse.model_validate(data).available_courts()
        else:
            # TODO: Better error handling
            print(response.text)
