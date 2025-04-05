from pydantic import BaseModel
from typing import List, Dict, Union
from enum import Enum

class Time(BaseModel):
    format_24_hour: str

class Price(BaseModel):
    formatted_amount: str

class BadmintonCourt(BaseModel):
    starts_at: Time
    ends_at: Time
    duration: str
    price: Price
    spaces: int

    def is_available(self) -> bool:
        return self.spaces > 0

    def formatted(self) -> str:
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

    def formatted(self) -> List[str]:
        return [court.formatted() for court in self.data if court.is_available()] if isinstance(self.data, list) else [court.formatted() for court in self.data.values() if court.is_available()]

class CourtDuration(Enum):
    FORTY_MINUTES = 'badminton-40min'
    SIXTY_MINUTES = 'badminton-60min'

    def __str__(self):
        return self.value