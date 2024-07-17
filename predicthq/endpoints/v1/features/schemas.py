from datetime import date
from typing import Dict, List, Optional, Union

from pydantic import BaseModel, RootModel

from predicthq.endpoints.schemas import ResultSet


class FeatureRankLevel(BaseModel):
    rank_levels: dict


class FeatureStats(BaseModel):
    avg: Optional[float] = None
    count: Optional[int] = None
    max: Optional[float] = None
    median: Optional[float] = None
    min: Optional[float] = None
    sum: Optional[float] = None
    std_dev: Optional[float] = None


class FeatureStat(BaseModel):
    stats: FeatureStats


class Feature(RootModel):
    root: Dict[str, Union[date, FeatureStat, FeatureRankLevel]]

    def __getattr__(self, name: str) -> Union[date, FeatureStat, FeatureRankLevel]:
        return self.root[name]


class FeatureResultSet(ResultSet):
    results: List[Optional[Feature]]
