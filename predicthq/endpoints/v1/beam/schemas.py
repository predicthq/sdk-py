from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from predicthq.endpoints.schemas import ArgKwargResultSet
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


class BeamPaginationResultSet(ArgKwargResultSet):
    def has_next(self):
        return self._kwargs.get("offset", 0) + len(self.results) < self.count

    def get_next(self):
        if "offset" in self._kwargs:
            self._kwargs["offset"] = self._kwargs.get("offset") + len(self.results)
        else:
            self._kwargs["offset"] = len(self.results)
        return self._more(**self._kwargs)



class CreateAnalysisResponse(BaseModel):
    model_config: ConfigDict = ConfigDict(extra="allow")

    analysis_id: str


class GeoPoint(BaseModel):
    model_config: ConfigDict = ConfigDict(extra="allow")

    lat: str
    lon: str


class Location(BaseModel):
    model_config: ConfigDict = ConfigDict(extra="allow")

    geopoint: GeoPoint
    radius: float
    unit: str
    google_place_id: Optional[str] = None


class RankLevel(BaseModel):
    model_config: ConfigDict = ConfigDict(extra="allow")

    min: int
    max: Optional[int] = None


class RankLevels(BaseModel):
    model_config: ConfigDict = ConfigDict(extra="allow")

    phq: Optional[RankLevel] = None
    local: Optional[RankLevel] = None


class Rank(BaseModel):
    model_config: ConfigDict = ConfigDict(extra="allow")

    type: str
    levels: Optional[RankLevels] = None


class AnalysisDateRange(BaseModel):
    model_config: ConfigDict = ConfigDict(extra="allow")

    start: datetime
    end: datetime


class BestPracticeChecks(BaseModel):
    model_config: ConfigDict = ConfigDict(extra="allow")

    industry: bool = False
    rank: bool = False
    radius: bool = False


class AnalysisReadinessChecks(BaseModel):
    model_config: ConfigDict = ConfigDict(extra="allow")

    date_range: Optional[AnalysisDateRange] = None
    error_code: Optional[str] = None
    missing_dates: Optional[List[str]] = None
    validation_response: Optional[dict] = None
    best_practice: bool
    best_practice_checks: BestPracticeChecks


class ProcessingCompleted(BaseModel):
    model_config: ConfigDict = ConfigDict(extra="allow")

    correlation: bool
    feature_importance: bool
    value_quant: bool


class DemandTypeGroup(BaseModel):
    model_config: ConfigDict = ConfigDict(extra="allow")

    interval: str
    week_start_day: Optional[str] = None
    industry: Optional[str] = None
    unit_descriptor: Optional[str] = None
    currency_code: str


class DemandType(DemandTypeGroup):
    interval: str
    week_start_day: Optional[str] = None
    industry: Optional[str] = None
    unit_descriptor: Optional[str] = None
    unit_currency_multiplier: float
    currency_code: str


class RadiusUnit(StrEnum):
    m = "m"
    km = "km"
    mi = "mi"
    ft = "ft"


class GeoJsonGeometryType(StrEnum):
    POINT = "Point"
    POLYGON = "Polygon"
    MULTI_POLYGON = "MultiPolygon"
    LINE_STRING = "LineString"
    MULTI_LINE_STRING = "MultiLineString"


class GeoJsonProperties(BaseModel):
    radius: Annotated[float, Field(gt=0)]
    radius_unit: RadiusUnit


class GeoJsonGeometry(BaseModel):
    type: GeoJsonGeometryType
    coordinates: Annotated[list, Field(min_length=1)]


class GeoJson(BaseModel):
    type: Literal["Feature"]
    properties: Optional[GeoJsonProperties] = None
    geometry: GeoJsonGeometry


class Place(BaseModel):
    place_id: int
    type: str
    name: str
    county: Optional[str] = None
    region: Optional[str] = None
    country: Optional[str] = None
    geojson: GeoJson


class SavedLocation(BaseModel):
    name: Optional[str] = None
    formatted_address: Optional[str] = None
    geojson: Optional[GeoJson] = None
    h3: Optional[List[str]] = None
    place_ids: Optional[List[int]] = None
    place_hierarchies: Optional[List[str]] = None
    places: Optional[List[Place]] = None
    location_id: str


class Analysis(BaseModel):
    model_config: ConfigDict = ConfigDict(extra="allow")

    analysis_id: Optional[str] = None
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
    group_ids: Optional[List[str]] = None
    tz: Optional[str] = None
    create_dt: datetime
    update_dt: datetime
    processed_dt: Optional[datetime] = None
    external_id: Optional[str] = None
    label: Optional[List[str]] = None
    saved_location: Optional[SavedLocation] = None


class AnalysisResultSet(BeamPaginationResultSet):
    results: List[Analysis] = Field(alias="analyses")


class FeatureGroup(BaseModel):
    model_config: ConfigDict = ConfigDict(extra="allow")

    feature_group: str
    features: List[str]
    p_value: float
    important: bool


class FeatureImportance(BaseModel):
    model_config: ConfigDict = ConfigDict(extra="allow")

    feature_importance: List[FeatureGroup]


class CorrelationResult(BaseModel):
    date: str
    actual_demand: Optional[float] = None
    baseline_demand: Optional[float] = None
    remainder: Optional[float] = None
    impact_significance: str
    impact_significance_score: Optional[int] = None


class CorrelationResultSet(BeamPaginationResultSet):
    model_config = ConfigDict(protected_namespaces=())
    model_version: str
    version: int
    results: List[CorrelationResult] = Field(alias="dates")


class CreateAnalysisGroupResponse(BaseModel):
    model_config: ConfigDict = ConfigDict(extra="allow")

    group_id: str


class ExcludedAnalysis(BaseModel):
    model_config: ConfigDict = ConfigDict(extra="allow")

    analysis_id: str
    reason: str
    excluded_from: List[str]


class ProcessingCompletedGroup(BaseModel):
    model_config: ConfigDict = ConfigDict(extra="allow")

    feature_importance: bool
    value_quant: bool
    excluded_analyses: List[ExcludedAnalysis]


class AnalysisGroup(BaseModel):
    model_config: ConfigDict = ConfigDict(extra="allow")

    group_id: Optional[str] = None
    name: str
    analysis_ids: List[str]
    user_id: Optional[str] = None
    processing_completed: ProcessingCompletedGroup
    readiness_status: Optional[str] = None
    demand_type: Optional[DemandTypeGroup] = None
    status: str
    create_dt: datetime
    update_dt: datetime
    processed_dt: Optional[datetime] = None


class AnalysisGroupResultSet(BeamPaginationResultSet):
    results: List[AnalysisGroup] = Field(alias="groups")
