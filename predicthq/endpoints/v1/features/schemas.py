import csv
from datetime import date
from typing import Dict, List, Optional, Union

from pydantic import BaseModel, RootModel

from predicthq.endpoints.schemas import ArgKwargResultSet


class CsvMixin:
    def _flatten_json(self, separator: str) -> Optional[List[dict]]:
        def __flatten_json(d: dict, pk: str = "") -> dict:
            flat_json = {}
            for k, v in d.items():
                if isinstance(v, dict):
                    flat_json.update(
                        __flatten_json(v, f"{pk}{separator}{k}" if pk else k)
                    )
                    continue
                flat_json.update({f"{pk}{separator}{k}" if pk else k: v})
            return flat_json

        return [__flatten_json(d.model_dump(exclude_none=True)) for d in self.iter_all()]

    def to_csv(self, file: str, mode: str = "w+", separator: str = "_") -> None:
        header = None
        with open(file, mode=mode) as csv_file:
            csv_writer = csv.writer(csv_file)
            for d in self._flatten_json(separator):
                if not header:
                    header = list(d.keys())
                    csv_writer.writerow(header)
                csv_writer.writerow([d[h] for h in header])


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


class FeatureResultSet(ArgKwargResultSet, CsvMixin):
    results: List[Optional[Feature]]

    def get_next(self):
        if not self.has_next() or not hasattr(self, "_more"):
            return
        params = self._parse_params(self.next)
        return self._more(_params=params, _json=self._kwargs.get("_json", {}) or self._kwargs)
