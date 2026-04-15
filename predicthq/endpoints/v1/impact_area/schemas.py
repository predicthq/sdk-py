from typing import List, Optional, Union

from pydantic import BaseModel


class LocationResult(BaseModel):
    lat: str
    lon: str


class RadiusProperties(BaseModel):
    radius: Optional[float] = None
    radius_unit: Optional[str] = None


class Point(BaseModel):
    type: str
    coordinates: List[float]


class Polygon(BaseModel):
    type: str
    coordinates: List[List[List[float]]]


class MultiPolygon(BaseModel):
    type: str
    coordinates: List[List[List[List[float]]]]


class GeoJsonFeature(BaseModel):
    type: str = "Feature"
    properties: Optional[RadiusProperties] = None
    geometry: Union[Point, Polygon, MultiPolygon]


class ImpactAreaResultSet(BaseModel):
    location: LocationResult
    warnings: List[str] = []
    geojson: GeoJsonFeature
