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


class PlaceResultSet(ResultSet):
    results: List[Optional[Place]]
