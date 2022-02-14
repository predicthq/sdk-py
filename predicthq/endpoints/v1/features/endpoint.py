import inspect

from predicthq.endpoints.base import UserBaseEndpoint
from predicthq.endpoints.decorators import accepts, returns
from .schemas import FeatureRequest, FeatureResultSet


class FeaturesEndpoint(UserBaseEndpoint):

    BASE_FEATURE_CRITERIA = {"stats": ["sum", "count"], "phq_rank": None}

    @classmethod
    def mutate_bool_to_default_for_type(cls, user_request_spec):
        attributes = inspect.getmembers(FeatureRequest, lambda a: not (inspect.isroutine(a)))
        fields_to_mutate = [
            a[0] for a in attributes if a[0].startswith("phq_attendance_") or a[0].startswith("phq_viewership_sports")
        ]
        for key, val in user_request_spec.items():
            if key in fields_to_mutate and isinstance(val, bool):
                user_request_spec[key] = cls.BASE_FEATURE_CRITERIA

    @accepts(FeatureRequest, query_string=False)
    @returns(FeatureResultSet)
    def obtain_features(self, **request):
        verify_ssl = request.pop("config", {}).get("verify_ssl", True)
        return self.client.post(
            self.build_url("v1", "features"),
            json=request,
            verify=verify_ssl,
        )
