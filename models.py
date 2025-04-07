from pydantic import BaseModel
from typing import List, Dict, Union
from enum import Enum

class Time(BaseModel):
    format_24_hour: str

class Price(BaseModel):
    formatted_amount: str

# TODO: Check if this format is the same for all activities. If so make this a generic base class
class BadmintonCourt(BaseModel):
    starts_at: Time
    ends_at: Time
    duration: str
    price: Price
    spaces: int

    def is_available(self) -> bool:
        return self.spaces > 0

    def __str__(self):
        return f'Court at {self.starts_at.format_24_hour} - {self.ends_at.format_24_hour} ({self.duration}) | Price: {self.price.formatted_amount} | Spaces: {self.spaces}'

class ActivitiesResponse(BaseModel):
    """
    The response can be in two forms:
    {
        "data": {
            "3": {
                <Details>
            }
        },
        ...
    }

    or

    "data": [
        {
            <court details>
        },
        ...
    ]
    """
    data: Union[Dict[str, BadmintonCourt], List[BadmintonCourt]]

    def available_courts(self) -> List[BadmintonCourt]:
        return (
            [court for court in self.data if court.is_available()]
            if isinstance(self.data, list)
            else [court for court in self.data.values() if court.is_available()]
        )

# TODO: Does this need to exist?
class Activity(Enum):
    BADMINTON_FORTY_MINUTES = 'badminton-40min'
    BADMINTON_SIXTY_MINUTES = 'badminton-60min'

    def __str__(self):
        return self.value