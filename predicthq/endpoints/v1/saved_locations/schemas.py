from datetime import date, datetime
from typing import List, Optional, Tuple, Union
from ..events.schemas import Event

from pydantic import BaseModel
from pydantic import Field, field_validator, model_validator, ConfigDict

from predicthq.endpoints.schemas import ResultSet

from typing import Optional, List

# Python < 3.11 does not have StrEnum in the enum module
import sys
if sys.version_info < (3, 11):
    import enum

    class StrEnum(str, enum.Enum):
        pass
else:
    from enum import StrEnum

# Python < 3.9 does not have Annotated
if sys.version_info < (3, 9):
    from typing_extensions import Annotated
else:
    from typing import Annotated

# Python < 3.8 does not have Literal
if sys.version_info < (3, 8):
    from typing_extensions import Literal
else:
    from typing import Literal


class RadiusUnit(StrEnum):
    METERS = "m"
    KILOMETERS = "km"
    FEET = "ft"
    MILES = "mi"


class Location(BaseModel):
    lat: str
    lon: str

    def as_geopoint(self) -> str:
        return f"{self.lat},{self.lon}"


class SuggestedRadiusResponse(BaseModel):
    model_config: ConfigDict = ConfigDict(extra="allow")

    radius: float
    radius_unit: RadiusUnit
    location: Location

class Entities(BaseModel):
    entity_id: str
    name: str
    type: str
    formatted_address: Optional[str] = None


class PredictedEventSpendIndustries(BaseModel):
    accommodation: int
    hospitality: int
    transportation: int


class Point(BaseModel):
    type: str
    coordinates: List[float]


class MultiPoint(BaseModel):
    type: str
    coordinates: List[List[float]]


class Polygon(BaseModel):
    type: str
    coordinates: List[List[List[float]]]


class MultiPolygon(BaseModel):
    type: str
    coordinates: List[List[List[List[float]]]]


class GeoAddress(BaseModel):
    country_code: Optional[str] = None
    formatted_address: Optional[str] = None
    locality: Optional[str] = None
    postcode: Optional[str] = None
    region: Optional[str] = None


class Geo(BaseModel):
    geometry: Union[Point, MultiPoint, Polygon, MultiPolygon]
    placekey: Optional[str] = None
    address: Optional[GeoAddress] = None


class SubscriptionValidType(StrEnum):
    BROADCASTS = "broadcasts"
    EVENTS = "events"
    FEATURES_API = "features_api"
    NOTIFICATIONS = "notifications"


class SavedLocationStatus(StrEnum):
    ACTIVE = "active"
    DELETED = "deleted"
    PENDING = "pending"


class DateRangeType(StrEnum):
    NEXT_90D = "next_90d"


class PhqModel(BaseModel):
    pass
    """Custom Pydantic BaseModel to handle a default json_encoder for datetime"""


class DateRange(PhqModel):
    type: DateRangeType
    start_dt: datetime
    end_dt: datetime


class SummaryInsights(PhqModel):
    date_range: DateRange
    phq_attendance_sum: int
    attended_event_count: int
    non_attended_event_count: int
    unscheduled_event_count: int
    demand_surge_count: Optional[int] = None
    venue_count: Optional[int] = None
    pes_total_sum: Optional[int] = None
    pes_accommodation_sum: Optional[int] = None
    pes_hospitality_sum: Optional[int] = None
    pes_transportation_sum: Optional[int] = None


Position = tuple[float, float] | tuple[float, float, float]


class Point(PhqModel):
    type: Literal["Point"] = "Point"
    coordinates: Position


class Polygon(PhqModel):
    type: Literal["Polygon"] = "Polygon"
    coordinates: list[list[Position]]


class MultiPolygon(PhqModel):
    type: Literal["MultiPolygon"] = "MultiPolygon"
    coordinates: list[list[list[Position]]]


class LineString(PhqModel):
    type: Literal["LineString"] = "LineString"
    coordinates: list[Position]


class MultiLineString(PhqModel):
    type: Literal["MultiLineString"] = "MultiLineString"
    coordinates: list[list[Position]]


Geometry = Point | Polygon | MultiPolygon | LineString | MultiLineString


class PlaceGeoJson(PhqModel):
    type: Literal["Feature"] = "Feature"
    geometry: Geometry


class Place(PhqModel):
    place_id: int
    type: str
    name: str
    county: Optional[str] = None
    region: Optional[str] = None
    country: Optional[str] = None
    geojson: PlaceGeoJson


class Properties(PhqModel):
    """Custom properties for embedding the radius information"""

    radius: float | None = None
    radius_unit: RadiusUnit | None = None


class GeoJson(PhqModel):
    type: Literal["Feature"]
    properties: Properties | None = None
    geometry: Geometry = Field(discriminator="type")


class SavedLocationBase(PhqModel):
    location_code: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    labels: Optional[list[str]] = None
    geojson: GeoJson | None = None
    place_ids: Optional[list[int]] = None
    formatted_address: Optional[str] = None


class SavedLocation(SavedLocationBase):
    location_id: str

    share_url: str | None = None

    create_dt: datetime
    update_dt: datetime
    enrich_dt: Optional[datetime] = None
    insights_dt: Optional[datetime] = None
    user_id: Optional[str] = None
    subscription_valid_types: Annotated[
        list[SubscriptionValidType], Field(default_factory=list)
    ]
    status: SavedLocationStatus
    summary_insights: Annotated[list[SummaryInsights], Field(default_factory=list)]
    places: Annotated[list[Place], Field(default_factory=list)]


class SavedLocationResultSet(ResultSet):
    results: List[Optional[SavedLocation]] = Field(alias="locations")


class CreateSavedLocationResponse(BaseModel):
    model_config: ConfigDict = ConfigDict(extra="allow")

    location_id: str


class PostSharingEnableResponse(BaseModel):
    model_config: ConfigDict = ConfigDict(extra="allow")

    share_url: str


