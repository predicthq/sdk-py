from predicthq.endpoints.base import UserBaseEndpoint
from predicthq.endpoints.decorators import accepts, returns
from .schemas import (
    FeatureRequest, FeatureResultSet
)


class FeaturesEndpoint(UserBaseEndpoint):

    @accepts(FeatureRequest, query_string=False)
    @returns(FeatureResultSet)
    def obtain_features(self, **request):
        return self.client.post(self.build_url('v1', 'features'), json=request)
