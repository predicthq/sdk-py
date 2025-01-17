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


class AllowExtra(BaseModel):
    model_config: ConfigDict = ConfigDict(extra="allow")


class CreateAnalysisResponse(AllowExtra):
    analysis_id: str


class GeoPoint(AllowExtra):
    lat: str
    lon: str


class Location(AllowExtra):
    geopoint: GeoPoint
    radius: float
    unit: str
    google_place_id: Optional[str] = None


class RankLevel(AllowExtra):
    min: int
    max: Optional[int] = None


class RankLevels(AllowExtra):
    phq: Optional[RankLevel] = None
    local: Optional[RankLevel] = None


class Rank(AllowExtra):
    type: str
    levels: Optional[RankLevels] = None


class AnalysisDateRange(AllowExtra):
    start: datetime
    end: datetime


class BestPracticeChecks(AllowExtra):
    industry: bool = False
    rank: bool = False
    radius: bool = False


class AnalysisReadinessChecks(AllowExtra):
    date_range: Optional[AnalysisDateRange] = None
    error_code: Optional[str] = None
    missing_dates: Optional[List[str]] = None
    validation_response: Optional[dict] = None
    best_practice: bool
    best_practice_checks: BestPracticeChecks


class ProcessingCompleted(AllowExtra):
    correlation: bool
    feature_importance: bool
    value_quant: bool


class DemandTypeGroup(AllowExtra):
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


class Analysis(AllowExtra):
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


class FeatureGroup(AllowExtra):
    feature_group: str
    features: List[str]
    p_value: float
    important: bool


class FeatureImportance(AllowExtra):
    feature_importance: List[FeatureGroup]


class CorrelationResultSet(BeamPaginationResultSet):
    model_version: str
    version: int
    results: List[dict] = Field(alias="dates")


class CreateAnalysisGroupResponse(AllowExtra):
    group_id: str


class ExcludedAnalysis(AllowExtra):
    analysis_id: str
    reason: str
    excluded_from: List[str]


class ProcessingCompletedGroup(AllowExtra):
    feature_importance: bool
    value_quant: bool
    excluded_analyses: List[ExcludedAnalysis]


class AnalysisGroup(AllowExtra):
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
