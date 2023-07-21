from pydantic import BaseModel


class LocationResult(BaseModel):
    lat: float
    lon: float


class SuggestedRadiusResultSet(BaseModel):
    radius: float
    radius_unit: str
    location: LocationResult
