from typing import List, Optional, Tuple

from pydantic import BaseModel, field_validator

from predicthq.endpoints.schemas import ResultSet


class Place(BaseModel):
    id: str
    type: str
    name: str
    county: Optional[str] = None
    region: Optional[str] = None
    country: Optional[str] = None
    country_alpha2: Optional[str] = None
    country_alpha3: Optional[str] = None
    location: Tuple[float, float]

    @field_validator("location")
    def reverse_location(cls, value: Tuple[float, float]):
        """
        Location is received as follows:
        "location": [lon, lat]
        By convention, we are used to have geopoints formated as lat,lon, which is what this validator enforces
        """
        return value[1], value[0]


class PlaceResultSet(ResultSet):
    results: List[Optional[Place]]
