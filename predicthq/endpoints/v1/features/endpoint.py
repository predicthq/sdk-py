from predicthq.endpoints.base import UserBaseEndpoint
from predicthq.endpoints.decorators import accepts, returns

from .schemas import FeatureResultSet


class FeaturesEndpoint(UserBaseEndpoint):
    BASE_FEATURE_CRITERIA = {"stats": [["sum", "count"]], "phq_rank": [None]}
    FIELDS_TO_MUTATE = frozenset(
        [
            "phq_attendance_",
            "phq_viewership_",
            "phq_impact_",
            "phq_spend_",
        ]
    )

    @classmethod
    def mutate_bool_to_default_for_type(cls, user_request_spec):
        for key, val in user_request_spec.items():
            if any(key.startswith(x) for x in cls.FIELDS_TO_MUTATE):
                user_request_spec[key] = [
                    cls.BASE_FEATURE_CRITERIA if isinstance(v, bool) else v for v in val
                ]

    @accepts(query_string=False)
    @returns(FeatureResultSet)
    # This is a temporary solution to get the next page for Features API
    # _params and _json are for internal use only
    def obtain_features(self, _params: dict = None, _json: dict = None, **request):
        verify_ssl = request.pop("config", {}).get("verify_ssl", True)
        return self.client.post(
            self.build_url("v1", "features"),
            json=_json or request,
            verify=verify_ssl,
            params=_params,
        )
