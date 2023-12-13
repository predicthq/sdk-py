from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from predicthq.endpoints.schemas import ResultSet


class GeoPoint(BaseModel):
    lat: float
    lon: float


class BroadcastEventEntities(BaseModel):
    entity_id: str
    type: str
    name: str
    formatted_address: Optional[str] = None


class BroadcastEventLocation(BaseModel):
    geopoint: GeoPoint
    place_hierarchies: List[List[str]]
    country: str


class BroadcastEventDates(BaseModel):
    start: datetime
    end: Optional[datetime] = None
    start_local: datetime
    end_local: Optional[datetime] = None
    timezone: str

    # predicted_end_local is a paid feature.
    # It will only show up in your response body if you
    # have subscribed to it.
    predicted_end_local: Optional[datetime] = None


class BroadcastEvent(BaseModel):
    event_id: str
    title: str
    category: str
    labels: List[str]
    dates: BroadcastEventDates
    location: BroadcastEventLocation
    entities: List[BroadcastEventEntities]

    # The following fields are paid features.
    # They will only show up in your response body if you
    # have subscribed to them.
    phq_attendance: Optional[int] = None
    phq_rank: Optional[int] = None
    local_rank: Optional[int] = None
    aviation_rank: Optional[int] = None


class Place(BaseModel):
    place_id: str
    type: str
    name: str
    county: str
    region: str
    country: str


class BroadcastLocation(BaseModel):
    geopoint: GeoPoint
    place_hierarchies: List[List[str]]
    places: List[Place]
    country: str


class BroadcastDates(BaseModel):
    start: datetime
    start_local: datetime
    timezone: str


class Broadcast(BaseModel):
    broadcast_id: str
    updated: datetime
    first_seen: datetime
    dates: Optional[BroadcastDates] = None
    location: Optional[BroadcastLocation] = None
    phq_viewership: Optional[int] = None
    record_status: str
    broadcast_status: Optional[str] = None
    event: Optional[BroadcastEvent] = None


class BroadcastResultSet(ResultSet):
    overflow: bool
    results: List[Optional[Broadcast]]
