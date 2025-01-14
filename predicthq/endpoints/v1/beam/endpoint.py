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
)
from predicthq.endpoints.decorators import accepts, returns
from typing import overload, List


class BeamEndpoint:
    def __init__(self, client):
        self.analysis = self.Analysis(client)

    class Analysis(BaseEndpoint):
        @accepts(query_string=False)
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
        @returns(CreateAnalysisResponse)
        def create(self, **params):
            verify_ssl = params.pop("config.verify_ssl", True)
            return self.client.post(
                self.build_url("v1", "beam", "analysis"),
                json=params,
                verify=verify_ssl,
            )

        @accepts()
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
                f"{self.build_url('v1', 'beam', 'analysis')}{analysis_id}/",
                params=params,
                verify=verify_ssl,
            )

        @accepts(query_string=False)
        @overload
        def update(
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
        def update(self, analysis_id: str, **params):
            verify_ssl = params.pop("config.verify_ssl", True)
            return self.client.patch(
                f"{self.build_url('v1', 'beam', 'analysis')}{analysis_id}/",
                json=params,
                verify=verify_ssl,
            )

        @accepts()
        def delete(self, analysis_id: str, **params):
            verify_ssl = params.pop("config.verify_ssl", True)
            return self.client.delete(
                f"{self.build_url('v1', 'beam', 'analysis')}{analysis_id}/",
                params=params,
                verify=verify_ssl,
            )

        @accepts()
        def refresh(self, analysis_id: str, **params):
            verify_ssl = params.pop("config.verify_ssl", True)
            return self.client.post(
                f"{self.build_url('v1', 'beam', 'analysis')}{analysis_id}/refresh/",
                params=params,
                verify=verify_ssl,
            )

        @accepts()
        @returns(EventResultSet)
        def get_events(self, analysis_id: str, **params):
            verify_ssl = params.pop("config.verify_ssl", True)
            return self.client.get(
                f"{self.build_url('v1', 'beam', 'analysis')}{analysis_id}/events/",
                params=params,
                verify=verify_ssl,
            )

        @accepts()
        @returns(Event)
        def get_event(self, analysis_id: str, event_id: str, **params):
            verify_ssl = params.pop("config.verify_ssl", True)
            return self.client.get(
                f"{self.build_url('v1', 'beam', 'analysis')}{analysis_id}/events/{event_id}/",
                params=params,
                verify=verify_ssl,
            )

        @accepts()
        @returns(CorrelationResultSet)
        def get_correlation(self, analysis_id: str, **params):
            verify_ssl = params.pop("config.verify_ssl", True)
            return self.client.get(
                f"{self.build_url('v1', 'beam', 'analysis')}{analysis_id}/correlate/",
                params=params,
                verify=verify_ssl,
            )

        @accepts()
        @returns(FeatureImportance)
        def get_feature_importance(self, analysis_id: str, **params):
            verify_ssl = params.pop("config.verify_ssl", True)
            return self.client.get(
                f"{self.build_url('v1', 'beam', 'analysis')}{analysis_id}/feature-importance/",
                params=params,
                verify=verify_ssl,
            )

        @accepts()
        @returns(ValueQuant)
        def get_value_quant(self, analysis_id: str, **params):
            verify_ssl = params.pop("config.verify_ssl", True)
            return self.client.get(
                f"{self.build_url('v1', 'beam', 'analysis')}{analysis_id}/value-quant/",
                params=params,
                verify=verify_ssl,
            )

        @accepts(query_string=False)
        def upload_demand(self, analysis_id: str, **params):
            verify_ssl = params.pop("config.verify_ssl", True)
            return self.client.post(
                f"{self.build_url('v1', 'beam', 'analysis')}{analysis_id}/sink/",
                params=params,
                verify=verify_ssl,
            )
