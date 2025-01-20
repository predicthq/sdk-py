from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from predicthq.endpoints.schemas import ArgKwargResultSet
from typing import Optional, List


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
    unit_descriptor: str
    currency_code: str


class DemandType(DemandTypeGroup):
    interval: str
    week_start_day: Optional[str] = None
    industry: Optional[str] = None
    unit_descriptor: str
    unit_currency_multiplier: float
    currency_code: str


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


class CorrelationResultSet(BeamPaginationResultSet):
    model_version: str
    version: int
    results: List[dict] = Field(alias="dates")


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
