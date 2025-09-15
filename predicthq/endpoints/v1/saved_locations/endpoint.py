from predicthq.endpoints.base import UserBaseEndpoint, BaseEndpoint
from predicthq.endpoints.decorators import accepts, returns
from typing import overload, List, Optional
from .schemas import (
    SavedLocation,
    SavedLocationResultSet,
    CreateSavedLocationResponse,
    PostSharingEnableResponse,
    SuggestedRadiusResponse,
    Location,
)
from ..events.schemas import EventResultSet


class SavedLocationsEndpoint(UserBaseEndpoint):
    @overload
    def search(
        self,
        location_id: Optional[List[str]] = None,
        location_code: Optional[List[str]] = None,
        labels: Optional[List[str]] = None,
        user_id: Optional[List[str]] = None,
        subscription_valid_types: Optional[List[str]] = None,
        q: Optional[str] = None,
        sort: Optional[List[str]] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        **params,
    ): ...
    @accepts()
    @returns(SavedLocationResultSet)
    def search(self, **params):
        verify_ssl = params.pop("config.verify_ssl", True)
        result = self.client.get(
            self.build_url("v1", "saved-locations"),
            params=params,
            verify=verify_ssl,
        )
        return result

    @overload
    def create(
        self,
        name: str,
        geojson: dict,
        labels: Optional[List[str]] = None,
        location_code: Optional[str] = None,
        formatted_address: Optional[str] = None,
        description: Optional[str] = None,
        place_ids: Optional[List[str]] = None,
        **params,
    ): ...
    @accepts(query_string=False)
    @returns(CreateSavedLocationResponse)
    def create(self, **params):
        verify_ssl = params.pop("config.verify_ssl", True)

        result = self.client.post(
            f"{self.build_url('v1', 'saved-locations')}",
            json=params,
            verify=verify_ssl,
        )
        return result

    @accepts()
    @returns(SavedLocation)
    def get(self, location_id, **params):
        verify_ssl = params.pop("config.verify_ssl", True)
        return self.client.get(
            f"{self.build_url('v1', 'saved-locations')}{location_id}",
            params=params,
            verify=verify_ssl,
        )

    @overload
    def search_event_result_set(
        location_id: str,
        date_range_type: Optional[str] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        **params,
    ): ...
    @returns(EventResultSet)
    def search_event_result_set(self, location_id, **params):
        verify_ssl = params.pop("config.verify_ssl", True)
        url = f"{self.build_url('v1', 'saved-locations')}{location_id}/insights/events"
        response = self.client.get(
            url,
            params=params,
            verify=verify_ssl,
        )
        return response

    @accepts()
    def refresh_location_insights(self, location_id: str, **params):
        verify_ssl = params.pop("config.verify_ssl", True)
        return self.client.post(
            f"{self.build_url('v1', 'saved-locations')}{location_id}/insights/refresh",
            params=params,
            verify=verify_ssl,
        )

    @overload
    def replace_location_data(
        self,
        location_id: str,
        name: str,
        geojson: dict,
        labels: Optional[List[str]] = None,
        location_code: Optional[str] = None,
        formatted_address: Optional[str] = None,
        description: Optional[str] = None,
        place_ids: Optional[List[str]] = None,
        external_id: Optional[str] = None,
        **params,
    ): ...
    @accepts(query_string=False)
    def replace_location_data(self, location_id: str, **params):
        verify_ssl = params.pop("config.verify_ssl", True)
        params.pop("location_id", None)  # Remove location_id from payload
        response = self.client.put(
            f"{self.build_url('v1', 'saved-locations')}{location_id}",
            json=params,
            verify=verify_ssl,
        )
        return response

    @accepts()
    def delete_location(self, location_id: str, **params):
        verify_ssl = params.pop("config.verify_ssl", True)
        return self.client.delete(
            f"{self.build_url('v1', 'saved-locations')}{location_id}",
            params=params,
            verify=verify_ssl,
        )

    @accepts()
    @returns(PostSharingEnableResponse)
    def sharing_enable(self, location_id: str, **params):
        verify_ssl = params.pop("config.verify_ssl", True)
        return self.client.post(
            f"{self.build_url('v1', 'saved-locations')}{location_id}/sharing/enable",
            params=params,
            verify=verify_ssl,
        )

    @overload
    def suggested_radius(
        self,
        location_origin: Location,
        radius_unit: str,
        industry: str,
        **params,
    ): ...
    @accepts(query_string=False)
    @returns(SuggestedRadiusResponse)
    def suggested_radius(self, **params):
        verify_ssl = params.pop("config.verify_ssl", True)
        loc = params.pop("location_origin", None)
        if isinstance(loc, Location):
            params["location.origin"] = loc.as_geopoint()
        elif isinstance(loc, str):
            params["location.origin"] = loc
        return self.client.get(
            f"{self.build_url('v1', 'suggested-radius')}",
            params=params,
            verify=verify_ssl,
        )
