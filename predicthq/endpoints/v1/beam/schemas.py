from pydantic import BaseModel, Field
from datetime import datetime
from predicthq.endpoints.schemas import ResultSet
from typing import Optional


class CreateAnalysisResponse(BaseModel):
    analysis_id: str


class GeoPoint(BaseModel):
    lat: str
    lon: str


class Location(BaseModel):
    geopoint: GeoPoint
    radius: float
    unit: str
    google_place_id: Optional[str] = None


class RankLevel(BaseModel):
    min: int
    max: Optional[int] = None


class RankLevels(BaseModel):
    phq: Optional[RankLevel] = None
    local: Optional[RankLevel] = None


class Rank(BaseModel):
    type: str
    levels: Optional[RankLevels] = None


class AnalysisDateRange(BaseModel):
    start: datetime
    end: datetime


class BestPracticeChecks(BaseModel):
    industry: bool = False
    rank: bool = False
    radius: bool = False


class AnalysisReadinessChecks(BaseModel):
    date_range: Optional[AnalysisDateRange] = None
    error_code: Optional[str] = None
    missing_dates: Optional[list[str]] = None
    validation_response: Optional[dict] = None
    best_practice: bool
    best_practice_checks: BestPracticeChecks


class ProcessingCompleted(BaseModel):
    correlation: bool
    feature_importance: bool
    value_quant: bool


class DemandType(BaseModel):
    interval: str
    week_start_day: Optional[str] = None
    industry: Optional[str] = None
    unit_descriptor: str
    unit_currency_multiplier: float
    currency_code: str


class Analysis(BaseModel):
    analysis_id: str
    name: str
    location: Location
    rank: Rank
    user_id: Optional[str] = None
    access_type: str
    status: str
    readiness_status: Optional[str] = None
    readiness_checks: AnalysisReadinessChecks
    processing_completed: ProcessingCompleted
    demand_type: DemandType
    group_ids: Optional[list[str]] = None
    tz: Optional[str] = None
    create_dt: datetime
    update_dt: datetime
    processed_dt: Optional[datetime] = None
    external_id: Optional[str] = None
    label: Optional[list[str]] = None


class AnalysisResultSet(ResultSet):
    results: list[Analysis] = Field(alias="analyses")


class Address(BaseModel):
    locality: Optional[str] = None
    country_code: Optional[str] = None
    formatted_address: Optional[str] = None
    postcode: Optional[str] = None
    region: Optional[str] = None


class Geo(BaseModel):
    address: Optional[Address] = None


class Event(BaseModel):
    even_id: str
    category: str
    geo: Geo
    labels: list
    title: str
    timezone: Optional[str] = None
    phq_rank: Optional[int] = None
    local_rank: Optional[int] = None
    formatted_address: Optional[str] = None
    impact_patterns: Optional[list] = None


class EventResultSet(BaseModel):
    events: list[Event]


class FeatureGroup(BaseModel):
    feature_group: str
    features: list[str]
    p_value: float
    important: bool


class FeatureImportance(BaseModel):
    feature_importance: list[FeatureGroup]


class Incremental(BaseModel):
    forecast_uplift_pct_relative: float
    forecast_uplift_pct_absolute: float
    financial_uplift_annual: float
    unit_uplift_annual: float


class HistoricalInfo(BaseModel):
    anomalous_demand_pct: float
    event_contribution_pct: float
    event_financial_impact_annual: float


class Historical(BaseModel):
    anomalous_demand_pct: float
    event_contribution_pct: float
    total_event_contribution_pct: float
    incremental: Optional[HistoricalInfo] = None
    decremental: Optional[HistoricalInfo] = None


class Prediction(BaseModel):
    incremental: Incremental


class ValueQuant(BaseModel):
    prediction: Optional[Prediction] = None
    historical: Optional[Historical] = None


class CorrelationResultSet(ResultSet):
    model_version: str
    version: str
    results: list[dict] = Field(alias="dates")
