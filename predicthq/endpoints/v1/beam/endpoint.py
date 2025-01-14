from predicthq.endpoints.base import BaseEndpoint
from .schemas import (
    CreateAnalysisResponse,
    AnalysisResultSet,
    Analysis,
    EventResultSet,
    Event,
    FeatureImportance,
    ValueQuant,
    CorrelationResultSet,
    CreateAnalysisGroupResponse,
    AnalysisGroup,
    AnalysisGroupResultSet,
)
from predicthq.endpoints.decorators import accepts, returns
from typing import overload, List
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
            location__radius: float = None,
            location__unit: str = None,
            location__google_place_id: str = None,
            location__geoscope_paths: List[str] = None,
            rank__type: str = None,
            rank__levels__phq: dict = None,
            rank__levels__local: dict = None,
            demand_type__industry: str = None,
            demand_type__unit_descriptor: str = None,
            demand_type__unit_currency_multiplier: float = None,
            demand_type__currency_code: str = None,
            tz: str = None,
            external_id: str = None,
            label: List[str] = None,
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
            updated__gt: str = None,
            updated__gte: str = None,
            updated__lt: str = None,
            updated__lte: str = None,
            q: str = None,
            status: List[str] = None,
            group_id: List[str] = None,
            demand_type__interval: List[str] = None,
            demand_type__industry: List[str] = None,
            readiness_status: List[str] = None,
            include_deleted: bool = None,
            sort: List[str] = None,
            offset: int = None,
            limit: int = None,
            external_id: List[str] = None,
            label: List[str] = None,
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
            name: str = None,
            location__geopoint: dict = None,
            location__radius: float = None,
            location__unit: str = None,
            location__google_place_id: str = None,
            location__geoscope_paths: List[str] = None,
            rank__type: str = None,
            rank__levels__phq: dict = None,
            rank__levels__local: dict = None,
            demand_type__industry: str = None,
            demand_type__unit_descriptor: str = None,
            demand_type__unit_currency_multiplier: float = None,
            demand_type__currency_code: str = None,
            tz: str = None,
            external_id: str = None,
            label: List[str] = None,
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
        def search_events(
            self,
            analysis_id: str,
            start__gt: date = None,
            start__gte: date = None,
            start__lt: date = None,
            start__lte: date = None,
            end__gt: date = None,
            end__gte: date = None,
            end__lt: date = None,
            end__lte: date = None,
            active__gt: date = None,
            active__gte: date = None,
            active__lt: date = None,
            active__lte: date = None,
            impact__gt: date = None,
            impact__gte: date = None,
            impact__lt: date = None,
            impact__lte: date = None,
            **params,
        ): ...
        @accepts()
        @returns(EventResultSet)
        def search_events(self, analysis_id: str, **params):
            verify_ssl = params.pop("config.verify_ssl", True)
            return self.client.get(
                f"{self.build_url('v1', 'beam')}analyses/{analysis_id}/events/",
                params=params,
                verify=verify_ssl,
            )

        @accepts()
        @returns(Event)
        def get_event(self, analysis_id: str, event_id: str, **params):
            verify_ssl = params.pop("config.verify_ssl", True)
            return self.client.get(
                f"{self.build_url('v1', 'beam')}analyses/{analysis_id}/events/{event_id}/",
                params=params,
                verify=verify_ssl,
            )

        @overload
        def get_correlation(
            self,
            analysis_id: str,
            date__gt: date = None,
            date__gte: date = None,
            date__lt: date = None,
            date__lte: date = None,
            offset: int = None,
            limit: int = None,
            include_features: List[str] = None,
            **params,
        ): ...
        @accepts()
        @returns(CorrelationResultSet)
        def get_correlation(self, analysis_id: str, **params):
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

        @accepts()
        @returns(ValueQuant)
        def get_value_quant(self, analysis_id: str, **params):
            verify_ssl = params.pop("config.verify_ssl", True)
            return self.client.get(
                f"{self.build_url('v1', 'beam')}analyses/{analysis_id}/value-quant/",
                params=params,
                verify=verify_ssl,
            )

        # TODO this function needs to accept various types of demand data to upload
        @accepts(query_string=False)
        def upload_demand(self, analysis_id: str, **params):
            verify_ssl = params.pop("config.verify_ssl", True)
            return self.client.post(
                f"{self.build_url('v1', 'beam')}analyses/{analysis_id}/sink/",
                params=params,
                verify=verify_ssl,
            )

    class AnalysisGroupEndpoint(BaseEndpoint):
        @overload
        def create(
            self,
            name: str,
            analysis_ids: List[str],
            demand_type__unit_descriptor: str = None,
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
            updated__gt: str = None,
            updated__gte: str = None,
            updated__lt: str = None,
            updated__lte: str = None,
            q: str = None,
            status: List[str] = None,
            demand_type__interval: List[str] = None,
            demand_type__industry: List[str] = None,
            readiness_status: List[str] = None,
            include_deleted: bool = None,
            sort: List[str] = None,
            offset: int = None,
            limit: int = None,
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
            name: str = None,
            analysis_ids: List[str] = None,
            demand_type__unit_descriptor: str = None,
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
        def get_feature_importance(self, group_id: str = None, **params):
            verify_ssl = params.pop("config.verify_ssl", True)
            return self.client.get(
                f"{self.build_url('v1', 'beam')}analysis-groups/{group_id}/feature-importance/",
                params=params,
                verify=verify_ssl,
            )

        @accepts()
        @returns(ValueQuant)
        def get_value_quant(self, group_id: str = None, **params):
            verify_ssl = params.pop("config.verify_ssl", True)
            return self.client.get(
                f"{self.build_url('v1', 'beam')}analysis-groups/{group_id}/value-quant/",
                params=params,
                verify=verify_ssl,
            )
