from predicthq.endpoints.base import BaseEndpoint
from .schemas import (
    CreateAnalysisResponse,
    AnalysisResultSet,
    Analysis,
    FeatureImportance,
    CorrelationResultSet,
    CreateAnalysisGroupResponse,
    AnalysisGroup,
    AnalysisGroupResultSet,
)
from predicthq.endpoints.decorators import accepts, returns
from typing import overload, List, Optional, TextIO, Union
from datetime import date


class BeamEndpoint:
    def __init__(self, client):
        self.analysis = self.AnalysisEndpoint(client)
        self.analysis_group = self.AnalysisGroupEndpoint(client)

    class AnalysisEndpoint(BaseEndpoint):
        @overload
        def create(
            self,
            name: str,
            location__geopoint: dict,
            location__radius: Optional[float] = None,
            location__unit: Optional[str] = None,
            location__google_place_id: Optional[str] = None,
            location__geoscope_paths: Optional[List[str]] = None,
            rank__type: Optional[str] = None,
            rank__levels__phq: Optional[dict] = None,
            rank__levels__local: Optional[dict] = None,
            demand_type__industry: Optional[str] = None,
            demand_type__unit_descriptor: Optional[str] = None,
            demand_type__unit_currency_multiplier: Optional[float] = None,
            demand_type__currency_code: Optional[str] = None,
            tz: Optional[str] = None,
            external_id: Optional[str] = None,
            label: Optional[List[str]] = None,
            **params,
        ): ...
        @accepts(query_string=False)
        @returns(CreateAnalysisResponse)
        def create(self, **params):
            verify_ssl = params.pop("config.verify_ssl", True)
            return self.client.post(
                f"{self.build_url('v1', 'beam')}analyses/",
                json=params,
                verify=verify_ssl,
            )

        @overload
        def search(
            self,
            updated__gt: Optional[str] = None,
            updated__gte: Optional[str] = None,
            updated__lt: Optional[str] = None,
            updated__lte: Optional[str] = None,
            q: Optional[str] = None,
            status: Optional[List[str]] = None,
            group_id: Optional[List[str]] = None,
            demand_type__interval: Optional[List[str]] = None,
            demand_type__industry: Optional[List[str]] = None,
            readiness_status: Optional[List[str]] = None,
            include_deleted: Optional[bool] = None,
            sort: Optional[List[str]] = None,
            offset: Optional[int] = None,
            limit: Optional[int] = None,
            external_id: Optional[List[str]] = None,
            label: Optional[List[str]] = None,
            **params,
        ): ...
        @accepts()
        @returns(AnalysisResultSet)
        def search(self, **params):
            verify_ssl = params.pop("config.verify_ssl", True)
            return self.client.get(
                f"{self.build_url('v1', 'beam')}analyses/",
                params=params,
                verify=verify_ssl,
            )

        @accepts()
        @returns(Analysis)
        def get(self, analysis_id, **params):
            verify_ssl = params.pop("config.verify_ssl", True)
            return self.client.get(
                f"{self.build_url('v1', 'beam')}analyses/{analysis_id}/",
                params=params,
                verify=verify_ssl,
            )

        @overload
        def update(
            self,
            analysis_id: str,
            name: Optional[str] = None,
            location__geopoint: Optional[dict] = None,
            location__radius: Optional[float] = None,
            location__unit: Optional[str] = None,
            location__google_place_id: Optional[str] = None,
            location__geoscope_paths: Optional[List[str]] = None,
            rank__type: Optional[str] = None,
            rank__levels__phq: Optional[dict] = None,
            rank__levels__local: Optional[dict] = None,
            demand_type__industry: Optional[str] = None,
            demand_type__unit_descriptor: Optional[str] = None,
            demand_type__unit_currency_multiplier: Optional[float] = None,
            demand_type__currency_code: Optional[str] = None,
            tz: Optional[str] = None,
            external_id: Optional[str] = None,
            label: Optional[List[str]] = None,
            **params,
        ): ...
        @accepts(query_string=False)
        def update(self, analysis_id: str, **params):
            verify_ssl = params.pop("config.verify_ssl", True)
            return self.client.patch(
                f"{self.build_url('v1', 'beam')}analyses/{analysis_id}/",
                json=params,
                verify=verify_ssl,
            )

        @accepts()
        def delete(self, analysis_id: str, **params):
            verify_ssl = params.pop("config.verify_ssl", True)
            return self.client.delete(
                f"{self.build_url('v1', 'beam')}analyses/{analysis_id}/",
                params=params,
                verify=verify_ssl,
            )

        @accepts()
        def refresh(self, analysis_id: str, **params):
            verify_ssl = params.pop("config.verify_ssl", True)
            return self.client.post(
                f"{self.build_url('v1', 'beam')}analyses/{analysis_id}/refresh/",
                params=params,
                verify=verify_ssl,
            )

        @overload
        def get_correlation_results(
            self,
            analysis_id: str,
            date__gt: Optional[date] = None,
            date__gte: Optional[date] = None,
            date__lt: Optional[date] = None,
            date__lte: Optional[date] = None,
            offset: Optional[int] = None,
            limit: Optional[int] = None,
            include_features: Optional[List[str]] = None,
            **params,
        ): ...
        @accepts()
        @returns(CorrelationResultSet)
        def get_correlation_results(self, analysis_id: str, **params):
            verify_ssl = params.pop("config.verify_ssl", True)
            return self.client.get(
                f"{self.build_url('v1', 'beam')}analyses/{analysis_id}/correlate/",
                params=params,
                verify=verify_ssl,
            )

        @accepts()
        @returns(FeatureImportance)
        def get_feature_importance(self, analysis_id: str, **params):
            verify_ssl = params.pop("config.verify_ssl", True)
            return self.client.get(
                f"{self.build_url('v1', 'beam')}analyses/{analysis_id}/feature-importance/",
                params=params,
                verify=verify_ssl,
            )

        @accepts(query_string=False)
        @overload
        def upload_demand(
            self,
            analysis_id: str,
            json: Optional[Union[str, TextIO]] = None,
            ndjson:  Optional[Union[str, TextIO]] = None,
            csv:  Optional[Union[str, TextIO]] = None,
            **params,
        ): ...
        def upload_demand(self, analysis_id: str, **params):
            verify_ssl = params.pop("config.verify_ssl", True)
            if json := params.pop("json", None):
                headers = {"Content-Type": "application/json"}
                file = json
            if ndjson := params.pop("ndjson", None):
                headers = {"Content-Type": "application/x-ndjson"}
                file = ndjson
            if csv := params.pop("csv", None):
                headers = {"Content-Type": "text/csv"}
                file = csv

            if isinstance(file, str):
                with open(file) as f:
                    return self.client.post(
                        f"{self.build_url('v1', 'beam')}analyses/{analysis_id}/sink/",
                        data=f.read(),
                        headers=headers,
                        verify=verify_ssl,
                    )

            return self.client.post(
                f"{self.build_url('v1', 'beam')}analyses/{analysis_id}/sink/",
                data=file.read(),
                headers=headers,
                verify=verify_ssl,
            )

    class AnalysisGroupEndpoint(BaseEndpoint):
        @overload
        def create(
            self,
            name: str,
            analysis_ids: List[str],
            demand_type__unit_descriptor: Optional[str] = None,
            **params,
        ): ...
        @accepts(query_string=False)
        @returns(CreateAnalysisGroupResponse)
        def create(self, **params):
            verify_ssl = params.pop("config.verify_ssl", True)
            return self.client.post(
                f"{self.build_url('v1', 'beam')}analysis-groups/",
                json=params,
                verify=verify_ssl,
            )

        @overload
        def search(
            self,
            updated__gt: Optional[str] = None,
            updated__gte: Optional[str] = None,
            updated__lt: Optional[str] = None,
            updated__lte: Optional[str] = None,
            q: Optional[str] = None,
            status: Optional[List[str]] = None,
            demand_type__interval: Optional[List[str]] = None,
            demand_type__industry: Optional[List[str]] = None,
            readiness_status: Optional[List[str]] = None,
            include_deleted: Optional[bool] = None,
            sort: Optional[List[str]] = None,
            offset: Optional[int] = None,
            limit: Optional[int] = None,
            **params,
        ): ...
        @accepts()
        @returns(AnalysisGroupResultSet)
        def search(self, **params):
            verify_ssl = params.pop("config.verify_ssl", True)
            return self.client.get(
                f"{self.build_url('v1', 'beam')}analysis-groups/",
                params=params,
                verify=verify_ssl,
            )

        @accepts()
        @returns(AnalysisGroup)
        def get(self, group_id: str, **params):
            verify_ssl = params.pop("config.verify_ssl", True)
            return self.client.get(
                f"{self.build_url('v1', 'beam')}analysis-groups/{group_id}/",
                params=params,
                verify=verify_ssl,
            )

        @overload
        def update(
            self,
            group_id: str,
            name: Optional[str] = None,
            analysis_ids: Optional[List[str]] = None,
            demand_type__unit_descriptor: Optional[str] = None,
            **params,
        ): ...
        @accepts(query_string=False)
        def update(self, group_id: str, **params):
            verify_ssl = params.pop("config.verify_ssl", True)
            return self.client.patch(
                f"{self.build_url('v1', 'beam')}analysis-groups/{group_id}/",
                json=params,
                verify=verify_ssl,
            )

        @accepts()
        def delete(self, group_id: str, **params):
            verify_ssl = params.pop("config.verify_ssl", True)
            return self.client.delete(
                f"{self.build_url('v1', 'beam')}analysis-groups/{group_id}/",
                params=params,
                verify=verify_ssl,
            )

        @accepts()
        def refresh(self, group_id: str, **params):
            verify_ssl = params.pop("config.verify_ssl", True)
            return self.client.post(
                f"{self.build_url('v1', 'beam')}analysis-groups/{group_id}/refresh/",
                params=params,
                verify=verify_ssl,
            )

        @accepts()
        @returns(FeatureImportance)
        def get_feature_importance(self, group_id: str, **params):
            verify_ssl = params.pop("config.verify_ssl", True)
            return self.client.get(
                f"{self.build_url('v1', 'beam')}analysis-groups/{group_id}/feature-importance/",
                params=params,
                verify=verify_ssl,
            )
