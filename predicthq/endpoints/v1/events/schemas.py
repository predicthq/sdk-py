from datetime import date, datetime
from typing import List, Optional, Tuple, Union

from pydantic import BaseModel, field_validator

from predicthq.endpoints.schemas import ResultSet


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


class Geo(BaseModel):
    geometry: Union[Point, MultiPoint, Polygon, MultiPolygon]
    placekey: Optional[str] = None


class ParentEvent(BaseModel):
    parent_event_id: str


class ImpactPatternImpacts(BaseModel):
    date_local: date
    value: int
    position: str


class ImpactPattern(BaseModel):

    vertical: str
    impact_type: str
    impacts: List[ImpactPatternImpacts]


class Event(BaseModel):
    cancelled: Optional[datetime] = None
    category: str
    country: str
    deleted_reason: Optional[str] = None
    description: Optional[str] = None
    duplicate_of_id: Optional[str] = None
    duration: Optional[int] = None
    end: Optional[datetime] = None
    first_seen: Optional[datetime] = None
    geo: Optional[Geo] = None
    id: str
    impact_patterns: Optional[List[ImpactPattern]] = []
    labels: List[str]
    location: Optional[Tuple[float, float]] = None
    parent_event: Optional[ParentEvent] = None
    place_hierarchies: Optional[List[List[str]]] = None
    postponed: Optional[datetime] = None
    relevance: Optional[float] = None
    scope: Optional[str] = None
    start: datetime
    state: Optional[str] = None
    timezone: Optional[str] = None
    title: str
    updated: Optional[datetime] = None

    # The below fields are only available if they are enabled in your plan.
    aviation_rank: Optional[int] = None  # Aviation Rank add-on
    brand_safe: Optional[bool] = None
    entities: Optional[List[Entities]] = []  # Venues and addresses add-on
    local_rank: Optional[int] = None  # Local Rank add-on
    phq_attendance: Optional[int] = None  # PHQ Attendance add-on
    predicted_end: Optional[datetime] = None
    private: Optional[bool] = None  # Loop add-on
    rank: Optional[int] = None  # PHQ Rank add-on
    predicted_event_spend: Optional[int] = None  # Predicted Event Spend add-on
    predicted_event_spend_industries: Optional[PredictedEventSpendIndustries] = None  # Predicted Event Spend add-on


class EventResultSet(ResultSet):
    overflow: Optional[bool] = False
    results: List[Optional[Event]]


class CountResultSet(BaseModel):
    count: int
    top_rank: float
    rank_levels: dict
    categories: dict
    labels: dict


class CalendarDay(BaseModel):
    date: date
    count: int
    top_rank: float
    rank_levels: dict
    categories: dict
    labels: dict
    top_events: EventResultSet


class CalendarResultSet(ResultSet):
    results: List[Optional[CalendarDay]]
