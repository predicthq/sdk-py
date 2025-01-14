from pydantic import BaseModel, Field
from datetime import datetime
from predicthq.endpoints.schemas import ResultSet


class CreateAnalysisResponse(BaseModel):
    analysis_id: str


class GeoPoint(BaseModel):
    lat: str
    lon: str


class Location(BaseModel):
    geopoint: GeoPoint
    radius: float
    unit: str
    google_place_id: str | None = None


class RankLevel(BaseModel):
    min: int
    max: int | None = None


class RankLevels(BaseModel):
    phq: RankLevel | None = None
    local: RankLevel | None = None


class Rank(BaseModel):
    type: str
    levels: RankLevels | None = None


class AnalysisDateRange(BaseModel):
    start: datetime
    end: datetime


class BestPracticeChecks(BaseModel):
    industry: bool = False
    rank: bool = False
    radius: bool = False


class AnalysisReadinessChecks(BaseModel):
    date_range: AnalysisDateRange | None = None
    error_code: str | None = None
    missing_dates: list[str] | None = None
    validation_response: dict | None = None
    best_practice: bool
    best_practice_checks: BestPracticeChecks


class ProcessingCompleted(BaseModel):
    correlation: bool
    feature_importance: bool
    value_quant: bool


class DemandType(BaseModel):
    interval: str
    week_start_day: str | None = None
    industry: str | None = None
    unit_descriptor: str
    unit_currency_multiplier: float
    currency_code: str


class Analysis(BaseModel):
    analysis_id: str
    name: str
    location: Location
    rank: Rank
    user_id: str | None = None
    access_type: str
    status: str
    readiness_status: str | None = None
    readiness_checks: AnalysisReadinessChecks
    processing_completed: ProcessingCompleted
    demand_type: DemandType
    group_ids: list[str] | None = None
    tz: str | None = None
    create_dt: datetime
    update_dt: datetime
    processed_dt: datetime | None = None
    external_id: str | None = None
    label: list[str] | None = None


class AnalysisResultSet(ResultSet):
    results: list[Analysis] = Field(alias="analyses")


class Address(BaseModel):
    locality: str | None = None
    country_code: str | None = None
    formatted_address: str | None = None
    postcode: str | None = None
    region: str | None = None


class Geo(BaseModel):
    address: Address | None = None


class Event(BaseModel):
    even_id: str
    category: str
    geo: Geo
    labels: list
    title: str
    timezone: str | None = None
    phq_rank: int | None = None
    local_rank: int | None = None
    formatted_address: str | None = None
    impact_patterns: list | None = None


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
    incremental: HistoricalInfo | None = None
    decremental: HistoricalInfo | None = None


class Prediction(BaseModel):
    incremental: Incremental


class ValueQuant(BaseModel):
    prediction: Prediction | None = None
    historical: Historical | None = None


class CorrelationResultSet(ResultSet):
    model_version: str
    version: str
    results: list[dict] = Field(alias="dates")
