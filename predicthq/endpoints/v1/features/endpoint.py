import inspect

from predicthq.endpoints.base import UserBaseEndpoint
from predicthq.endpoints.decorators import accepts, returns
from .schemas import FeatureResultSet


class FeaturesEndpoint(UserBaseEndpoint):

    BASE_FEATURE_CRITERIA = {"stats": ["sum", "count"], "phq_rank": None}
    FIELDS_TO_MUTATE = frozenset([
        "phq_attendance_",
        "phq_viewership_sports",
        "phq_impact_severe_weather_",
        "phq_spend_"
    ])

    @classmethod
    def mutate_bool_to_default_for_type(cls, user_request_spec):
        for key, val in user_request_spec.items():
            if any(key.startswith(x) for x in cls.FIELDS_TO_MUTATE) and isinstance(val, bool):
                user_request_spec[key] = cls.BASE_FEATURE_CRITERIA

    @accepts(query_string=False)
    @returns(FeatureResultSet)
    def obtain_features(self, **request):
        verify_ssl = request.pop("config", {}).get("verify_ssl", True)
        return self.client.post(
            self.build_url("v1", "features"),
            json=request,
            verify=verify_ssl,
        )
