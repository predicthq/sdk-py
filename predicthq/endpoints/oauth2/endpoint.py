from predicthq.endpoints.base import BaseEndpoint
from predicthq.endpoints.decorators import accepts, returns
from .schemas import AccessToken, GetTokenParams, RevokeTokenParams


class OAuth2Endpoint(BaseEndpoint):

    @accepts(GetTokenParams)
    @returns(AccessToken)
    def get_token(self, client_id, client_secret, scope, grant_type, **kwargs):
        data = {
            "grant_type": grant_type,
            "scope": scope,
        }
        data.update(kwargs)
        return self.client.post('/oauth2/token/', auth=(client_id, client_secret), data=data)

    @accepts(RevokeTokenParams)
    def revoke_token(self, client_id, client_secret, token, token_type_hint):
        data = {
            "token_type_hint": token_type_hint,
            "token": token,
        }
        self.client.post('/oauth2/revoke/', auth=(client_id, client_secret), data=data)
