import requests

from typing import List
from config import BETTER_ENDPOINT, HEADERS
from models import ActivitiesResponse, BadmintonCourt, Activity

class CourtFinder:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(HEADERS)

    def get_all_available_badminton_courts(self, date: str) -> List[BadmintonCourt]:
        forty_minute_courts = self.get_available_courts(Activity.BADMINTON_FORTY_MINUTES, date)
        sixty_minute_courts = self.get_available_courts(Activity.BADMINTON_SIXTY_MINUTES, date)
        return forty_minute_courts + sixty_minute_courts

    def get_available_courts(self, activity: Activity, date: str) -> ActivitiesResponse:
        response = self.session.get(BETTER_ENDPOINT.format(activity), params={'date': date})

        if response.ok:
            data = response.json()
            return ActivitiesResponse.model_validate(data).available_courts()
        else:
            # TODO: Better error handling
            print(response.text)
